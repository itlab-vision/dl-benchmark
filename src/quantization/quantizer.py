import os
import sys
import json
import argparse
import cv2 as cv
import numpy as np
from addict import Dict
from compression.graph import load_model, save_model
from compression.engines.ie_engine import IEEngine
from compression.pipeline.initializer import create_pipeline
from data_loader import DatasetsDataLoader


def parse_json(config_file_name):
    return json.load(open(config_file_name, 'r'))


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', help='Path to a configuration file with a configurations for quantizing model.', required=True, type=str, dest='config')
    parser.add_argument('-q', '--quantized_model_dir', default="./quantized_models", help='Path to a directory for quantized model.', type=str, dest='quant_dir')
    return parser


def main():
    args = build_argparser().parse_args()
    configs = Dict(parse_json(args.config))
    try:
        for model_config in configs['models']:
            data_loader = DatasetsDataLoader(model_config['dataset'])

            model = load_model(Dict(model_config['model']))
            engine = IEEngine(model_config['engine_config'], data_loader)
            pipeline = create_pipeline(model_config['algorithms'], engine)
            quantized_model = pipeline.run(model)

            quantized_model_name = quantized_model.models[0]['model'].name
            q_model_path = os.path.join(args.quant_dir, quantized_model_name)
            save_model(quantized_model, q_model_path)
            
            print('Quantized model {0} was saved to {1}'.format(quantized_model_name, q_model_path))
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)