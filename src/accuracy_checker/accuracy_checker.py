import argparse
import logging as log
import sys
from pathlib import Path

from config_parser import TestResultParser
from executors import Executor
from output import OutputHandler
from parameters import Parameters
from process import ProcessHandler

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger, exception_hook  # noqa: E402

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


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
        '--csv_delimiter',
        metavar='CHARACTER',
        type=str,
        help='Delimiter to use in the resulting file',
        default=';')
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

    if not Path(args.config_path).is_file():
        raise ValueError('Wrong path to configuration file!')

    return args


def accuracy_check(executor_type, test_list, output_handler, log):
    status = EXIT_SUCCESS

    try:
        process_executor = Executor.get_executor(executor_type, log)
    except ValueError as ex:
        log.error(ex, exc_info=True)
        return EXIT_FAILURE
    process_executor.prepare_executor(test_list)

    for idx, test in enumerate(test_list):
        test_process = ProcessHandler(log, process_executor, test)
        test_process.execute(idx)

        log.info('Saving test result in file\n')
        output_handler.add_results(test, test_process, process_executor)

        current_status = test_process.get_status()
        if current_status != EXIT_SUCCESS:
            status = current_status
            log.error(f'Test finished with non-zero code: {current_status}')
    return status


if __name__ == '__main__':
    configure_logger()
    sys.excepthook = exception_hook

    args = cli_argument_parser()
    test_parameters = Parameters(args.source_path, args.annotations_path, args.definitions_path,
                                 args.extensions_path)
    test_list = TestResultParser.get_test_list(args.config_path, test_parameters)

    log.info(f'Create result table with name: {args.result_file}')

    output_handler = OutputHandler(args.result_file, args.csv_delimiter)
    output_handler.create_table()

    log.info(f'Start {len(test_list)} accuracy tests\n')

    return_code = accuracy_check(args.executor_type, test_list, output_handler, log)
    log.info('Accuracy tests completed' if not return_code else 'Accuracy tests failed')
    sys.exit(return_code)
