import argparse
import sys
import importlib
import abc
import json
import traceback
from pathlib import Path
from xml.etree import ElementTree as ET
from config_parser import TVMQuantizationConfigParser
from parameters import TVMModelReader
sys.path.append(str(Path(__file__).resolve().parents[2]))
from utils.logger_conf import configure_logger  # noqa: E402

log = configure_logger()


#class Dataset(metaclass=abc.ABCMeta):
#    def __init__(self, args):
#        self.tvm = importlib.import_module('tvm')
#        self.link = args['link']
#    
#    #@abc.abstractmethod
#    def download_dataset(self):
#        rec_file = self.tvm.contrib.download.download_testdata("http://data.mxnet.io.s3-website-us-west-1.amazonaws.com/data/val_256_q90.rec",
#                                                               "val_256_q90.rec",)
#        print(rec_file)
#    #@abc.abstractmethod
#    def get_val_data(self):
#        pass
    


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-mn', '--model_name',
    #                    help='Model name.',
    #                    type=str,
    #                    required=True,
    #                    dest='model_name')
    #parser.add_argument('-m', '--model',
    #                    help='Path to an .json, .onnx, .pt, .prototxt file with a trained model.',
    #                    type=str,
    #                    dest='model_path')
    #parser.add_argument('-w', '--weights',
    #                    help='Path to an .params, .caffemodel, .pth file with a trained weights.',
    #                    type=str,
    #                    dest='model_params')
    #parser.add_argument('-mm', '--module',
    #                    help='Module with model architecture.',
    #                    default='torchvision.models',
    #                    type=str,
    #                    dest='module')
    #parser.add_argument('-is', '--input_shape',
    #                    help='Input shape BxWxHxC, B is a batch size,'
    #                         'W is an input tensor width,'
    #                         'H is an input tensor height,'
    #                         'C is an input tensor number of channels.',
    #                    required=True,
    #                    type=int,
    #                    nargs=4,
    #                    dest='input_shape')
    #parser.add_argument('-f', '--source_framework',
    #                    help='Source model framework',
    #                    default='tvm',
    #                    type=str,
    #                    dest='source_framework')
    #parser.add_argument('-b', '--batch_size',
    #                    help='Batch size.',
    #                    default=1,
    #                    type=int,
    #                    dest='batch_size')
    #parser.add_argument('-in', '--input_name',
    #                    help='Input name.',
    #                    default='data',
    #                    type=str,
    #                    dest='input_name')
    #parser.add_argument('-d', '--device',
    #                    help='Specify the target device to infer (CPU by default)',
    #                    default='CPU',
    #                    type=str,
    #                    dest='device')
    #parser.add_argument('-op', '--output_dir',
    #                    help='Path to save the model.',
    #                    default=None,
    #                    type=str,
    #                    dest='output_dir')
    args = parser.parse_args()
    return args


def create_dict_for_converter(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'device': args.device,
        'module': args.module,
        'output_dir': args.output_dir,
        'source_framework': args.source_framework,
    }
    return dictionary


def main():
    args = cli_argument_parser()
    try:
        f = TVMQuantizationConfigParser('config.xml')
        reader = TVMModelReader(log)
        r = f.parse()
        print(r[0][0])
        reader.add_arguments(r[0][0]['Model'])
        print(reader.model_path)
        #f = ET.parse('/home/vanya/projects/dl-benchmark/src/config.xml')
        #a = f.getroot()
        #for elem in a:
        #    for subelem in elem:
        #        print(subelem.tag)
        #        for subbb in subelem:
        #            print(subbb.tag)
        #            print(subbb.text)
    
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
