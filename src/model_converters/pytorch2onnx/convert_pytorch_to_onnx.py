import argparse
import sys

import model_converter
import torchvision.models as models
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))  # noqa: E402
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def parse_input_shape(value, count):
    stripped_value = value.strip('[] ')
    try:
        nums = [int(item) for item in stripped_value.split(',')]
        if len(nums) != count:
            raise argparse.ArgumentTypeError(f'The length should be {count}')
        return nums
    except ValueError:
        errStr = ': '.join(['int'] * count)
        raise argparse.ArgumentTypeError(
            f'The parameter must be in the format [{errStr}]')


def get_model_by_name(model_name):
    try:
        model_constructor = getattr(models, model_name)
        model = model_constructor()
        return model
    except AttributeError:
        raise ValueError(f'Model {model_name} is not found in torchvision.models')


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-mn', '--model_name',
                        help='Name of model',
                        type=str,
                        default=None,
                        dest='model_name')

    parser.add_argument('-w', '--weights',
                        help='Path to file with format .pth with weights of PyTorch model',
                        type=str,
                        default=None,
                        dest='weights')

    parser.add_argument('-b', '--batch_size',
                        help='Batch size',
                        default=1,
                        type=int,
                        dest='batch_size')

    parser.add_argument('-is', '--input_size',
                        help='Dimensions of the input image',
                        default=None,
                        type=str,
                        dest='input_size')

    parser.add_argument('-ch', '--channels',
                        help='Number of channels',
                        default=3,
                        type=int,
                        dest='channels_size')

    parser.add_argument('-od', '--output_dir',
                        help='The path to the folder with the output weights',
                        default='./converted_models',
                        type=str,
                        dest='output_dir')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = cli_argument_parser()
    exitPath = args.output_dir
    if not (os.path.exists(args.output_dir)):
        os.makedirs(args.output_dir)

    try:
        torch_model = get_model_by_name(args.model_name)
        nums = parse_input_shape(args.input_size, 2)

        converter = model_converter.Converter(
            save_dir=f'{args.output_dir}',
            simplify_exported_model=False,
        )

        converted_model = converter.convert(
            torch_model=torch_model,
            batch_size=args.batch_size,
            input_size=nums,
            channels=args.channels_size,
            fmt='onnx',
            force=True,
            torch_weights=args.weights,
        )

        os.rename(f'{args.output_dir}/model.onnx', f'{args.output_dir}/{args.model_name}.onnx')
        log.info(f'The model was saved in {args.output_dir}/{args.model_name}.onnx')
    except ValueError as e:
        log.error(e)
