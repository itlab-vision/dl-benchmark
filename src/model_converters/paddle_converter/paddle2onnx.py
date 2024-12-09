import argparse
import logging as log
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--model_dir',
                        help='Directory to save model in.',
                        required=True,
                        type=str,
                        dest='model_dir')
    parser.add_argument('-f', '--model_filename',
                        help='Name of the model file name.',
                        required=True,
                        type=str,
                        dest='model_filename')
    parser.add_argument('-p', '--params_filename',
                        help='Name of the parameters file name.',
                        required=True,
                        type=str,
                        dest='params_filename')
    parser.add_argument('-m', '--model_path',
                        help='Path to an .onnx file.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-o', '--opset_version',
                        help='',
                        required=True,
                        type=str,
                        dest='opset_version')
    args = parser.parse_args()

    return args


def convert_paddle_to_onnx(model_dir: str, model_filename: str, params_filename: str,
                           model_path: str, opset_version: str):
    os.system(f"""paddle2onnx --model_dir {model_dir} --model_filename {model_filename}
    --params_filename {params_filename}
    --save_file {model_path}
    --opset_version {opset_version}
    --enable_onnx_checker True""")


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = cli_argument_parser()
    convert_paddle_to_onnx(model_dir=args.model_dir, model_filename=args.model_filename,
                           params_filename=args.params_filename, model_path=args.model_path,
                           opset_version=args.opset_version)


if __name__ == '__main__':
    main()
