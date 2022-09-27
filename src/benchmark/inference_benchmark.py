import argparse
import logging as log
import os
import sys

import config_parser
from output import OutputHandler
from processes import Process
from executors import Executor


def cli_parser():
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
                        help='The environment in which the tests will be executed',
                        default='host_machine')

    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        raise ValueError('Wrong path to configuration file!')

    return args


def inference_benchmark(executor_type, test_list, output_handler, log):
    process_executor = Executor.get_executor(executor_type, log)
    for test in test_list:
        test_process = Process.get_process(test, process_executor, log)
        test_process.execute()

        log.info('Saving test result in file')
        output_handler.add_row_to_table(process_executor, test, test_process)


if __name__ == '__main__':
    try:
        log.basicConfig(
            format='[ %(levelname)s ] %(message)s',
            level=log.INFO,
            stream=sys.stdout
        )

        args = cli_parser()
        test_list = config_parser.process_config(args.config_path, log)

        log.info(f'Create result table with name: {args.result_file}')

        output_handler = OutputHandler(args.result_file)
        output_handler.create_table()

        log.info('Start {} inference tests'.format(len(test_list)))

        inference_benchmark(args.executor_type, test_list, output_handler, log)

        log.info('End inference tests')
        log.info('Work is done!')
    except Exception as exp:
        log.error(str(exp))
