import argparse
import logging as log
import sys
from pathlib import Path

from config_processor import process_config
from executors import Executor
from frameworks.framework_wrapper_registry import FrameworkWrapperRegistry
from output import OutputHandler

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger, exception_hook  # noqa: E402
from constants import Status  # noqa: E402


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config',
                        type=str,
                        dest='config_path',
                        help='Path to configuration file',
                        required=True)
    parser.add_argument('-r', '--result',
                        type=str,
                        dest='result_file',
                        help='Full name of the resulting file',
                        required=True)
    parser.add_argument('--csv_delimiter',
                        metavar='CHARACTER',
                        type=str,
                        help='Delimiter to use in the resulting file',
                        default=';')
    parser.add_argument('--executor_type',
                        type=str,
                        choices=['host_machine', 'docker_container'],
                        help='Environment to execute test: host_machine, docker_container',
                        default='host_machine')
    parser.add_argument('-b', '--cpp_benchmarks_dir',
                        type=str,
                        help='Path to the folder with pre-built C++ benchmark apps',
                        default=None,
                        required=False)
    parser.add_argument('--openvino_cpp_benchmark_dir',
                        type=str,
                        help='Path to the folder with pre-built OpenVINO C++ Benchmark App',
                        default=None,
                        required=False)

    args = parser.parse_args()

    if not Path(args.config_path).is_file():
        raise ValueError('Wrong path to configuration file!')

    return args


def inference_benchmark(executor_type, test_list, output_handler, log,
                        cpp_benchmarks_dir=None, openvino_cpp_benchmark_dir=None):
    status = Status.EXIT_SUCCESS

    try:
        process_executor = Executor.get_executor(executor_type, log)
    except ValueError as ex:
        log.error(ex, exc_info=True)
        return Status.EXECUTOR_NOT_FOUND

    for test in test_list:
        framework_name = test.indep_parameters.inference_framework
        benchmarks_path = cpp_benchmarks_dir
        if 'openvino' in framework_name.lower():
            benchmarks_path = openvino_cpp_benchmark_dir

        try:
            log.info('Creating separate process for the test')
            test_process = FrameworkWrapperRegistry()[framework_name].create_process(
                test, process_executor, log, benchmarks_path)

            log.info('Executing process')
            test_process.execute()

            test_status = test_process.get_status()
            if test_status != Status.EXIT_SUCCESS.value:
                status = Status.INFERENCE_FAILURE
                log.error(f'Test finished with non-zero code: {test_status}')
        except Exception as ex:
            status = Status.INFERENCE_EXCEPTION
            log.error(f'Inference failed with exception: {ex}', exc_info=True)
            test_process = None

        log.info('Saving test result in file')
        output_handler.add_row_to_table(process_executor, test, test_process)

    return status


if __name__ == '__main__':
    configure_logger()
    sys.excepthook = exception_hook

    args = cli_argument_parser()

    log.info(f'Parsing configuration file {args.config_path}')
    test_list = process_config(args.config_path, log)

    log.info(f'Create result table with name: {args.result_file}')

    output_handler = OutputHandler(args.result_file, args.csv_delimiter)
    output_handler.create_table()

    log.info(f'Start {len(test_list)} inference tests')

    inference_status = inference_benchmark(args.executor_type, test_list,
                                           output_handler, log,
                                           args.cpp_benchmarks_dir,
                                           args.openvino_cpp_benchmark_dir)
    log.info('Inference tests completed' if not inference_status.value else 'Inference tests failed')
    sys.exit(inference_status.value)
