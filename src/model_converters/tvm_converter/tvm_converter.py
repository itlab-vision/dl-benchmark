import argparse
import sys
import traceback
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath('tvm_auxiliary')))
from converter import TVMConverter  # noqa: E402

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from utils.logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name',
                        help='Model name.',
                        type=str,
                        required=True,
                        dest='model_name')
    parser.add_argument('-m', '--model',
                        help='Path to an .json, .onnx, .pt, .prototxt file with a trained model.',
                        type=str,
                        dest='model_path')
    parser.add_argument('-w', '--weights',
                        help='Path to an .params, .caffemodel, .pth file with a trained weights.',
                        type=str,
                        dest='model_params')
    parser.add_argument('-mm', '--module',
                        help='Module with model architecture.',
                        default='torchvision.models',
                        type=str,
                        dest='module')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, B is a batch size,'
                             'W is an input tensor width,'
                             'H is an input tensor height,'
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('-f', '--source_framework',
                        help='Source model framework',
                        default='tvm',
                        type=str,
                        dest='source_framework')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('-op', '--output_dir',
                        help='Path to save the model.',
                        default=None,
                        type=str,
                        dest='output_dir')
    parser.add_argument('--high_level_ir',
                        help='Type of high lever Intermediate Representation (IR)',
                        choices=['relay', 'relax'],
                        default='relay',
                        type=str,
                        dest='high_level_ir')
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
        'high_level_ir': args.high_level_ir,
    }
    return dictionary


def main():
    args = cli_argument_parser()
    try:
        converter = TVMConverter.get_converter(create_dict_for_converter(args))
        converter.get_tvm_model()
        converter.save_tvm_model()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
