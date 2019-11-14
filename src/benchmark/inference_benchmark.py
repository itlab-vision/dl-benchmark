import os
import sys
import utils
import output
import argparse
import config_parser
import logging as log


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'config_path',
        help = 'Path to configuration file', required = True)
    parser.add_argument('-f', '--filename', type = str, dest = 'result_file',
        help = 'Full name of the resulting file', required = True)
    config = parser.parse_args().config_path
    result = parser.parse_args().result_file
    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')
    return config, result


def inference_benchmark(test_list, result_table, log):
    environment = os.environ.copy()
    for i in range(len(test_list)):
        framework = 'OpenVINO DLDT'
        test = test_list[i]
        mode = (test.parameter.mode).lower()
        test_status = 'Passed'
        latency = None
        fps = None
        average_time = None
        if mode == 'sync':
            log.info('Start sync inference test on model : {}'.format(test.model.name))
            command_line = utils.create_cmd_line_for_sync_test(test.model.model, 
                test.model.weight, test.dataset.path, test.parameter.batch_size,
                test.parameter.device, test.parameter.extension, test.parameter.iteration,
                test.parameter.nthreads, test.parameter.min_inference_time)
            return_code, out = utils.run_test(command_line, environment)
            input_shape = utils.parse_model_input_shape(out)
            if return_code == 0:
                log.info('End sync inference test on model : {}'.format(test.model.name))
                average_time, fps, latency = utils.parse_sync_output(out)
            else:
                log.warning('Sync inference test on model: {} was ended with error:'.format(test.model.name))
                test_status = 'Failed'
                utils.print_error(out)
        if mode == 'async':
            log.info('Start async inference test on model : {}'.format(test.model.name))
            command_line = utils.create_cmd_line_for_async_test(test.model.model, 
                test.model.weight, test.dataset.path, test.parameter.batch_size,
                test.parameter.device, test.parameter.extension, test.parameter.iteration,
                test.parameter.nthreads, test.parameter.nstreams, test.parameter.async_request)
            return_code, out = utils.run_test(command_line, environment)
            input_shape = utils.parse_model_input_shape(out)
            if return_code == 0:
                log.info('End async inference test on model : {}'.format(test.model.name))
                average_time, fps = utils.parse_async_output(out)
            else:
                log.warning('Async inference test on model: {} was ended with error. Process logs:'.format(test.model.name))
                test_status = 'Failed'
                utils.print_error(out)
        log.info('Saving test result in file')
        table_row = output.create_table_row(test_status, test.model, test.dataset, 
            test.parameter, framework, input_shape, average_time, latency, fps)
        output.add_row_to_table(result_table, table_row)


if __name__ == '__main__':
    try:
        log.basicConfig(format = '[ %(levelname)s ] %(message)s',
            level = log.INFO, stream = sys.stdout)
        config, result_table = build_parser()
        test_list = config_parser.process_config(config, log)
        log.info('Create result table with name: {}'.format(result_table))
        output.create_table(result_table)
        log.info('Start {} inference tests'.format(len(test_list)))
        inference_benchmark(test_list, result_table, log)
        log.info('End inference tests')
        log.info('Work is done!')
    except Exception as exp:
        log.error(str(exp))