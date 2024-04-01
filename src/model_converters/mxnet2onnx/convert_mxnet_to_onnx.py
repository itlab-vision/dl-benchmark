import argparse
import os
import sys

from mxnet.onnx import export_model

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from logger_conf import configure_logger

logger = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .json file with a trained model.',
                        type=str,
                        dest='model_json')
    parser.add_argument('-w', '--weights',
                        help='Path to an .params file with a trained weights.',
                        type=str,
                        dest='model_params')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, '
                             'B is a batch size, '
                             'W is an input tensor width, '
                             'H is an input tensor height, '
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('-p', '--path_save_model',
                        help='Path to save model',
                        type=str,
                        default='model.onnx',
                        dest='path_save_model')

    args = parser.parse_args()

    return args


def convert_model(args):
    try:
        logger.info('Starting model conversion...')
        export_model(
            sym=args.model_json,
            params=args.model_params,
            in_shapes=[tuple(args.input_shape)],
            onnx_file_path=args.path_save_model
        )
        logger.info(f'Model successfully converted and saved.')
    except Exception as e:
        logger.error(f'Error occurred during model conversion to ONNX format: {e}')


def main():
    args = cli_argument_parser()
    convert_model(args)


if __name__ == '__main__':
    main()
