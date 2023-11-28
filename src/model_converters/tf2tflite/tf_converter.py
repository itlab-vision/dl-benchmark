import argparse
import logging as log
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.model_converters.tf2tflite.tensorflow_common import (load_model, convert_with_tensor_rt, is_gpu_available,  # noqa
                                                    get_input_operation_name)  # noqa


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model_path',
                        help='Path to an .pb or .meta file, or saved model dir with a trained model.',
                        required=True,
                        type=Path,
                        dest='model_path')
    parser.add_argument('--input_name',
                        help='Input tensor names.',
                        default=None,
                        type=str,
                        nargs=1,
                        dest='input_name')
    parser.add_argument('--output_names',
                        help='Output tensor names.',
                        default=False,
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('--saved_model_dir',
                        help='A path where tf2 saved model will be saved.',
                        required=False,
                        default='auto',
                        type=str,
                        dest='saved_model_dir')
    parser.add_argument('--tensor_rt_precision',
                        help='TensorRT precision FP16, FP32. If not defined, no TensorRT conversion will be applied.'
                             ' Applicable only for hosts with NVIDIA GPU and tensorflow built with TensorRT support.',
                        type=str,
                        default=None,
                        dest='tensor_rt_precision')
    parser.add_argument('--tensor_rt_model_dir',
                        help='A path where TensorRT optimized model will be saved.',
                        required=False,
                        default='auto',
                        type=str,
                        dest='tensor_rt_model_dir')
    args = parser.parse_args()

    return args


def convert_to_saved_model(model_path: Path, input_op_name: list, output_names: str, saved_model_dir='auto'):
    _, saved_model_dir = load_model(Path(model_path), input_op_name, output_names, [], log,
                                    saved_model_dir=saved_model_dir)
    return saved_model_dir


def convert_saved_model_with_tensor_rt(saved_model_dir, tensor_rt_precision=None, tensor_rt_converted_path='auto'):
    if tensor_rt_precision is not None:
        if not is_gpu_available():
            errmsg = 'No NVIDIA_GPU detected on hostmachine, TensorRT conversion impossible'
            log.error(errmsg)
            raise AssertionError(errmsg)

        if tensor_rt_converted_path == 'auto':
            converted_model_dir = Path(saved_model_dir).parent / f'tensor_rt_{tensor_rt_precision}'
        else:
            converted_model_dir = tensor_rt_converted_path
        convert_with_tensor_rt(saved_model_dir, output_model_dir=str(converted_model_dir), log=log,
                               precision=tensor_rt_precision)
    else:
        log.warning('Provided TensorRT precision is None, nothing to convert')


def convert_model_to_tf2_format(model_path: Path,
                                input_name, output_names,
                                converted_model_path='auto',
                                tensor_rt_precision=None,
                                tensor_rt_converted_path='auto'):
    input_op_name = get_input_operation_name(input_name)
    saved_model_dir = convert_to_saved_model(model_path, input_op_name=input_op_name,
                                             output_names=output_names, saved_model_dir=converted_model_path)
    convert_saved_model_with_tensor_rt(saved_model_dir, tensor_rt_precision, tensor_rt_converted_path)


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = cli_argument_parser()
    convert_model_to_tf2_format(model_path=Path(args.model_path), input_name=args.input_name,
                                output_names=args.output_names, converted_model_path=args.saved_model_dir,
                                tensor_rt_precision=args.tensor_rt_precision,
                                tensor_rt_converted_path=args.tensor_rt_model_dir)


if __name__ == '__main__':
    main()
