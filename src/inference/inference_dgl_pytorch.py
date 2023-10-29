import argparse
import importlib
import json
import logging as log
import sys
import traceback
from pathlib import Path
from time import time

import torch
import dgl

import postprocessing_data as pp
from reporter.report_writer import ReportWriter
from inference_tools.loop_tools import loop_inference
from dgl_pytorch_auxiliary import inference_iteration, get_device_to_infer


def cli_argument_parser() -> argparse.Namespace:
    """Parsing all command line parameters

    Returns:
        argparse.Namespace: object for storing attributes
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to PyTorch model with format .pt.',
                        type=str,
                        dest='model')
    parser.add_argument('-mm', '--module',
                        help='Path to module with model architecture.',
                        default='torchvision.models',
                        type=str,
                        dest='module')
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
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations.',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--inference_mode',
                        help='Inference mode',
                        default=True,
                        type=bool,
                        dest='inference_mode')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'dgl_pytorch_inference_report.json',
                        dest='report_path',
                        help='Path to json benchmark report path, default: ./dgl_pytorch_inference_report.json')

    args = parser.parse_args()

    return args


def prepare_input(input_path: str) -> any:
    """Prepare input data to correct format

    Args:
        input_path (str): Path to input file

    Returns:
        any: graph object in DGL format
    """
    graph = dgl.data.utils.load_graphs(input_path)  # load graph
    g = graph[0][0]
    return g


def compile_model(model: any, device) -> any:
    """prepare and compile model. Now compile not support

    Args:
        module (any): PyTorch model

    Returns:
        any: PyTorch model
    """
    model.to(device)
    model.eval()
    return model


def inference_dgl_pytorch(
    model: any, num_iterations: int, input_graph: any, 
    inference_mode: bool, device: torch._C.device, test_duration: int) -> (any, list):
    """inference for DGL with PyTorch in Backend

    Args:
        model (any): PyTorch model
        num_iterations (int): interations count (not support)
        input_graph (any): graph object in DGL format
        inference_mode (bool): inference_mode flag in Pytorch
        device (torch._C.device): devic type for PyTorch
        test_duration (int): time for inference (for loop inference)

    Returns:
        (any, list): (predictions, inference time list)
    """
    features = input_graph.ndata["feat"]
    with torch.inference_mode(inference_mode):
        predictions = None
        time_infer = []
        if num_iterations == 1:
            t0 = time()
            pred = model(input_graph, features).argmax(dim=1)
            correct = (pred[input_graph.ndata['test_mask']] == input_graph.ndata["label"][input_graph.ndata["test_mask"]]).sum()
            predictions = int(correct) / int(input_graph.ndata['test_mask'].sum())
            t1 = time()
            time_infer.append(t1 - t0)
        else:
            # several decorator calls in order to use variables as decorator parameters
            inputs = [input_graph, features]
            time_infer = loop_inference(num_iterations, test_duration)(inference_iteration)(device, inputs, model)
    return predictions, time_infer


def load_model_from_file(model_path: str, module: str, model_name: str) -> any:
    """Load model from file

    Args:
        model_path (str): path to file. Format .pt
        module (str): module name of a model
        model_name (str): model class name

    Raises:
        ValueError: The file type is not supported

    Returns:
        any: PyTorch model
    """
    log.info(f'Loading model from path {model_path}')
    file_type = model_path.split('.')[-1]
    supported_extensions = ['pt']
    if file_type not in supported_extensions:
        raise ValueError(f'The file type {file_type} is not supported')

    model_cls = getattr(importlib.import_module(module, 'GCN'), model_name)

    import __main__
    setattr(__main__, model_name, model_cls)
    model = torch.load(model_path)
    return model


def write_cmd_options_to_report(report_writer: ReportWriter, args: argparse.Namespace) -> None:
    """Write cmd options to report

    Args:
        report_writer (ReportWriter): report object
        args (argparse.Namespace): cmd options
    """
    report_writer.update_cmd_options(
        m=args.module,
        i=args.input
    )

    report_writer.update_configuration_setup(
        iterations_num=args.number_iter,
        target_device=args.device,
        duration=args.time
    )

    report_writer.update_framework_info(
        name='DGL', 
        version=dgl.__version__,
        device=args.device,
        backend='PyTorch'
    )

    report_writer.write_report(args.report_path)


def main() -> None:
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    report_writer = ReportWriter()
    write_cmd_options_to_report(report_writer, args)

    try:
        model = load_model_from_file(args.model, args.module, args.model_name)

        device = get_device_to_infer(args.device)
        prepare_model = compile_model(model, device)

        log.info(f'Preparing input data {args.input}')
        input_data = prepare_input(args.input[0])

        log.info(f'Starting inference (max {args.number_iter} iterations or {args.time} sec) on {args.device}')
        result, inference_time = inference_dgl_pytorch(prepare_model, args.number_iter, 
                                                       input_data, args.inference_mode, device, args.time)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(1, inference_time)
        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
