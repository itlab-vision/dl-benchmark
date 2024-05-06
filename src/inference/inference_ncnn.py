import argparse
import sys
import traceback
from pathlib import Path

import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import NcnnIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import NcnnTransformer
from ncnn_auxiliary import (load_model, prepare_output, validate_task)

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
sys.path.append(str(Path(__file__).parent.parent.parent))

from logger_conf import configure_logger  # noqa: E402
log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-m', '--model',
                        help='Model name.',
                        choices=['squeezenet', 'shufflenetv2', 'faster_rcnn', 'rfcn',
                                 'mobilenet_ssd', 'mobilenetv2_ssdlite', 'mobilenetv3_ssdlite',
                                 'retinaface', 'squeezenet_ssd', 'mobilenet_yolov2',
                                 'mobilenetv2_yolov3', 'yolov4_tiny', 'yolov5s', 'yolov8s'],
                        required=True,
                        type=str,
                        dest='model')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxHxWxC, B is a batch size,'
                             'H is an input tensor height,'
                             'W is an input tensor width,'
                             'C is an input tensor number of channels.',
                        default=[1, 256, 256, 3],
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack.'
                             'Should be the same as B in input_shape argument.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file.',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results.',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Task type. Default: feedforward.',
                        choices=['feedforward', 'classification',
                                 'detection', 'face-detection'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations.',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs.',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default).',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--num_threads',
                        help='Number of threads.',
                        default=4,
                        type=int,
                        dest='num_threads')
    parser.add_argument('--time',
                        required=False,
                        default=0,
                        type=int,
                        dest='time',
                        help='Optional. Maximum test duration. 0 if no restrictions.')
    parser.add_argument('--threshold',
                        help='Probability threshold for detections filtering',
                        default=0.5,
                        type=float,
                        dest='threshold')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'ncnn_inference_report.json',
                        dest='report_path')
    args = parser.parse_args()

    return args


def inference_ncnn(net, number_iter, input_name, batch_size, get_slice, test_duration):
    result = None
    time_infer = []
    log.info(f'Starting inference ({number_iter} iterations)')
    if number_iter == 1:
        slice_input = get_slice()
        result, exec_time = infer_slice(input_name, batch_size, net, slice_input)
        time_infer.append(exec_time)
    else:
        loop_results = loop_inference(number_iter, test_duration)(inference_iteration)(input_name,
                                                                                       batch_size,
                                                                                       net,
                                                                                       get_slice)
        time_infer = loop_results['time_infer']
    log.info('Inference completed')
    return result, time_infer


def inference_iteration(input_name, batch_size, net, get_slice):
    slice_input = get_slice()
    _, exec_time = infer_slice(input_name, batch_size, net, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(input_name, batch_size, net, slice_input):
    res = []
    for i in range(batch_size):
        image = slice_input[input_name][i]
        net_result = net(image)
        res.append(net_result)
    return res


def main():
    try:
        args = cli_argument_parser()
        model_wrapper = NcnnIOModelWrapper(args)
        data_transformer = NcnnTransformer()
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        report_writer = ReportWriter()
        report_writer.update_framework_info(name='ncnn')
        report_writer.update_configuration_setup(batch_size=args.batch_size,
                                                 iterations_num=args.number_iter,
                                                 target_device=args.device)

        validate_task(args.model, args.task)

        io.prepare_input(args.model, args.input)
        net = load_model(args)

        result, inference_time = inference_ncnn(net, args.number_iter, args.input_name,
                                                args.input_shape[0], io.get_slice_input, args.time)

        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)
        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    result = prepare_output(result, args.task, model_wrapper)
                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning(f'Error when printing inference results. {str(ex)}')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
