import os
import sys
import argparse
import logging as log

from config_parser import config_parser
from process import process
from executors import executor


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file for all models',
        type=str, dest='config_path', required=True
    )
    parser.add_argument(
        '--executor_type',
        type=str, choices=['host_machine', 'docker_container'],
        help='The environment in which quantization will be executed',
        default='host_machine', dest='executor_type'
    )
    executor_type = parser.parse_args().executor_type
    config = parser.parse_args().config_path
    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')
    return config, executor_type


def quantization(executor_type, quantization_parameters, log):
    process_executor = executor.get_executor(executor_type, log)
    for i, params in enumerate(quantization_parameters):
        log.info('Start quantization model #{}!'.format(i + 1))
        quant_process = process(params, process_executor, log)
        quant_process.execute()
        log.info('End quantization model #{}!'.format(i + 1))


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout
    )
    try:
        config, executor_type = build_argparser()
        parser = config_parser(config)
        quantization_parameters = parser.parse()
        log.info('Start quantization on {}!'.format(executor_type))
        quantization(executor_type, quantization_parameters, log)
        log.info('End quantization!')
        parser.clean()
        log.info('Work is done!')
    except Exception as exp:
        log.error(str(exp))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
