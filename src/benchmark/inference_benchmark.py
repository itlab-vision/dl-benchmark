import os
import sys
import argparse
import config_parser
import inference
import postprocessing_data as pp
import output
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

def inference_benchmark(test_list):
    table = []
    for i in range(len(test_list)):
        mode = (test_list[i].parameter.mode).lower()
        latency = None
        fps = None
        average_time = None
        if mode == 'sync':
            inference_time = inference.test_sync(test_list[i].model, 
                test_list[i].dataset, test_list[i].parameter)
            inference_time = pp.delete_incorrect_time(inference_time,
                test_list[i].parameter.min_inference_time)
            inference_time = pp.three_sigma_rule(inference_time)
            average_time = pp.calculate_average_time(inference_time)
            latency = pp.calculate_latency(inference_time)
            fps = pp.calculate_fps(latency)
        if mode == 'async':
            inference_time = inference.test_async(test_list[i].model,
                test_list[i].dataset, test_list[i].parameter)
            average_time = inference_time
            fps = pp.calculate_fps(inference_time)
        table_row = output.create_table_row(test_list[i].model, test_list[i].dataset,
            test_list[i].parameter, average_time, latency, fps)
        table.append(table_row)
    return table

if __name__ == '__main__':
    try:
        log.basicConfig(format = '[ %(levelname)s ] %(message)s',
            level = log.INFO, stream = sys.stdout)
        config, result_file = build_parser()
        test_list = config_parser.process_config(config)
        log.info('Start inference tests on {} models'.format(len(test_list)))
        table = inference_benchmark(test_list)
        log.info('End inference tests')
        log.info('Saving data in file')
        output.save_table(table, result_file)
        log.info('Work is done!')
    except Exception as exp:
        log.warning(str(exp))