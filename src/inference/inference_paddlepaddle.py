import paddle.inference as paddle_infer
import argparse
import json
import sys
from pathlib import Path
import traceback

import postprocessing_data as pp
import preprocessing_data as prep
from inference_tools.loop_tools import get_exec_time
from inference_tools.loop_tools import loop_inference
from io_adapter import IOAdapter
from io_model_wrapper import PaddlePaddleIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import PaddlePaddleTransformer

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402
log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',
                        help='Path to a .pdmodel file.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-p', '--params',
                        help='Path to .pdiparams file.',
                        required=True,
                        type=str,
                        dest='params_path')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=False,
                        default=None,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('-nthreads', '--number_threads',
                        help='Number of threads to use for inference on the CPU (1 by default)',
                        default=1,
                        type=int,
                        dest='number_threads')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=None,
                        type=str,
                        dest='mean')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        default=None,
                        type=str,
                        dest='input_scale')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('--input_shapes',
                        help='Input tensor shapes',
                        default=None,
                        type=str,
                        dest='input_shapes',
                        required=True)
    parser.add_argument('--input_names',
                        help='Names of the input tensors',
                        default=None,
                        type=prep.names_arg,
                        dest='input_names')
    parser.add_argument('--output_names',
                        help='Name of the output tensor',
                        default=None,
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results to print',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'paddle_inference_report.json',
                        dest='report_path')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology')
    parser.add_argument('--memory_pool_init_size_mb', required=False, default=1000, type=int,
                        dest='memory_pool_init_size_mb', help='Initial size of the the allocated gpu memory, in MB')

    args = parser.parse_args()

    return args


def inference_paddlepaddle(predictor, number_iter, get_slice, test_duration):
    result = None
    input_info = predictor.get_input_names()
    outputs = predictor.get_output_names()
    if number_iter > 1:
        time_infer, _ = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice,
                                                                                        input_info, predictor)
    else:
        exec_time = inference_iteration(get_slice, input_info, predictor)
        result = {}
        for name in outputs:
            output_tensor = predictor.get_output_handle(name)
            output_data = output_tensor.copy_to_cpu()
            result[name] = output_data
        time_infer = [exec_time]
    return result, time_infer


def inference_iteration(get_slice, input_info, predictor):
    for name, data in get_slice().items():
        input_tensor = predictor.get_input_handle(name)
        input_tensor.copy_from_cpu(data)
    _, exec_time = infer_slice(predictor)
    return exec_time


@get_exec_time()
def infer_slice(predictor):
    predictor.run()


def prepare_output(result, output_names, task):
    if (output_names is None) or (len(result) != len(output_names)):
        raise ValueError('The number of output tensors does not match the number of corresponding output names')
    if task == 'classification':
        return result
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def main():
    try:
        args = cli_argument_parser()

        report_writer = ReportWriter()
        report_writer.update_framework_info(name='PaddlePaddle', version=paddle_infer.get_version())
        report_writer.update_configuration_setup(batch_size=args.batch_size,
                                                 iterations_num=args.number_iter,
                                                 target_device=args.device)

        config = paddle_infer.Config(args.model_path, args.params_path)

        config.enable_memory_optim()
        if args.device == 'GPU':
            config.enable_use_gpu(args.memory_pool_init_size_mb, 0)
        else:
            config.set_cpu_math_library_num_threads(args.number_threads)
        predictor = paddle_infer.create_predictor(config)
        args.input_shapes = prep.parse_input_arg(args.input_shapes, args.input_names)
        for name in predictor.get_input_names():
            predictor.get_input_handle(name).reshape(args.input_shapes[name])
        model_wrapper = PaddlePaddleIOModelWrapper(predictor)

        args.mean = prep.parse_input_arg(args.mean, args.input_names)
        args.input_scale = prep.parse_input_arg(args.input_scale, args.input_names)
        args.layout = prep.parse_layout_arg(args.layout, args.input_names)

        data_transformer = PaddlePaddleTransformer(prep.create_dict_for_transformer(args, 'NCHW'))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        if args.input and args.input != ['None']:
            log.info(f'Preparing input data: {args.input}')
            io.prepare_input(predictor, args.input)
        else:
            io.fill_unset_inputs(predictor, log)

        log.info(f'Starting inference ({args.number_iter} iterations)')
        result, inference_time = inference_paddlepaddle(predictor, args.number_iter, io.get_slice_input, args.time)

        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)

        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.task)

                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

            log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
