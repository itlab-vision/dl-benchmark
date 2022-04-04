import os
import sys
import argparse
import logging as log
from parameters import parameters
from executors import executor
from process import process
from output import output_handler as out_hand
from config_parser import parser


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file',
        type=str, dest='config_path', required=True)
    parser.add_argument(
        '-s', '--source',
        help='Path to directory in which input images will be searched',
        type=str, dest='source_path', required=True)
    parser.add_argument(
        '-r', '--result',
        help='Full name of the resulting file',
        type=str, dest='result_file', required=True)
    parser.add_argument(
        '-d', '--definitions',
        help='Path to the global datasets configuration file',
        type=str, dest='definitions_path', default=None, required=True)
    parser.add_argument(
        '-a', '--annotations',
        help='Path to directory in which annotation and meta files will be searched',
        type=str, dest='annotations_path', default=None, required=False)
    parser.add_argument(
        '-e', '--extensions',
        help='Path to directory with InferenceEngine extensions',
        type=str, dest='extensions_path', default=None, required=False)
    parser.add_argument('--executor_type', type=str, choices=['host_machine', 'docker_container'],
                        help='The environment in which the tests will be executed', default='host_machine')
    config = parser.parse_args().config_path
    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')
    source = parser.parse_args().source_path
    annotations = parser.parse_args().annotations_path
    definitions = parser.parse_args().definitions_path
    extensions = parser.parse_args().extensions_path
    result = parser.parse_args().result_file
    executor_type = parser.parse_args().executor_type
    return config, source, annotations, definitions, extensions, result, executor_type


def accuracy_check(executor_type, test_list, output_handler, log):
    process_executor = executor.get_executor(executor_type, log)
    process_executor.prepare_executor(test_list)
    for idx, test in enumerate(test_list):
        test_process = process(log, process_executor, test)
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
        config, source, annotations, definitions, extensions, result_table, executor_type = build_argparser()
        test_parameters = parameters(source, annotations, definitions, extensions)
        test_list = parser.get_test_list(config, test_parameters)
        log.info('Create result table with name: {}'.format(result_table))
        output_handler = out_hand(result_table)
        output_handler.create_table()
        log.info('Start {} accuracy tests'.format(len(test_list)))
        accuracy_check(executor_type, test_list, output_handler, log)
        log.info('End inference tests')
        log.info('Work is done!')
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
