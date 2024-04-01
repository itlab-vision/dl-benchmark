import argparse
import os
import shutil
import sys

import mxnet as mx
from mxnet.contrib.onnx.onnx2mx.import_model import import_model

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from logger_conf import configure_logger

logger = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .onnx file with a trained model.',
                        type=str,
                        dest='model')
    parser.add_argument('-mn', '--model_name',
                        help='Model name.',
                        type=str,
                        default='model',
                        dest='model_name')
    parser.add_argument('-p', '--path_save_model',
                        help='Path to save model',
                        type=str,
                        default=None,
                        dest='path_save_model')

    args = parser.parse_args()

    return args


def convert_model(args: argparse.Namespace):
    try:
        logger.info('Starting model conversion...')
        sym, arg, aux = import_model(args.model)
        mx.model.save_checkpoint(f'{args.model_name}', 0, sym, arg, aux)
        logger.info('Model successfully converted.')

        if args.path_save_model is not None:
            move_files(args)
        logger.info('Model successfully saved.')
    except Exception as e:
        logger.error(f'Error occurred during model conversion: {e}')


def move_files(args: argparse.Namespace):
    try:
        if not os.path.exists(args.path_save_model):
            os.makedirs(args.path_save_model, exist_ok=True)

        shutil.move(f'{args.model_name}-symbol.json', args.path_save_model)
        shutil.move(f'{args.model_name}-0000.params', args.path_save_model)
    except Exception as e:
        logger.error(f'Error occurred while moving files: {e}')


def main():
    args = cli_argument_parser()
    convert_model(args)


if __name__ == '__main__':
    main()
