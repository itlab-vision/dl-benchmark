import sys
import argparse
import os
import logging as log
import mxnet
import gluoncv
from mxnet.contrib.quantization import *

class QuantWrapper:
    def __init__(self, args):
        self._calib_mode = args['calib_mode']
        self._quant_dtype = args['quant_dtype']
        self._input_shape = args['input_shape']
        self._model_name = args['model_name']
        self._model_json = args['model_json']
        self._input_name = args['input_name']
        self._weights = args['model_params']
        self.quantized_net = None
    
    def quant_gluon_model(self, net, context):
        data = mxnet.nd.ones([1, *self._input_shape])
        quantized_net = quantize_net_v2(net, ctx=context, calib_mode=self._calib_mode,
                                        quantized_dtype=self._quant_dtype, calib_data=data)
        log.info(f'Quantizing model {self._model_name}')
        self.quantized_net = quantized_net

    def quant_network(self):
        return self.quantized_net

    def save_model_as_symbol_block(self):
        self.quantized_net.hybridize(static_shape=True, static_alloc=True)
        self.quantized_net.forward(mxnet.nd.zeros(self._input_shape))
        self.quantized_net.export('alexnet/quantized_int8_alexnet')

def load_network_gluon(model_json, model_params, context, input_name):
    log.info(f'Deserializing network from file ({model_json}, {model_params})')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        deserialized_net = mxnet.gluon.nn.SymbolBlock.imports(
            model_json, [input_name], model_params, ctx=context)
    return deserialized_net

def load_network_gluon_model_zoo(model_name, hybrid, context, save_model, path_save_model):
    log.info(f'Loading network \"{model_name}\" from GluonCV model zoo')
    net = gluoncv.model_zoo.get_model(model_name, pretrained=True, ctx=context)

    if save_model is True:
        log.info(f'Saving model \"{model_name}\" to \"{path_save_model}\"')
        if path_save_model is None:
            path_save_model = os.getcwd()
        path_save_model = os.path.join(path_save_model, model_name)
        if not os.path.exists(path_save_model):
            os.mkdir(path_save_model)
        gluoncv.utils.export_block(os.path.join(path_save_model, model_name), net,
                                   preprocess=None, layout='CHW', ctx=context)

    log.info(f'Info about the network:\n{net}')

    log.info(f'Hybridizing model for quantization: {hybrid}')
    if hybrid is True:
        net.hybridize()
    return net

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
                        default='int8',
                        type=str,
                        choices=['int8', 'uint8'],
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

def get_device_to_quant(device):
    log.info('Get device for quantization')
    if device == 'CPU':
        log.info(f'Quantization will be executed on {device}')
        return mxnet.cpu()
    elif device == 'NVIDIA_GPU':
        log.info(f'Quantization will be executed on {device}')
        return mxnet.gpu()
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')

def create_dict_for_quantwrapper(args):
    dictionary = {
        'calib_mode': args.calib_mode,
        'quant_dtype': args.quant_dtype,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_json': args.model_json,
        'model_params': args.model_params,
        'input_name': args.input_name
    }
    return dictionary

def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    context = get_device_to_quant(args.device)
    quant_wrapper = QuantWrapper(create_dict_for_quantwrapper(args))
    if ((args.model_name is not None)
            and (args.model_json is None)
            and (args.model_params is None)):
        net = load_network_gluon_model_zoo(args.model_name, None, context,
                                           save_model=True, path_save_model=None)
        quant_wrapper.quant_gluon_model(net, context)
        quant_wrapper.save_model_as_symbol_block()
    elif (args.model_json is not None) and (args.model_params is not None):
        net = load_network_gluon(args.model_json, args.model_params,
                                 context, args.input_name)
        quant_wrapper.quant_gluon_model(net, context)
        quant_wrapper.save_model_as_symbol_block()
    else:
        raise ValueError('Incorrect arguments.')

if __name__ == '__main__':
    sys.exit(main() or 0)