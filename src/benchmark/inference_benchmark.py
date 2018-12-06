import os
import argparse
import config_parser
import inference

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'path_to_config',
        help = 'Path to configuration file')
    config = parser.parse_args().path_to_config

    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')

    return config

def inference_benchmark(test_list):
    for i in range(len(test_list)):
        mode = (test_list[i].parameter.mode).lower()
        if mode == 'sync':
            inference_time = inference.test_sync(test_list[i].model, 
                test_list[i].dataset, test_list[i].parameter)
        else:
            inference_time = inference.test_async(test_list[i].model,
                test_list[i].dataset, test_list[i].parameter)

    return inference_time
    
if __name__ == "__main__":
    try:
        config = build_parser()
        test_list = config_parser.process_config(config)
        output = inference_benchmark(test_list)
    except Exception as exp:
        print('Error! : {}'.format(str(exp)))