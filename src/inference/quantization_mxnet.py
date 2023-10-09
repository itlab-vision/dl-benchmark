import sys
import argparse
import logging as log
import mxnet
import os
from mxnet.contrib.quantization import quantize_net_v2
from mxnet_auxiliary import (create_dict_for_quantwrapper, get_device,
                             load_network_gluon, load_network_gluon_model_zoo)


class QuantWrapper:
    def __init__(self, args):
        self._calib_mode = args['calib_mode']
        self._quant_dtype = args['quant_dtype']
        self._input_shape = args['input_shape']
        self._model_name = args['model_name']
        self._model_json = args['model_json']
        self._input_name = args['input_name']
        self._weights = args['model_params']
        self._quant_mode = args['quant_mode']
        self.quantized_net = None

    def quant_gluon_model(self, net, context):
        data = [[mxnet.nd.ones([1, *self._input_shape])]]
        quantized_net = quantize_net_v2(net, ctx=context, calib_mode=self._calib_mode,
                                        quantized_dtype=self._quant_dtype, calib_data=data,
                                        quantize_mode=self._quant_mode)
        log.info(f'Quantizing model {self._model_name}')
        self.quantized_net = quantized_net

    def quant_network(self):
        return self.quantized_net

    def save_model_as_symbol_block(self):
        if self._model_name is None:
            if not os.path.exists('quantized_model'):
                os.mkdir('quantized_model')
            self.quantized_net.export('quantized_model/quantized_model')
        else:
            name = self._model_name
            dtype = self._quant_dtype
            if not os.path.exists(name):
                os.mkdir(name)
            log.info(f'Saving {dtype} quantized model {name}')
            self.quantized_net.export(f'{name}/quantized_{dtype}_{name}')


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
    parser.add_argument('-mn', '--model_name',
                        help='Model name to download using GluonCV package.',
                        type=str,
                        dest='model_name')
    parser.add_argument('-cm', '--calib_mode',
                        help='If calib_mode=`none`, no calibration'
                             'will be used and the thresholds for requantization'
                             'after the corresponding layers will be calculated at'
                             'runtime by calling min and max operators'
                             'If calib_mode=`naive`, the min and max values of the layer'
                             'outputs from a calibration dataset will be directly taken'
                             'as the thresholds for quantization'
                             'If calib_mode=`entropy`, the thresholds for quantization'
                             'will be derived such that the KL divergence between the'
                             'distributions of FP32 layer outputs and quantized layer'
                             'outputs is minimized based upon the calibration dataset.',
                        default='none',
                        type=str,
                        choices=['none', 'naive', 'entropy'],
                        dest='calib_mode')
    parser.add_argument('-qdt', '--quant_dtype',
                        help='The quantized destination type for input data.'
                             'Currently support `int8`, `uint8`',
                        default='auto',
                        type=str,
                        choices=['int8', 'uint8', 'auto'],
                        dest='quant_dtype')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, B is a batch size,'
                             'W is an input tensor width,'
                             'H is an input tensor height,'
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('-qm', '--quantize_mode',
                        help='The mode that quantization pass to apply.'
                             'Support `full` and `smart`.'
                             '`full` means quantize all operator if possible.'
                             '`smart` means quantization pass will smartly'
                             'choice which operator should be quantized.',
                        default='full',
                        type=str,
                        choices=['full', 'smart'],
                        dest='quant_mode')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or '
                             'NVIDIA_GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    args = parser.parse_args()

    return args


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    context = get_device(args.device, 'quantization')
    quant_wrapper = QuantWrapper(create_dict_for_quantwrapper(args))
    if ((args.model_name is not None)
            and (args.model_json is None)
            and (args.model_params is None)):
        net = load_network_gluon_model_zoo(args.model_name, None, context,
                                           save_model=True, path_save_model=None,
                                           task='quantization')
    elif (args.model_json is not None) and (args.model_params is not None):
        net = load_network_gluon(args.model_json, args.model_params,
                                 context, args.input_name)
    else:
        raise ValueError('Incorrect arguments.')

    quant_wrapper.quant_gluon_model(net, context)
    quant_wrapper.save_model_as_symbol_block()


if __name__ == '__main__':
    sys.exit(main() or 0)
