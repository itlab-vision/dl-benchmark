import argparse
import json
import sys
from pathlib import Path

import spektral
import tensorflow as tf

import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from reporter.report_writer import ReportWriter
import spektral_auxiliary

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.model_converters.tf2tflite.tensorflow_common import (get_gpu_devices, is_gpu_available, restrisct_gpu_usage)  # noqa

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger   # noqa: E402


log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to a .keras file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-i', '--input',
                        help='Dataset or .bin file to import',
                        required=True,
                        type=str,
                        dest='input')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'sp_inference_report.json',
                        dest='report_path')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--time',
                        help='Time in seconds to execute topology.',
                        required=False,
                        default=0,
                        type=int,
                        dest='time')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['node-classification'],
                        default='feedforward_spektral',
                        type=str,
                        dest='task')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--restrisct_gpu_usage',
                        action='store_true',
                        help='Restrict TensorFlow to only use the first GPU')
    args = parser.parse_args()

    return args


def model_load(model_path):
    log.info(f'Loading network files:\n\t {model_path}')
    file_type = str(model_path).split('.')[-1]
    if file_type != 'keras':
        raise ValueError('Only .keras model save file type is supported.')
    compiled_model = tf.keras.saving.load_model(model_path, compile=True)

    return compiled_model


def prepare_output(result, task):
    if task == 'feedforward':
        return {}
    elif task == 'node-classification':
        return result
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def inference_spektral(model, number_iter, get_slice, test_duration):
    result = None
    time_infer = []
    log.info(f'Starting inference ({number_iter} iterations or {test_duration} seconds)')

    if number_iter == 1:
        slice_input = get_slice()
        result, exec_time = infer_slice(model, slice_input)
        time_infer.append(exec_time)
    else:
        time_infer = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice, model)['time_infer']
    log.info('Inference completed')

    return result, time_infer


def inference_iteration(get_slice, model):
    slice_input = get_slice()
    _, exec_time = infer_slice(model, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(model, slice_input):
    res = model(slice_input, training=False)
    return res


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='Spektral', version=spektral.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)

    if args.device == 'NVIDIA_GPU':
        if is_gpu_available():
            if args.restrisct_gpu_usage:
                log.info('Restruct GPU usage to 1 GPU device')
                restrisct_gpu_usage()
        else:
            raise AssertionError('NVIDIA_GPU device not found on hostmachine, unable to infer on NVIDIA_GPU')

    if args.device == 'CPU' and is_gpu_available():
        log.warning(f'NVIDIA_GPU device(s) {get_gpu_devices()} available on machine,'
                    f' tensorflow will use NVIDIA_GPU by default')

    io = spektral_auxiliary.SpektralIO.get_io_adapter(args, None, None)
    model = model_load(Path(args.model_path))
    io.prepare_input(model, args.input)

    result, inference_time = inference_spektral(model, args.number_iter, io.get_slice_input, args.time)

    log.info('Computing performance metrics')
    inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)

    report_writer.update_execution_results(**inference_result)
    log.info(f'Writing report to {args.report_path}')
    report_writer.write_report(args.report_path)

    if not args.raw_output:
        if args.number_iter == 1:
            try:
                log.info('Converting output tensor to print results')
                result = prepare_output(result, args.task)
                log.info('Inference results')
                io.process_output(result, log)
            except Exception as ex:
                log.warning('Error when printing inference results. {0}'.format(str(ex)))

    log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')


if __name__ == '__main__':
    sys.exit(main() or 0)
