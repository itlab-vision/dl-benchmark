import os
import argparse
import config_parser
import inference
import output

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'path_to_config',
        help = 'Path to configuration file')
    config = parser.parse_args().path_to_config

    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')

    return config

def inference_benchmark(test_list):
    table = []
    for i in range(len(test_list)):
        mode = (test_list[i].parameter.mode).lower()
        latency = None
        fps = None
        time = None
        average_time = None
        
        if mode == 'sync':
            inference_time = inference.test_sync(test_list[i].model, 
                test_list[i].dataset, test_list[i].parameter)
            #postprocessing time
            #Latency
            #FPS
        
        if mode == 'async':
            inference_time = inference.test_async(test_list[i].model,
                test_list[i].dataset, test_list[i].parameter)
            average_time = inference_time
            #FPS

        table_row = output.create_table_row(test_list[i].model, test_list[i].dataset,
            test_list[i].parameter, average_time, latency, fps)
        table.append(table_row)
    return table
    
if __name__ == "__main__":
    try:
        config = build_parser()
        test_list = config_parser.process_config(config)
        table = inference_benchmark(test_list)
        output.save_table_in_file(table)
    except Exception as exp:
        print('Error! : {}'.format(str(exp)))