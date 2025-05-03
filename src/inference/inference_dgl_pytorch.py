import argparse
import importlib
import json
import sys
import traceback
from pathlib import Path
from time import time
import importlib.util

import torch
import dgl
from ogb.nodeproppred import DglNodePropPredDataset

import postprocessing_data as pp
from reporter.report_writer import ReportWriter
from inference_tools.loop_tools import loop_inference
from pytorch_auxiliary import get_device_to_infer, infer_slice, set_thread_num
from io_model_wrapper import DGLPyTorchWrapper
from io_graphs_adapter.graph_adapter import IOGraphAdapter

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to PyTorch model with format .pt.',
                        type=str,
                        required=True,
                        dest='model')
    parser.add_argument('-mm', '--module',
                        help='Path to module with model architecture.',
                        type=str,
                        required=True,
                        dest='module_path')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or '
                             'NVIDIA_GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
    parser.add_argument('-mn', '--model_name',
                        help='Model name from the module.',
                        required=True,
                        type=str,
                        dest='model_name')
    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=False,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('--raw_output',
                        help='Raw output without logs.',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations.',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('-t', '--task',
                        help='Task type determines the type of output processing '
                             'method. Available values: node-classification.',
                        choices=['feedforward', 'node-classification'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1000,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-nw', '--num_workers',
                        help='Num workers in data loading.',
                        default=1,
                        type=int,
                        dest='num_workers')
    parser.add_argument('-ogbd', '--ogb_data',
                        help='Loading ogb data.',
                        choices=['ogbn-products'],
                        default=None,
                        type=str,
                        dest='ogb_data')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'dgl_pytorch_inference_report.json',
                        dest='report_path',
                        help='Path to json benchmark report path, default: ./dgl_pytorch_inference_report.json')
    parser.add_argument('--num_inter_threads',
                        help='Number of threads used for parallelism between independent operations',
                        default=None,
                        type=int,
                        dest='num_inter_threads')
    parser.add_argument('--num_intra_threads',
                        help='Number of threads used within an individual op for parallelism',
                        default=None,
                        type=int,
                        dest='num_intra_threads')

    args = parser.parse_args()

    return args


def auto_load_from_ogb(task, device):
    data = DglNodePropPredDataset(name=task)
    g, _ = data[0]
    g.create_formats_()
    g = g.to(device)
    return g


def prepare_input(input_path, device):
    graph = dgl.data.utils.load_graphs(input_path)  # load graph
    g = graph[0][0]
    g = g.to(device)
    return g


def compile_model(model, device, batch_size, num_workers):
    model.batch_size = batch_size
    model.num_workers = num_workers
    model.to(device)
    model.eval()
    return model


def inference_dgl_pytorch(model, num_iterations, input_graph, device, test_duration):
    features = input_graph.ndata['feat']
    with torch.inference_mode():
        predictions = None
        time_infer = []
        if num_iterations == 1:
            t0 = time()
            if 'inference' in dir(model):
                predictions = model.inference(input_graph, features, device).argmax(dim=1)
            else:
                predictions = model(input_graph, features, device).argmax(dim=1)
            t1 = time()
            time_infer.append(t1 - t0)
        else:
            # several decorator calls in order to use variables as decorator parameters
            if 'inference' in dir(model):
                inputs = [input_graph, features, device]
                time_infer = loop_inference(num_iterations, test_duration)(inference_iteration)(
                    device,
                    inputs,
                    model.inference,
                )
            else:
                inputs = [input_graph, features]
                time_infer = loop_inference(num_iterations, test_duration)(inference_iteration)(device, inputs, model)
    return predictions, time_infer


def inference_iteration(device, inputs, model):
    if device.type == 'cuda':
        torch.cuda.synchronize()
    _, exec_time = infer_slice(device, inputs, model)
    return exec_time


def load_model_from_file(model_path, module_path, model_name):
    log.info(f'Loading model from path {model_path}')
    file_type = model_path.split('.')[-1]
    supported_extensions = ['pt']
    if file_type not in supported_extensions:
        raise ValueError(f'The file type {file_type} is not supported')

    log.info(f'Load module from {module_path}')
    spec = importlib.util.spec_from_file_location(model_name, module_path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[f'{model_name}'] = foo
    spec.loader.exec_module(foo)

    import __main__
    setattr(__main__, model_name, getattr(foo, model_name))
    model = torch.load(model_path, map_location=torch.device('cpu'))

    return model


def prepare_output(result, task):
    if task == 'feedforward':
        return {}
    elif task == 'node-classification':
        log.info('Converting output tensor to print results')
        return {'output_result': result.detach().numpy()}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def write_cmd_options_to_report(report_writer, args):
    report_writer.update_cmd_options(
        m=args.module_path,
        i=args.input,
    )

    report_writer.update_configuration_setup(
        iterations_num=args.number_iter,
        target_device=args.device,
        duration=args.time,
    )

    report_writer.update_framework_info(
        name='DGL',
        version=dgl.__version__,
        device=args.device,
        backend='PyTorch',
    )

    report_writer.write_report(args.report_path)


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    write_cmd_options_to_report(report_writer, args)

    try:
        model = load_model_from_file(args.model, args.module_path, args.model_name)
        device = get_device_to_infer(args.device)
        compiled_model = compile_model(model, device, args.batch_size, args.num_workers)

        model_wrapper = DGLPyTorchWrapper(compiled_model)
        io = IOGraphAdapter.get_io_adapter(args, model_wrapper)

        set_thread_num(args.num_inter_threads, args.num_intra_threads)

        log.info(f'Preparing input data {args.input}')
        if args.ogb_data:
            input_data = auto_load_from_ogb(args.ogb_data, device)
        else:
            input_data = prepare_input(args.input[0], device)

        log.info(f'Starting inference (max {args.number_iter} iterations or {args.time} sec) on {args.device}')
        result, inference_time = inference_dgl_pytorch(compiled_model, args.number_iter,
                                                       input_data, device, args.time)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(1, inference_time['time_infer'])
        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    result = prepare_output(result, args.task)

                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
