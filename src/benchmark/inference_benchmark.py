import os
import sys
import argparse
import config_parser
import inference
import postprocessing_data as pp
import output
import logging as log
import subprocess


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


def inference_benchmark(test_list):
    table = []
    for i in range(len(test_list)):
        mode = (test_list[i].parameter.mode).lower()
        latency = None
        fps = None
        average_time = None
        inference_folder = os.path.normpath('../inference')
        if mode == 'sync':
            cmd_line = 'python {}/inference_sync_mode.py -m {} -w {} -i {} \
                -b {} -d {} -ni {} -mi {} --raw_output true'.format(inference_folder,
                        test_list[i].model.model, test_list[i].model.weight,
                    test_list[i].dataset.path, test_list[i].parameter.batch_size,
                    test_list[i].parameter.plugin, test_list[i].parameter.iteration,
                    test_list[i].parameter.min_inference_time)
            test = subprocess.Popen(cmd_line, shell = True,
                stdout = subprocess.PIPE, universal_newlines = True)
            test.wait()
            if not test.poll():
                continue
            lastline = ''
            for line in test.stdout:
                lastline = line
            result = lastline.split(',')
            average_time = float(result[0])
            fps = float(result[1])
            latency = float(result[2])
        if mode == 'async':
            cmd_line = 'python {}/inference_async_mode.py -m {} -w {} -i {} \
                -b {} -d {} -ni {} -r {} --raw_output true'.format(inference_folder,
                        test_list[i].model.model, test_list[i].model.weight,
                    test_list[i].dataset.path, test_list[i].parameter.batch_size,
                    test_list[i].parameter.plugin, test_list[i].parameter.iteration,
                    test_list[i].parameter.async_request)
            test = subprocess.Popen(cmd_line, shell = True,
                stdout = subprocess.PIPE, universal_newlines = True)
            test.wait()
            if not test.poll():
                continue
            lastline = ''
            for line in test.stdout:
                lastline = line
            result = lastline.split(',')
            average_time = float(result[0])
            fps = float(result[1])
        table_row = output.create_table_row(test_list[i].model,
            test_list[i].dataset, test_list[i].parameter, average_time,
            latency, fps)
        table.append(table_row)
    return table


if __name__ == '__main__':
    try:
        log.basicConfig(format = '[ %(levelname)s ] %(message)s',
            level = log.INFO, stream = sys.stdout)
        config, result_file = build_parser()
        test_list = config_parser.process_config(config)
        log.info('Start {} inference tests'.format(len(test_list)))
        table = inference_benchmark(test_list)
        log.info('End inference tests')
        log.info('Saving data in file')
        output.save_table(table, result_file)
        log.info('Work is done!')
    except Exception as exp:
        log.warning(str(exp))