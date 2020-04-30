import os
import sys
import utils
import output
import argparse
import config_parser
import logging as log

from processes import process
from executors import executor


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'config_path',
        help = 'Path to configuration file', required = True)
    parser.add_argument('-f', '--filename', type = str, dest = 'result_file',
        help = 'Full name of the resulting file', required = True)
    parser.add_argument('--enviroment', type = str, default='host_machine',
        help = 'The environment in which the tests will be executed')
    parser.add_argument('--enviroment_config', type = str, default='',
        help = 'Path to enviroment configuration file')
    parser.add_argument('--inference_folder', type = str, default='',
        help = 'Path to folder with inference scripts')
    config = parser.parse_args().config_path
    result = parser.parse_args().result_file
    enviroment = parser.parse_args().enviroment
    enviroment_config = parser.parse_args().enviroment_config
    inference_folder = parser.parse_args().inference_folder
    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')
    return config, result, enviroment, enviroment_config, inference_folder


def inference_benchmark(enviroment, test_list, result_table, enviroment_config, inference_folder, log):
    process_executor = executor.get_executor(enviroment, enviroment_config, log)
    for test in test_list:
        test_process = process.get_process(test, process_executor, inference_folder, log)
        test_process.execute()

        test_status = 'Success' if test_process.get_status() == 0 else 'Failed'
        input_shape = test_process.get_model_shape()
        average_time, fps, latency = test_process.get_performance_metrics()

        log.info('Saving test result in file')
        table_row = output.create_table_row(test_status, test.model, test.dataset,
            test.indep_parameters, test.dep_parameters, test.indep_parameters.inference_framework, input_shape, average_time, latency, fps)
        output.add_row_to_table(result_table, table_row)


if __name__ == '__main__':
    try:
        log.basicConfig(format = '[ %(levelname)s ] %(message)s',
            level = log.INFO, stream = sys.stdout)
        config, result_table, enviroment, enviroment_config, inference_folder = build_parser()
        test_list = config_parser.process_config(config, log)
        log.info('Create result table with name: {}'.format(result_table))
        output.create_table(result_table)
        log.info('Start {} inference tests'.format(len(test_list)))
        inference_benchmark(enviroment, test_list, result_table, enviroment_config, inference_folder, log)
        log.info('End inference tests')
        log.info('Work is done!')
    except Exception as exp:
        log.error(str(exp))