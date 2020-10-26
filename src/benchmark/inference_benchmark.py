import os
import sys
import argparse
import config_parser
import logging as log

from output import output_handler as out_hand
from processes import process
from executors import executor


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, dest='config_path', help='Path to configuration file', required=True)
    parser.add_argument('-r', '--result', type=str, dest='result_file', help='Full name of the resulting file', required=True)
    parser.add_argument('--executor_type', type=str, choices=['host_machine', 'docker_container'], help='The environment in which the tests will be executed', default='host_machine')
    config = parser.parse_args().config_path
    result = parser.parse_args().result_file
    executor_type = parser.parse_args().executor_type
    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')
    return config, result, executor_type


def inference_benchmark(executor_type, test_list, output_handler, log):
    process_executor = executor.get_executor(executor_type, log)
    for test in test_list:
        test_process = process.get_process(test, process_executor, log)
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
        config, result_table, executor_type = build_parser()
        test_list = config_parser.process_config(config, log)
        log.info('Create result table with name: {}'.format(result_table))
        output_handler = out_hand(result_table)
        output_handler.create_table()
        log.info('Start {} inference tests'.format(len(test_list)))
        inference_benchmark(executor_type, test_list, output_handler, log)
        log.info('End inference tests')
        log.info('Work is done!')
    except Exception as exp:
        log.error(str(exp))
