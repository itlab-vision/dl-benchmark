import argparse
import sys
from pathlib import Path

from config_parser import ConfigParser
from executors import Executor
from process import ProcessHandler

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger, exception_hook  # noqa: E402

log = configure_logger()

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def cli_argument_parser():
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

    if not Path(args.config_path).is_file():
        raise ValueError('Wrong path to configuration file!')

    return args


def quantization(executor_type, quantization_parameters, log):
    status = EXIT_SUCCESS

    try:
        process_executor = Executor.get_executor(executor_type, log)
    except ValueError as ex:
        log.error(ex, exc_info=True)
        return EXIT_FAILURE

    for idx, params in enumerate(quantization_parameters):
        quant_process = ProcessHandler(params, process_executor, log)
        quant_process.execute(idx)

        current_status = quant_process.get_status()
        if current_status != EXIT_SUCCESS:
            status = current_status
            log.error(f'Quantization finished with non-zero code: {current_status}')
        else:
            log.info('End quantization model #{0}!'.format(idx + 1))

    return status


if __name__ == '__main__':
    sys.excepthook = exception_hook

    args = cli_argument_parser()

    parser = ConfigParser(args.config_path)

    log.info('Start parsing the configuration on the path: {0}!'.format(args.config_path))
    quantization_parameters = parser.parse()
    log.info('Parsing done!')

    log.info(f'Start quantization of {len(quantization_parameters)} models\n')
    return_code = quantization(args.executor_type, quantization_parameters, log)
    log.info('Quantization completed' if not return_code else 'Quantization failed')

    parser.clean()
    sys.exit(return_code)
