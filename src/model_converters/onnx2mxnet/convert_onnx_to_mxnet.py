import argparse
import os
import shutil
import sys
import traceback

import mxnet as mx
from mxnet.contrib.onnx.onnx2mx.import_model import import_model

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))  # noqa: E402
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


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
    log.info('Starting model conversion...')
    sym, arg, aux = import_model(args.model)
    mx.model.save_checkpoint(f'{args.model_name}', 0, sym, arg, aux)
    log.info('Model successfully converted.')

    log.info('Saving model...')
    if args.path_save_model is not None:
        move_files(args)
    log.info('Model successfully saved.')


def move_files(args: argparse.Namespace):
    if not os.path.exists(args.path_save_model):
        os.makedirs(args.path_save_model, exist_ok=True)
    else:
        symbol_path = os.path.join(args.path_save_model, f'{args.model_name}-symbol.json')
        params_path = os.path.join(args.path_save_model, f'{args.model_name}-0000.params')

        if os.path.exists(symbol_path):
            os.remove(symbol_path)

        if os.path.exists(params_path):
            os.remove(params_path)

    shutil.move(f'{args.model_name}-symbol.json', args.path_save_model)
    shutil.move(f'{args.model_name}-0000.params', args.path_save_model)


def main():
    args = cli_argument_parser()
    try:
        convert_model(args)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
