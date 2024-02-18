import argparse
import json
import sys
import traceback

from pathlib import Path

import postprocessing_data as pp

from utils import (set_input_to_blobs, get_request_result, create_core, create_model,
                   configure_model, get_input_shape, reshape_input, compile_model)
from inference_tools.loop_tools import loop_inference
from io_adapter import IOAdapter
from io_model_wrapper import OpenVINOIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import OpenVINOTransformer

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .xml file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_xml')
    parser.add_argument('-w', '--weights',
                        help='Path to an .bin file with a trained weights.',
                        required=True,
                        type=str,
                        dest='model_bin')
    parser.add_argument('-i', '--input',
                        help='Data for input layers in format:'
                             'input_layer_name:path_to_image1,path_to_image2..'
                             'or input_layer_name:path_to_folder_with_images',
                        required=False,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--extension',
                        help='Path to INTEL_CPU (CPU, MYRIAD) custom layers',
                        type=str,
                        default=None,
                        dest='extension')
    parser.add_argument('-c', '--intel_gpu_config',
                        help='Path to INTEL_GPU config.',
                        type=str,
                        default=None,
                        dest='intel_gpu_config')
    parser.add_argument('-d', '--device',
                        help='Specify the target'
                             'device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable.'
                             'Support HETERO and MULTI plugins.'
                             'Use HETERO:<Device1>,<Device2>,... for HETERO plugin.'
                             'Use MULTI:<Device1>,<Device2>,... for MULTI plugin.'
                             'Sample will look for a suitable plugin for device specified (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--default_device',
                        help='Default device for heterogeneous inference',
                        choices=['CPU', 'GPU', 'MYRIAD', 'FGPA'],
                        default=None,
                        type=str,
                        dest='default_device')
    parser.add_argument('--dump',
                        help='Dump information about the model execution',
                        type=bool,
                        default=False,
                        dest='dump')
    parser.add_argument('-p', '--priority',
                        help='Priority for multi-device inference in descending order.'
                             'Use format <Device1>,<Device2> First device has top priority',
                        default=None,
                        type=str,
                        dest='priority')
    parser.add_argument('-a', '--affinity',
                        help='Path to file with affinity per layer in format <layer> <device> '
                             'for heterogeneous inference',
                        default=None,
                        type=str,
                        dest='affinity')
    parser.add_argument('--labels',
                        help='Labels mapping file',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results',
                        default=10,
                        type=int,
                        dest='number_top')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('-nthreads', '--number_threads',
                        help='Number of threads to use for inference on the CPU. (Max by default)',
                        type=int,
                        default=None,
                        dest='nthreads')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=[
                            'classification', 'detection', 'segmentation', 'recognition-face',
                            'person-attributes', 'age-gender', 'gaze', 'head-pose', 'person-detection-asl',
                            'adas-segmentation', 'road-segmentation', 'license-plate', 'instance-segmentation',
                            'single-image-super-resolution', 'sphereface', 'person-detection-action-recognition-old',
                            'person-detection-action-recognition-new', 'person-detection-raisinghand-recognition',
                            'person-detection-action-recognition-teacher', 'human-pose-estimation',
                            'action-recognition-encoder', 'driver-action-recognition-encoder', 'reidentification',
                            'driver-action-recognition-decoder', 'action-recognition-decoder', 'face-detection',
                            'mask-rcnn', 'yolo_tiny_voc', 'yolo_v2_voc', 'yolo_v2_coco', 'yolo_v2_tiny_coco',
                            'yolo_v3', 'yolo_v3_tf'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('--color_map',
                        help='Classes color map',
                        type=str,
                        default=None,
                        dest='color_map')
    parser.add_argument('--prob_threshold',
                        help='Probability threshold for detections filtering',
                        default=0.5,
                        type=float,
                        dest='threshold')
    parser.add_argument('-mi', '--mininfer',
                        help='Min inference time of single pass',
                        type=float,
                        default=0.0,
                        dest='mininfer')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'openvino_sync_inference_report.json',
                        dest='report_path')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')

    args = parser.parse_args()

    return args


def infer_sync(compiled_model, number_iter, get_slice, test_duration):
    request = compiled_model.create_infer_request()
    result = None
    time_infer, _ = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice, request)
    if number_iter == 1:
        result = get_request_result(request)
    return result, time_infer


def inference_iteration(get_slice, request):
    set_input_to_blobs(request, get_slice())
    exec_time = infer_slice(request)
    return exec_time


def infer_slice(request):
    request.infer()
    exec_time = request.latency / 1000
    return exec_time


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='OpenVINO')
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    try:
        model_wrapper = OpenVINOIOModelWrapper()
        data_transformer = OpenVINOTransformer()
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)
        core = create_core(
            args.extension,
            args.intel_gpu_config,
            args.device,
            args.nthreads,
            None,
            args.dump,
            'sync',
            log,
        )
        model = create_model(core, args.model_xml, args.model_bin, log)
        configure_model(core, model, args.device, args.default_device, args.affinity)
        input_shapes = get_input_shape(model_wrapper, model)

        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))

        reshape_input(model, args.batch_size)

        if args.input:
            log.info(f'Preparing input data: {args.input}')
            io.prepare_input(model, args.input)
        else:
            io.fill_unset_inputs(model, log)

        log.info('Create executable network')
        compiled_model = compile_model(core, model, args.device, args.priority)

        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, inference_time = infer_sync(compiled_model, args.number_iter, io.get_slice_input, args.time)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time, args.mininfer)

        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')

        del model
        del compiled_model
        del core
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
