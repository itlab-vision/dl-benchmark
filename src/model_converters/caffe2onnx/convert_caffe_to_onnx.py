import subprocess
import argparse
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))  # noqa: E402
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pt', '--prototxt',
                        help='The path to the prototxt file',
                        type=str,
                        default=None,
                        dest='path_to_prototxt')
    parser.add_argument('-w', '--weights',
                        help='The path to the caffemodel file',
                        type=str,
                        default=None,
                        dest='weights')
    parser.add_argument('-od', '--output_dir',
                        help='The path to the folder with the output weights',
                        default='./converted_models',
                        type=str,
                        dest='output_dir')
    args = parser.parse_args()
    return args


def call_caffe_to_onnx_converter(path_to_caffe_proto_file, path_to_caffe_weight_file, onnx_file_name):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_script_dir, 'caffe2onnx', 'caffe2onnx', 'convert.py')
    command = [
        'python', script_path,
        '--prototxt', path_to_caffe_proto_file,
        '--caffemodel', path_to_caffe_weight_file,
        '--onnx', onnx_file_name,
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.info(result.stdout)
        if result.stderr:
            raise ValueError(f'{result.stderr}')
    except subprocess.CalledProcessError as e:
        raise ValueError(f'{e}\nSTDOUT:{e.stdout}\nSTDERR:{e.stderr}')


if __name__ == '__main__':
    args = cli_argument_parser()
    exitPath = args.output_dir
    if not (os.path.exists(args.output_dir)):
        os.makedirs(args.output_dir)
    try:
        model_name = (re.split('/|\\\\', args.path_to_prototxt)[-1]).split('.')[-2]
        call_caffe_to_onnx_converter(
            args.path_to_prototxt, args.weights,
            os.path.join(args.output_dir, f'{model_name}.onnx'),
        )
    except ValueError as e:
        log.error(e)
