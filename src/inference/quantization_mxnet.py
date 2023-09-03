import sys
import argparse
import os
import logging as log
import mxnet
from mxnet.contrib.quantization import *
from inference_mxnet_sync_mode import load_network_gluon, \
                                      load_network_gluon_model_zoo


class QuantWrapper:
    def __init__(self, args):
        self._calib_mode = args['calib_mode']
        self._quant_dtype = args['quant_dtype']
        self._input_shape = args['input_shape']
        self._model_name = args['model_name']
        self._model_json = args['model_json']
        self._weights = args['model_params']
    
    def quant_gluon_model(self):
        log.info('Load model as symbol block')
        sym, arg_params, aux_params = mxnet.model.load_checkpoint(f'{self._model_name}/{self._model_name}', 0)
        log.info(f'Quantizing model {self._model_name}')
        qsym, qarg_params, aux_params, _ = quantize_graph(sym=sym, arg_params=arg_params, 
                                                          aux_params=aux_params,
                                                          calib_mode=self._calib_mode,
                                                          quantized_dtype=self._quant_dtype)
        mxnet.model.save_checkpoint(f'{self._model_name}/quantized_{self._model_name}', 0, qsym, qarg_params, aux_params)
        


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
                        required=False,
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
        'input_shape': args.input_shape,
        'model_name': args.model_name,
        'model_json': args.model_json,
        'model_params': args.model_params,
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
    if ((args.model_name is not None)
            and (args.model_json is None)
            and (args.model_params is None)):
        quant_wrapper = QuantWrapper(create_dict_for_quantwrapper(args))
        load_network_gluon_model_zoo(args.model_name, None, context,
                                     save_model=True, path_save_model=None)
        quant_wrapper.quant_gluon_model()
    elif (args.model_json is not None) and (args.model_params is not None):
        net = load_network_gluon(args.model_json, args.model_params, context,
                                 args.input_name)
    else:
        raise ValueError('Incorrect arguments.')

if __name__ == '__main__':
    sys.exit(main() or 0)