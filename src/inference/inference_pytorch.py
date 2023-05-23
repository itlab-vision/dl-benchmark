import argparse
import ast
import importlib
import logging as log
import re
import sys
import traceback
from time import time

import torch

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import PyTorchIOModelWrapper
from transformer import PyTorchTransformer


def names_arg(values):
    if values is not None:
        values = values.split(',')

    return values


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to PyTorch model with format .pt.',
                        type=str,
                        dest='model')
    parser.add_argument('-mn', '--model_name',
                        help='Model name from TorchVision.',
                        type=str,
                        dest='model_name')
    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-in', '--input_names',
                        help='Names of the input tensors',
                        default=None,
                        type=names_arg,
                        dest='input_names')
    parser.add_argument('-is', '--input_shapes',
                        help='Input tensor shapes',
                        default=None,
                        type=str,
                        dest='input_shapes')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=None,
                        type=str,
                        dest='mean')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        type=str,
                        dest='input_scale')
    parser.add_argument('--output_names',
                        help='Name of the output tensors.',
                        default='output',
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
                        default=None,
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
                        choices=['feedforward', 'classification'],
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
    parser.add_argument('--model_type',
                        help='Model type for inference',
                        choices=['scripted', 'baseline'],
                        default='scripted',
                        type=str,
                        dest='model_type')
    parser.add_argument('--inference_mode',
                        help='Inference mode',
                        default=True,
                        type=bool,
                        dest='inference_mode')
    parser.add_argument('--tensor_rt_precision',
                        help='Tensor RT precision FP16, FP32.'
                             ' Applicable only for hosts with NVIDIA GPU and pytorch built with Tensor-RT support',
                        type=str,
                        default=None,
                        dest='tensor_rt_precision')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('--input_type',
                        help='Parameter input type',
                        default=None,
                        type=str,
                        dest='input_type')

    args = parser.parse_args()

    return args


def get_device_to_infer(device):
    log.info('Get device for inference')
    if device == 'CPU':
        log.info(f'Inference will be executed on {device}')
        return torch.device('cpu')
    elif device == 'NVIDIA_GPU':
        log.info(f'Inference will be executed on {device}')
        return torch.device('cuda')
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')


def is_gpu_available():
    return torch.cuda.is_available()


def get_trt_dtype(tensor_rt_precision):
    if tensor_rt_precision:
        tensor_rt_dtype = None
        if tensor_rt_precision == 'FP32':
            tensor_rt_dtype = torch.float
        elif tensor_rt_precision == 'FP16':
            tensor_rt_dtype = torch.half
        else:
            raise ValueError(f'Unknown Tensor RT precision {tensor_rt_precision}')
        return tensor_rt_dtype
    else:
        return None


def load_model_from_module(model_name):
    model_cls = model_name
    model_path = 'torchvision.models'
    model_cls = importlib.import_module(model_path).__getattribute__(model_cls)
    module = model_cls(weights=True)
    return module


def load_model_from_file(model_path):
    log.info(f'Loading model from path {model_path}')
    file_type = model_path.split('.')[-1]
    supported_extensions = ['pt']
    if file_type not in supported_extensions:
        raise ValueError(f'The file type {file_type} is not supported')
    model = torch.load(model_path)
    return model


def compile_model(module, device, model_type, use_tensorrt, shapes, trt_dtype):
    if model_type == 'baseline':
        log.info('Inference will be executed on baseline model')
    elif model_type == 'scripted':
        log.info('Inference will be executed on scripted model')
        module = torch.jit.script(module)
    else:
        raise ValueError(f'Model type {model_type} is not supported for inference')
    module.to(device)
    module.eval()

    if use_tensorrt:
        if is_gpu_available():
            import torch_tensorrt
            inputs = [torch_tensorrt.Input(shapes[key], dtype=trt_dtype) for key in shapes]
            trt_ts_module = torch_tensorrt.compile(module, inputs=inputs,
                                                   truncate_long_and_double=True,
                                                   enabled_precisions=trt_dtype)
            return trt_ts_module
        else:
            raise ValueError('GPU is not available')
    else:
        return module


def create_dict_for_transformer(args):
    dictionary = {}
    for name in args.input_names:
        mean = args.mean.get(name, None)
        input_scale = args.input_scale.get(name, None)
        layout = args.layout.get(name, 'NCHW')
        dictionary[name] = {'channel_swap': None, 'mean': mean,
                            'input_scale': input_scale, 'layout': layout}
    return dictionary


def inference_pytorch(model, num_iterations, get_slice, input_names, inference_mode, device):
    with torch.inference_mode(inference_mode):
        predictions = None
        time_infer = []
        if num_iterations == 1:
            inputs = [torch.from_numpy(get_slice()[input_name]).to(device) for input_name in input_names]
            t0 = time()
            predictions = torch.nn.functional.softmax(model(*inputs), dim=1)
            t1 = time()
            time_infer.append(t1 - t0)
        else:
            for _ in range(num_iterations):
                inputs = [torch.from_numpy(get_slice()[input_name]).to(device) for input_name in input_names]
                t0 = time()
                with torch.no_grad():
                    model(*inputs)
                t1 = time()
                time_infer.append(t1 - t0)

    return predictions, time_infer


def prepare_output(result, output_names, task):
    if task == 'feedforward':
        return {}
    if (output_names is None) or len(output_names) == 0:
        raise ValueError('The number of output tensors does not match the number of corresponding output names')
    if task == 'classification':
        return {output_names[0]: result.detach().numpy()}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def parse_input_arg(values, input_names):
    return_values = {}
    if values is not None:
        matches = re.findall(r'(.*?)\[(.*?)\],?', values)
        if matches:
            for i, match in enumerate(matches):
                name, value = match
                value = ast.literal_eval(value)
                if name != '':
                    return_values[name] = value
                else:
                    if input_names is None:
                        raise ValueError('Please set --input-names parameter'
                                         ' or use input0[value0],input1[value1] format')
                    return_values[input_names[i]] = list(value)
        else:
            raise ValueError(f'Unable to parse input parameter: {values}')
    return return_values


def parse_layout_arg(values, input_names):
    return_values = {}
    if values is not None:
        matches = re.findall(r'(.*?)\((.*?)\),?', values)
        if matches:
            for i, match in enumerate(matches):
                name, value = match
                if name != '':
                    return_values[name] = value
                else:
                    if input_names is None:
                        raise ValueError(f'Please set --input-names parameter'
                                         f' or use input0(value0),input1(value1) format instead {values}')
                    return_values[input_names[i]] = value
        else:
            values = values.split(',')
            return_values = dict(zip(input_names, values))
    return return_values


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        trt_dtype = get_trt_dtype(args.tensor_rt_precision)
        args.input_shapes = parse_input_arg(args.input_shapes, args.input_names)
        model_wrapper = PyTorchIOModelWrapper(args.input_shapes, args.batch_size, trt_dtype, args.input_type)

        args.mean = parse_input_arg(args.mean, args.input_names)
        args.input_scale = parse_input_arg(args.input_scale, args.input_names)
        args.layout = parse_layout_arg(args.layout, args.input_names)
        data_transformer = PyTorchTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        if args.model_name is not None and args.model is None:
            model = load_model_from_module(args.model_name)
        elif args.model_name is None and args.model is not None:
            model = load_model_from_file(args.model)
        else:
            raise ValueError('Incorrect arguments.')

        device = get_device_to_infer(args.device)
        compiled_model = compile_model(model, device, args.model_type,
                                       args.tensor_rt_precision is not None, args.input_shapes, trt_dtype)

        for layer_name in args.input_names:
            layer_shape = model_wrapper.get_input_layer_shape(args.model, layer_name)
            log.info(f'Shape for input layer {layer_name}: {layer_shape}')

        log.info(f'Preparing input data {args.input}')
        io.prepare_input(compiled_model, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, inference_time = inference_pytorch(compiled_model, args.number_iter,
                                                   io.get_slice_input, args.input_names, args.inference_mode,
                                                   device)

        log.info('Computing performance metrics')
        average_time, latency, fps = pp.calculate_performance_metrics_sync_mode(args.batch_size,
                                                                                inference_time)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.task)

                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

            log.info('Performance results')
            pp.log_performance_metrics_sync_mode(log, average_time, fps, latency)
        else:
            pp.print_performance_metrics_sync_mode(average_time, fps, latency)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
