import os
import sys
import argparse
import config_parser
import output
import logging as log
import subprocess
import platform


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
    inference_folder = os.path.normpath('../inference')
    inference_async_scrypt = os.path.join(inference_folder, 'inference_async_mode.py')
    inference_sync_scrypt = os.path.join(inference_folder, 'inference_sync_mode.py')
    python_type = ''
    os_type = platform.system()
    if os_type == 'Windows':
        python_type = 'python'
    elif os_type == 'Linux':
        python_type = 'python3'
    else:
        raise ValueError('OS type not supported')
    environment = os.environ.copy()
    for i in range(len(test_list)):
        mode = (test_list[i].parameter.mode).lower()
        latency = None
        fps = None
        average_time = None
        if mode == 'sync':
            log.info('Start sync inference test on model : {}'.format(test_list[i].model.name))
            cmd_line = '{} {} -m {} -w {} -i {} -b {} -d {} -ni {} \
                -mi {} --raw_output true'.format(python_type, inference_sync_scrypt,
                    test_list[i].model.model, test_list[i].model.weight,
                    test_list[i].dataset.path, test_list[i].parameter.batch_size,
                    test_list[i].parameter.plugin, test_list[i].parameter.iteration,
                    test_list[i].parameter.min_inference_time)
            if (test_list[i].parameter.nthreads != 'None'):
                cmd_line += ' -nthreads {}'.format(test_list[i].parameter.nthreads)
            test = subprocess.Popen(cmd_line, env = environment, shell = True,
                stdout = subprocess.PIPE, universal_newlines = True)
            test.wait()
            if test.poll():
                log.warning('Sync inference test on model: {} was ended with error. Process logs:'.format(test_list[i].model.name))
                for line in test.stdout:
                    print('    {}'.format(line), end = '')
                continue
            log.info('End sync inference test on model : {}'.format(test_list[i].model.name))
            lastline = ''
            for line in test.stdout:
                lastline = line
            result = lastline.split(',')
            average_time = float(result[0])
            fps = float(result[1])
            latency = float(result[2])
        if mode == 'async':
            log.info('Start async inference test on model : {}'.format(test_list[i].model.name))
            cmd_line = '{} {} -m {} -w {} -i {} -b {} -d {} -ni {} \
                -r {} --raw_output true'.format(python_type, inference_async_scrypt,
                    test_list[i].model.model, test_list[i].model.weight,
                    test_list[i].dataset.path, test_list[i].parameter.batch_size,
                    test_list[i].parameter.plugin, test_list[i].parameter.iteration,
                    test_list[i].parameter.async_request)
            if (test_list[i].parameter.nthreads != 'None'):
                cmd_line += ' -nthreads {}'.format(test_list[i].parameter.nthreads)
            test = subprocess.Popen(cmd_line, env = environment, shell = True,
                stdout = subprocess.PIPE, universal_newlines = True)
            test.wait()
            if test.poll():
                log.warning('Async inference test on model: {} was ended with error. Process logs:'.format(test_list[i].model.name))
                for line in test.stdout:
                    print('    {}'.format(line), end = '')
                continue
            log.info('End sync inference test on model : {}'.format(test_list[i].model.name))
            lastline = ''
            for line in test.stdout:
                lastline = line
            result = lastline.split(',')
            average_time = float(result[0])
            fps = float(result[1])
        log.info('Saving test result in file')
        table_row = output.create_table_row(test_list[i].model,
            test_list[i].dataset, test_list[i].parameter, average_time,
            latency, fps)
        output.add_row_to_table(result_table, table_row)


if __name__ == '__main__':
    try:
        log.basicConfig(format = '[ %(levelname)s ] %(message)s',
            level = log.INFO, stream = sys.stdout)
        config, result_table = build_parser()
        test_list = config_parser.process_config(config)
        log.info('Create result table with name: {}'.format(result_table))
        output.create_table(result_table)
        log.info('Start {} inference tests'.format(len(test_list)))
        table = inference_benchmark(test_list, result_table, log)
        log.info('End inference tests')
        log.info('Work is done!')
    except Exception as exp:
        log.warning(str(exp))