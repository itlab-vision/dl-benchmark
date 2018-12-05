import argparse
import os
import config_parser

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'path_to_config',
        help = 'Path to configuration file')
    config = parser.parse_args().path_to_config

    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')

    return config

def inference_benchmark(test_list):
    output_data = []
    for i in range(len(test_list)):
        if ((test_list[i].parameters.mode).lower()) == 'sync':
            #call sync test
            output_data.append([])
        else:
            #call async test
            output_data.append([])
        
    return output_data
    
if __name__ == "__main__":
    try:
        config = build_parser()
        test_list = config_parser.process_config(config)
        output = inference_benchmark(test_list)
    except Exception as Error:
        print('Error! : {}'.format(str(Error)))