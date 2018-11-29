import argparse
import readconfig as rc
     
def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'path_to_config',
        help = 'Path to file with config')
    
    config = parser.parse_args().path_to_config
	
    if not os.path.isfile(config):
        raise ValueError('Wrong path to file!')
    
    return config

def test_inference(test_list):
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
    except Exception as Error:
        print('Error! : {}'.format(str(Error)))
    test_list = rc.process_config(config)
    output = test_inference(test_list)