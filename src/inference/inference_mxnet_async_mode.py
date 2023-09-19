import argparse
import json
import logging as log
import os
import sys
import traceback
import warnings
from pathlib import Path
from time import time

import gluoncv
import mxnet

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import MXNetIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import MXNetTransformer
from mxnet_auxiliary import prepare_output


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
    parser.add_argument('--hybrid',
                        help='Flag to enable symbolic computations.'
                             'Default value is false.',
                        action='store_true',
                        dest='hybrid')
    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, B is a batch size,'
                             'W is an input tensor width,'
                             'H is an input tensor height,'
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('--norm',
                        help='Flag to normalize input images'
                             '(use --mean and --std arguments to set'
                             'required normalization parameters).',
                        action='store_true',
                        dest='norm')
    parser.add_argument('--mean',
                        help='Mean values.',
                        default=[0, 0, 0],
                        type=float,
                        nargs=3,
                        dest='mean')
    parser.add_argument('--std',
                        help='Standard deviation values.',
                        default=[1., 1., 1.],
                        type=float,
                        nargs=3,
                        dest='std')
    parser.add_argument('--channel_swap',
                        help='Parameter of channel swap (WxHxC to CxWxH by default).',
                        default=[2, 0, 1],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    parser.add_argument('--output_names',
                        help='Name of the output tensors.',
                        default=None,
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file.',
                        default='image_net_labels.json',
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results.',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Task type determines the type of output processing '
                             'method. Available values: feedforward - without'
                             'postprocessing (by default), classification - output'
                             'is a vector of probabilities.',
                        choices=['feedforward', 'classification', 'detection',
                                 'segmentation'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations.',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs.',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or '
                             'NVIDIA GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('-s', '--save_model',
                        help='Flag to indicate whether the model should be saved'
                             '(it may be required for GluonCV-models)',
                        action='store_true',
                        dest='save_model')
    parser.add_argument('-p', '--path_save_model',
                        help='Path to save model',
                        default=None,
                        type=str,
                        dest='path_save_model')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'mxnet_async_inference_report.json',
                        dest='report_path')
    parser.add_argument('--threshold',
                        help='Probability threshold for detections filtering',
                        default=0.5,
                        type=float,
                        dest='threshold')
    parser.add_argument('--color_map',
                        help='Classes color map',
                        type=str,
                        default=None,
                        dest='color_map')

    args = parser.parse_args()

    return args


def get_device_to_infer(device):
    log.info('Get device for inference')
    if device == 'CPU':
        log.info(f'Inference will be executed on {device}')
        return mxnet.cpu()
    elif device == 'NVIDIA_GPU':
        log.info(f'Inference will be executed on {device}')
        return mxnet.gpu()
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')


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

    log.info(f'Hybridizing model to accelerate inference: {hybrid}')
    if hybrid is True:
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
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
    }
    return dictionary


def inference_mxnet(net, num_iterations, get_slice, input_name):
    predictions = None
    slice_input = None
    if num_iterations == 1:
        mxnet.nd.waitall()
        inference_time = time()
        slice_input = get_slice()
        predictions = net(slice_input[input_name])
        mxnet.nd.waitall()
        inference_time = time() - inference_time
    else:
        mxnet.nd.waitall()
        inference_time = time()
        for _ in range(num_iterations):
            slice_input = get_slice()
            net(slice_input[input_name]).softmax()
        mxnet.nd.waitall()
        inference_time = time() - inference_time

    return predictions, inference_time


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='MxNet', version=mxnet.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)

    try:
        model_wrapper = MXNetIOModelWrapper(create_dict_for_modelwrapper(args))
        data_transformer = MXNetTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        context = get_device_to_infer(args.device)

        if ((args.model_name is not None)
                and (args.model_json is None)
                and (args.model_params is None)):
            net = load_network_gluon_model_zoo(args.model_name, args.hybrid, context,
                                               args.save_model, args.path_save_model)
        elif (args.model_json is not None) and (args.model_params is not None):
            net = load_network_gluon(args.model_json, args.model_params, context,
                                     args.input_name)
        else:
            raise ValueError('Incorrect arguments.')

        log.info(f'Shape for input layer {args.input_name}: {args.input_shape}')

        log.info(f'Preparing input data {args.input}')
        io.prepare_input(net, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, inference_time = inference_mxnet(net, args.number_iter,
                                                 io.get_slice_input_mxnet, args.input_name)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_async_mode(inference_time,
                                                                       args.batch_size,
                                                                       args.number_iter)
        report_writer.update_execution_results(**inference_result, iterations_num=args.number_iter)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.task,
                                            model_wrapper)

                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

            log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
