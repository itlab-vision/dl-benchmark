import argparse
import logging as log
import sys
from time import time
import numpy as np
import json

import mxnet
import mxnet.gluon.model_zoo.vision as model_zoo

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import MXNetIOModelWrapper
from transformer import MXNetTransformer


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
    parser.add_argument('-n', '--model_name',
                        help='Model name to download using Gluon package.',
                        type=str,
                        required=True,
                        dest='model_name')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-in', '--input_name',
                        help='Input name',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape WxHxC, W is an input tensor width, \
                              H is an input tensor height, C is an input tensor \
                              number of channnels',
                        default=None,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=[0, 0, 0],
                        type=float,
                        nargs=3,
                        dest='mean')
    parser.add_argument('--std',
                        help='Parameter standard deviation',
                        default=[1., 1., 1.],
                        type=float,
                        nargs=3,
                        dest='std')
    parser.add_argument('--norm',
                        help='Flag to normalize input images',
                        default=True,
                        type=bool,
                        dest='norm')
    parser.add_argument('--channel_swap',
                        help='Parameter channel swap',
                        default=[2, 0, 1],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results',
                        default=10,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification'],
                        default='classification',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')

    args = parser.parse_args()

    return args


def get_device_to_infer(device):
    log.info('Get device for inference')
    if device == 'CPU':
        log.info(f'Inference will be executed on {device}')
        return mxnet.cpu()
    elif device == 'GPU':
        log.info(f'Inference will be executed on {device}')
        return mxnet.gpu()
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')


def load_network(model_json, model_params, context):
    raise ValueError('Function is not implemented')


def load_network_gluon(model_name, context, input_name, input_shape):
    log.info(f'Loading network \"{model_name}\"')
    net = model_zoo.get_model(model_name, pretrained=True, ctx=context)
    log.info(f'Info about the network:\n{net}')
    
    log.info('Hybridize model to accelerate inference')
    net.hybridize()

    return net

def create_dict_for_transformer(args):
    dictionary = {
        'channel_swap': args.channel_swap,
        'mean': args.mean,
        'std': args.std,
        'norm': args.norm,
        'input_shape': args.input_shape,
        'batch_size': args.batch_size,
    }
    return dictionary

def create_dict_for_modelwrapper(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': args.input_shape,
    }
    return dictionary

def print_topk_predictions(predictions, k):
    mxnet.test_utils.download('https://raw.githubusercontent.com/dmlc/web-data/master/mxnet/doc/tutorials/onnx/image_net_labels.json')
    categories = np.array(json.load(open('image_net_labels.json', 'r')))
    top_pred = predictions.topk(k=k)[0].asnumpy()
    for index in top_pred:
        probability = predictions[0][int(index)]
        category = categories[int(index)]
        print("{}: {:.2f}%".format(category, probability.asscalar()*100))

def inference_mxnet(net, num_iterations, get_slice, input_name):
    predictions = None
    time_infer = []
    slice_input = None
    if num_iterations == 1:
        slice_input = get_slice(0)
        t0 = time()
        predictions = net(slice_input[input_name]).softmax()
        t1 = time()
        print_topk_predictions(predictions, 5)
        time_infer.append(t1 - t0)
    else:
        for i in range(num_iterations):
            slice_input = get_slice(i)
            t0 = time()
            net(slice_input[input_name]).softmax()
            t1 = time()
            time_infer.append(t1 - t0)

    return predictions, time_infer

def process_result(batch_size, inference_time):
    inference_time = pp.three_sigma_rule(inference_time)
    average_time = pp.calculate_average_time(inference_time)
    latency = pp.calculate_latency(inference_time)
    fps = pp.calculate_fps(batch_size, latency)
    return average_time, latency, fps

def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        model_wrapper = MXNetIOModelWrapper(create_dict_for_modelwrapper(args))
        data_transformer = MXNetTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        context = get_device_to_infer(args.device)

        if (args.model_name is not None) and \
               (args.model_json is None) and \
               (args.model_params is None):
            net = load_network_gluon(args.model_name, context, args.input_name,
                                     args.input_shape)
        elif (args.model_json is not None) and (args.model_params is not None):
            net = load_network(args.model_json, args.model_params, context)
        else:
            raise ValueError('Incorrect arguments.')

        log.info('Prepare input data')
        io.prepare_input(net, args.input)

        log.info('Start inference')
        result, inference_time = inference_mxnet(net, args.number_iter,
                                                 io.get_slice_input, args.input_name)
        
        log.info('Compute performance metrics')
        time, latency, fps = process_result(args.batch_size, inference_time)
        log.info(f'Performance metrics:\n\tAverage time = {time} s\n\tLatency={latency}\n\tFPS={fps} fps')
    except Exception as ex:
        log.error(str(ex))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)

