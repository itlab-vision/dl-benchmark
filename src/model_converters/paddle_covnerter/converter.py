import torch
import numpy as np
from torchvision.models import (AlexNet, VGG, ResNet, SqueezeNet, DenseNet,
                                Inception3, GoogLeNet, ShuffleNetV2, MobileNetV2, MobileNetV3, MNASNet)
from x2paddle.convert import pytorch2paddle
import argparse
import logging as log
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model_path',
                        help='Path to an .onnx or .pth file.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-f', '--framework',
                        help='Original model framework (ONNX or Pytorch)',
                        required=True,
                        type=str,
                        choices=['onnx', 'pytorch'],
                        dest='framework')
    parser.add_argument('-p', '--pytorch_module_name',
                        help='Module name for PyTorch model.',
                        required=False,
                        type=str,
                        choices=['AlexNet', 'VGG', 'ResNet', 'SqueezeNet', 'DenseNet', 'InceptionV3', 'GoogLeNet',
                                 'ShuffleNetV2', 'MobileNetV2', 'MobileNetV3', 'MNASNet'],
                        dest='module_name')
    parser.add_argument('-d', '--save_dir',
                        help='Directory for converted model to be saved to.',
                        required=True,
                        type=str,
                        dest='save_dir')
    args = parser.parse_args()

    return args


def convert_pytorch_to_paddle(model_path: str, module_name, save_dir: str):

    modules = {'AlexNet': AlexNet,
               'VGG': VGG,
               'ResNet': ResNet,
               'SqueezeNet': SqueezeNet,
               'DenseNet': DenseNet,
               'InceptionV3': Inception3,
               'GoogLeNet': GoogLeNet,
               'ShuffleNetV2': ShuffleNetV2,
               'MobileNetV2': MobileNetV2,
               'MobileNetV3': MobileNetV3,
               'MNASNet': MNASNet}

    torch_module = modules[module_name]()
    torch_module.load_state_dict(torch.load(model_path))
    torch_module.eval()

    input_data = np.random.rand(1, 3, 224, 224).astype('float32')
    pytorch2paddle(torch_module,
                   save_dir=save_dir,
                   jit_type='trace',
                   input_examples=[torch.tensor(input_data)])


def convert_onnx_to_paddle(model_path: str, save_dir: str):
    print(f'x2paddle --framework=onnx --model={model_path} --save_dir={save_dir}')
    os.system(f'x2paddle --framework=onnx --model={model_path} --save_dir={save_dir}')


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = cli_argument_parser()
    if args.framework == 'pytorch' and not args.module_name:
        raise ValueError('Module name for pytorch is not specified')
    elif args.framework == 'pytorch' and args.module_name:
        convert_pytorch_to_paddle(model_path=args.model_path,
                                  module_name=args.module_name, save_dir=args.save_dir)
    elif args.framework == 'onnx':
        convert_onnx_to_paddle(model_path=args.model_path, save_dir=args.save_dir)


if __name__ == '__main__':
    main()
