import argparse
import logging as log
import os
import sys

from config_parser import TestResultParser
from executors import Executor
from output import OutputHandler
from parameters import Parameters
from process import ProcessHandler


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file',
        type=str,
        dest='config_path',
        required=True)
    parser.add_argument(
        '-s', '--source',
        help='Path to directory in which input images will be searched',
        type=str,
        dest='source_path',
        required=True)
    parser.add_argument(
        '-r', '--result',
        help='Full name of the resulting file',
        type=str,
        dest='result_file',
        required=True)
    parser.add_argument(
        '-d', '--definitions',
        help='Path to the global datasets configuration file',
        type=str,
        dest='definitions_path',
        default=None,
        required=True)
    parser.add_argument(
        '-a', '--annotations',
        help='Path to annotation and meta files directory',
        type=str,
        dest='annotations_path',
        default=None,
        required=False)
    parser.add_argument(
        '-e', '--extensions',
        help='Path to InferenceEngine extensions directory',
        type=str,
        dest='extensions_path',
        default=None,
        required=False)
    parser.add_argument(
        '--executor_type',
        type=str,
        choices=['host_machine', 'docker_container'],
        help='Environment ro execute test: host_machine, docker_container',
        default='host_machine')

    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        raise ValueError('Wrong path to configuration file!')

    return args


def accuracy_check(executor_type, test_list, output_handler, log):
    process_executor = Executor.get_executor(executor_type, log)
    process_executor.prepare_executor(test_list)
    for idx, test in enumerate(test_list):
        test_process = ProcessHandler(log, process_executor, test)
        test_process.execute(idx)
        log.info('Saving test result in file')
        output_handler.add_results(test, test_process, process_executor)


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout
    )

    try:
        args = cli_argument_parser()

        test_parameters = Parameters(args.source_path, args.annotations_path, args.definitions_path,
                                     args.extensions_path)
        test_list = TestResultParser.get_test_list(args.config, test_parameters)

        log.info('Create result table with name: {}'.format(args.result_file))

        output_handler = OutputHandler(args.result_file)
        output_handler.create_table()

        log.info('Start {} accuracy tests'.format(len(test_list)))

        accuracy_check(args.executor_type, test_list, output_handler, log)

        log.info('Inference tests completed')
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
