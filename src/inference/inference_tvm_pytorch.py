import argparse
import json
import logging as log
import sys
import traceback
import torch
import torchvision
import tvm


from pathlib import Path
from time import time


import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import TVMIOModelWrapper
from transformer import TVMTransformer
from reporter.report_writer import ReportWriter
from tvm_auxiliary import (TVMConverter, create_dict_for_converter_mxnet,
                           prepare_output, create_dict_for_modelwrapper,
                           create_dict_for_transformer)


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name',
                        help='Model name to download using packages from TorchVision.',
                        type=str,
                        dest='model_name')
    parser.add_argument('-m', '--model',
                        help='Path to an .pt file with a trained model.',
                        type=str,
                        dest='model_path')
    parser.add_argument('-w', '--weights',
                        help='Path to an .pth file with a trained weights.',
                        type=str,
                        dest='model_params')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or '
                             'NVIDIA_GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations.',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--output_names',
                        help='Name of the output tensors.',
                        default='output0',
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('-t', '--task',
                        help='Task type determines the type of output processing '
                             'method. Available values: feedforward - without'
                             'postprocessing (by default), classification - output'
                             'is a vector of probabilities.',
                        choices=['feedforward', 'classification'],
                        default='feedforward',
                        type=str,
                        dest='task')
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
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
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
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results to print',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('--channel_swap',
                        help='Parameter of channel swap (WxHxC to CxWxH by default).',
                        default=[2, 0, 1],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'tvm_inference_report.json',
                        dest='report_path')
    args = parser.parse_args()
    return args


class PyTorchToTVMConverter(TVMConverter):
    def __init__(self, args):
        super().__init__(args)

    def _get_device_for_framework(self):
        return super()._get_device_for_framework()

    def _convert_model_from_framework(self, target, dev):
        model_name = self.args['model_name']
        log.info('Get model from TorchVision')
        pt_model = torchvision.models.__getattribute__(model_name)
        pt_model = pt_model(True)
        pt_model = pt_model.eval()
        input_shape = self.args['input_shape']
        input_data = torch.randn(input_shape)
        scripted_model = torch.jit.trace(pt_model, input_data).eval()
        input_name = self.args['input_name']
        shape_list = [(input_name, input_shape)]
        log.info('Creating graph module from PyTorch model')
        model, params = tvm.relay.frontend.from_pytorch(scripted_model, shape_list)
        with tvm.transform.PassContext(opt_level=3):
            lib = tvm.relay.build(model, target=target, params=params)
        module = tvm.contrib.graph_executor.GraphModule(lib['default'](dev))
        return module


def inference_tvm(module, num_of_iterations, input_name, get_slice, test_duration):
    result = None
    time_infer = []
    if num_of_iterations == 1:
        slice_input = get_slice()
        t0 = time()
        module.set_input(input_name, slice_input[input_name])
        module.run()
        result = module.get_output(0)
        t1 = time()
        time_infer.append(t1 - t0)
    else:
        time_infer = loop_inference(num_of_iterations, test_duration)(inference_iteration)(get_slice,
                                                                                           input_name,
                                                                                           module)
    return result, time_infer


def inference_iteration(get_slice, input_name, module):
    slice_input = get_slice()
    _, exec_time = infer_slice(input_name, module, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(input_name, module, slice_input):
    module.set_input(input_name, slice_input[input_name])
    module.run()
    res = module.get_output(0)
    return res


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='TVM', version=tvm.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    try:
        wrapper = TVMIOModelWrapper(create_dict_for_modelwrapper(args))
        transformer = TVMTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, wrapper, transformer)
        log.info(f'Shape for input layer {args.input_name}: {args.input_shape}')
        converter = PyTorchToTVMConverter(create_dict_for_converter_mxnet(args))
        graph_module = converter.get_graph_module()
        log.info(f'Preparing input data: {args.input}')
        io.prepare_input(graph_module, args.input)
        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, infer_time = inference_tvm(graph_module,
                                           args.number_iter,
                                           args.input_name,
                                           io.get_slice_input,
                                           args.time)
        if args.number_iter == 1:
            log.info('Converting output tensor to print results')
            res = prepare_output(result, args.task, args.output_names)
            log.info('Inference results')
            io.process_output(res, log)
        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, infer_time)
        report_writer.update_execution_results(**inference_result)
        report_writer.write_report(args.report_path)
        log.info('Performance results')
        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
