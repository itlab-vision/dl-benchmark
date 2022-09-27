import argparse
import logging as log
import os
import sys

from config_parser import ConfigParser
from executors import Executor
from process import Process


def cli_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config',
                        help='Path to configuration file for all models',
                        type=str,
                        dest='config_path',
                        required=True)
    parser.add_argument('--executor_type',
                        type=str,
                        choices=['host_machine', 'docker_container'],
                        help='The environment in which quantization will be executed',
                        default='host_machine',
                        dest='executor_type')

    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        raise ValueError('Wrong path to configuration file!')

    return args


def quantization(executor_type, quantization_parameters, log):
    process_executor = Executor.get_executor(executor_type, log)
    for i, params in enumerate(quantization_parameters):
        log.info('Start quantization model #{}!'.format(i + 1))
        quant_process = Process(params, process_executor, log)
        quant_process.execute()
        log.info('End quantization model #{}!'.format(i + 1))


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout
    )
    try:
        args = cli_parser()
        parser = ConfigParser(args.config_path)
        quantization_parameters = parser.parse()

        log.info('Start quantization on {}!'.format(args.executor_type))

        quantization(args.executor_type, quantization_parameters, log)

        log.info('End quantization!')
        parser.clean()
        log.info('Work is done!')
    except Exception as exp:
        log.error(str(exp))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
