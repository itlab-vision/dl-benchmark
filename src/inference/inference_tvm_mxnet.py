import argparse
import json
import sys
import traceback
import warnings
from pathlib import Path

import gluoncv
import mxnet
import tvm

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import TVMIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import TVMTransformer
from tvm_auxiliary import (TVMConverter, create_dict_for_converter_mxnet,
                           prepare_output, create_dict_for_modelwrapper,
                           create_dict_for_transformer, inference_tvm)

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name',
                        help='Model name to download using packages from GluonCV.',
                        type=str,
                        dest='model_name')
    parser.add_argument('-m', '--model',
                        help='Path to an .json file with a trained model.',
                        type=str,
                        dest='model_path')
    parser.add_argument('-w', '--weights',
                        help='Path to an .params file with a trained weights.',
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
    parser.add_argument('-ol', '--opt_level',
                        help='TVM optimization level for graph module.',
                        default=0,
                        type=int,
                        dest='opt_level')
    parser.add_argument('--channel_swap',
                        help='Parameter of channel swap (WxHxC to CxWxH by default).',
                        default=[2, 0, 1],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    parser.add_argument('--raw_output',
                        help='Raw output without logs.',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'tvm_inference_report.json',
                        dest='report_path')
    args = parser.parse_args()
    return args


class MXNetToTVMConverter(TVMConverter):
    def __init__(self, args):
        super().__init__(args)

    def _get_device_for_framework(self):
        device = self.args['device']
        if device == 'CPU':
            return mxnet.cpu()
        elif device == 'NVIDIA_GPU':
            return mxnet.gpu()
        else:
            log.info(f'The device {device} is not supported')
            raise ValueError('The device is not supported')

    def _get_mxnet_network(self):
        model_name = self.args['model_name']
        model_path = self.args['model_path']
        weights = self.args['model_params']
        context = self._get_device_for_framework()

        if ((model_name is not None)
                and (model_path is None)
                and (weights is None)):
            log.info(f'Loading network \"{model_name}\" from GluonCV model zoo')
            net = gluoncv.model_zoo.get_model(model_name, pretrained=True, ctx=context)
            return net

        elif ((model_path is not None) and (weights is not None)):
            log.info(f'Deserializing network from file ({model_path}, {weights})')
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                net = mxnet.gluon.nn.SymbolBlock.imports(
                    model_path, [self.args['input_name']], weights, ctx=context)
            return net

        else:
            raise ValueError('Incorrect arguments.')

    def _convert_model_from_framework(self, target, dev):
        net = self._get_mxnet_network()
        op_lev = self.args['opt_level']
        shape_dict = {self.args['input_name']: self.args['input_shape']}
        log.info('Creating graph module from MXNet model')
        model, params = tvm.relay.frontend.from_mxnet(net, shape_dict)
        with tvm.transform.PassContext(opt_level=op_lev):
            lib = tvm.relay.build(model, target=target, params=params)
        module = tvm.contrib.graph_executor.GraphModule(lib['default'](dev))
        return module


def main():
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
        converter = MXNetToTVMConverter(create_dict_for_converter_mxnet(args))
        graph_module = converter.get_graph_module()
        log.info(f'Preparing input data: {args.input}')
        io.prepare_input(graph_module, args.input)
        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, infer_time = inference_tvm(graph_module,
                                           args.number_iter,
                                           args.input_name,
                                           io.get_slice_input,
                                           args.time)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    res = prepare_output(result, args.task, args.output_names)
                    log.info('Inference results')
                    io.process_output(res, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

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
