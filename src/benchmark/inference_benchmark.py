import argparse
import logging as log
import os
import sys

from config_processor import process_config
from executors import Executor
from frameworks.framework_wrapper_registry import FrameworkWrapperRegistry
from output import OutputHandler


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
    parser.add_argument('--executor_type',
                        type=str,
                        choices=['host_machine', 'docker_container'],
                        help='Environment ro execute test: host_machine, docker_container',
                        default='host_machine')
    parser.add_argument('-b', '--cpp_benchmark_path',
                        type=str,
                        dest='cpp_benchmark_path',
                        help='Path to pre-built C++ Benchmark App',
                        default=None,
                        required=False)

    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        raise ValueError('Wrong path to configuration file!')

    return args


def inference_benchmark(executor_type, test_list, output_handler, log, cpp_benchmark_path=None):
    process_executor = Executor.get_executor(executor_type, log)
    for test in test_list:
        framework_name = test.indep_parameters.inference_framework
        test_process = FrameworkWrapperRegistry()[framework_name].create_process(test, process_executor,
                                                                                 log, cpp_benchmark_path)
        test_process.execute()

        log.info('Saving test result in file\n')
        output_handler.add_row_to_table(process_executor, test, test_process)


if __name__ == '__main__':
    try:
        log.basicConfig(
            format='[ %(levelname)s ] %(message)s',
            level=log.INFO,
            stream=sys.stdout,
        )

        args = cli_argument_parser()
        test_list = process_config(args.config_path, log)

        log.info(f'Create result table with name: {args.result_file}')

        output_handler = OutputHandler(args.result_file)
        output_handler.create_table()

        log.info(f'Start {len(test_list)} inference tests\n')

        inference_benchmark(args.executor_type, test_list, output_handler, log, args.cpp_benchmark_path)

        log.info('Inference tests completed')
    except Exception as exp:
        log.error(str(exp))
