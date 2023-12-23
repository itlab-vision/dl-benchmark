import argparse
import json
import sys
import traceback
from pathlib import Path
from time import time

import mxnet

import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import MXNetIOModelWrapper
from mxnet_auxiliary import (load_network_gluon, load_network_gluon_model_zoo,
                             get_device, create_dict_for_modelwrapper,
                             create_dict_for_transformer, prepare_output,
                             create_dict_for_quantwrapper)
from quantization_mxnet import QuantWrapper
from reporter.report_writer import ReportWriter
from transformer import MXNetTransformer

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


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
                        required=False,
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
                             'NVIDIA_GPU (CPU by default)',
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
                        default=Path(__file__).parent / 'mxnet_sync_inference_report.json',
                        dest='report_path')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
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
    parser.add_argument('-q', '--quantization',
                        help='Quantization model for further inference.',
                        action='store_true',
                        dest='quantization')
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
                        help='The quantized type of weights.'
                             'Currently support `int8`, `uint8`',
                        default='auto',
                        type=str,
                        choices=['int8', 'uint8', 'auto'],
                        dest='quant_dtype')
    parser.add_argument('-qm', '--quantize_mode',
                        help='The mode that quantization pass to apply.'
                             'Support `full` and `smart`.'
                             '`full` means quantize all operators if possible.'
                             '`smart` means quantization pass will smartly'
                             'choice which operator should be quantized.',
                        default='full',
                        type=str,
                        choices=['full', 'smart'],
                        dest='quant_mode')
    parser.add_argument('-sqm', '--save_quantized_model',
                        help='Save quantized model.',
                        action='store_true',
                        dest='save_quantized_model')
    args = parser.parse_args()

    return args


def inference_mxnet(net, num_iterations, get_slice, input_name, test_duration):
    predictions = None
    time_infer = []
    if num_iterations == 1:
        mxnet.nd.waitall()
        t0 = time()
        slice_input = get_slice()
        predictions = net(slice_input[input_name])
        mxnet.nd.waitall()
        t1 = time()
        time_infer.append(t1 - t0)
    else:
        time_infer = loop_inference(num_iterations, test_duration)(inference_iteration)(get_slice, input_name, net)
    return predictions, time_infer


def inference_iteration(get_slice, input_name, net):
    mxnet.nd.waitall()
    slice_input = get_slice()
    _, exec_time = infer_slice(input_name, net, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(input_name, net, slice_input):
    res = net(slice_input[input_name])
    mxnet.nd.waitall()
    return res


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='MXNet', version=mxnet.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)

    try:
        model_wrapper = MXNetIOModelWrapper(create_dict_for_modelwrapper(args))
        data_transformer = MXNetTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        context = get_device(args.device, 'inference')

        quant_wrapper = QuantWrapper(create_dict_for_quantwrapper(args))

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

        if (args.quantization):
            quant_wrapper.quant_gluon_model(net, context)
            net = quant_wrapper.quantized_net

        if (args.save_quantized_model):
            quant_wrapper.save_model_as_symbol_block()

        log.info(f'Shape for input layer {args.input_name}: {args.input_shape}')

        if args.input:
            log.info(f'Preparing input data: {args.input}')
            io.prepare_input(net, args.input)
        else:
            current_shape = model_wrapper.get_input_layer_shape(net, args.input_name)
            transformed_shape = [
                args.batch_size,
                *io._transformer.get_shape_in_chw_order(current_shape, args.input_name[0]),
            ]
            custom_shapes = {args.input_name[0]: transformed_shape}
            model_wrapper._input_shape = [transformed_shape]
            io.fill_unset_inputs(net, log, custom_shapes)

        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, inference_time = inference_mxnet(net, args.number_iter,
                                                 io.get_slice_input_mxnet, args.input_name, args.time)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)
        report_writer.update_execution_results(**inference_result)
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

            log.info('Performance results')
            log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
