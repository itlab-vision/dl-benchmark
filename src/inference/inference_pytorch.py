import sys
import argparse
import traceback
import importlib
import logging as log
from time import time

import torch

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import PyTorchIOModelWrapper
from transformer import PyTorchTransformer


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
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxCxHxW, B is a batch size,'
                             'C is an input tensor number of channels'
                             'H is an input tensor height,'
                             'W is an input tensor width.',
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


def compile_model(module, device, model_type):
    if model_type == 'baseline':
        log.info('Inference will be executed on baseline model')
    elif model_type == 'scripted':
        log.info('Inference will be executed on scripted model')
        module = torch.jit.script(module)
    else:
        raise ValueError(f'Model type {model_type} is not supported for inference')
    module.to(device)
    module.eval()
    return module


def create_dict_for_transformer(args):
    dictionary = {
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
        'input_shape': [args.batch_size] + args.input_shape[1:],
    }
    return dictionary


def inference_pytorch(model, num_iterations, get_slice, input_name, inference_mode, device):
    with torch.inference_mode(inference_mode):
        predictions = None
        time_infer = []
        slice_input = None
        if num_iterations == 1:
            slice_input = get_slice(0)
            t0 = time()
            data = slice_input[input_name].to(device)
            predictions = torch.nn.functional.softmax(model(data), dim=1)
            t1 = time()
            time_infer.append(t1 - t0)
        else:
            for i in range(num_iterations):
                data = get_slice(i)[input_name].to(device)
                t0 = time()
                model(data)
                t1 = time()
                time_infer.append(t1 - t0)

    return predictions, time_infer


def process_result(batch_size, inference_time):
    inference_time = pp.three_sigma_rule(inference_time)
    average_time = pp.calculate_average_time(inference_time)
    latency = pp.calculate_latency(inference_time)
    fps = pp.calculate_fps(batch_size, latency)
    return average_time, latency, fps


def result_output(average_time, fps, latency):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))
    log.info('Latency : {0:.3f}'.format(latency))


def raw_result_output(average_time, fps, latency):
    print('{0:.3f},{1:.3f},{2:.3f}'.format(average_time, fps, latency))


def prepare_output(result, output_names, task):
    if task == 'feedforward':
        return {}
    if (output_names is None) or len(output_names) == 0:
        raise ValueError('The number of output tensors does not match the number of corresponding output names')
    if task == 'classification':
        return {output_names[0]: result.detach().numpy()}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        model_wrapper = PyTorchIOModelWrapper(create_dict_for_modelwrapper(args))
        data_transformer = PyTorchTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        if args.model_name is not None and args.model is None:
            model = load_model_from_module(args.model_name)
        elif args.model_name is None and args.model is not None:
            model = load_model_from_file(args.model)
        else:
            raise ValueError('Incorrect arguments.')

        device = get_device_to_infer(args.device)
        compiled_model = compile_model(model, device, args.model_type)

        log.info(f'Shape for input layer {args.input_name}: {args.input_shape}')

        log.info(f'Preparing input data {args.input}')
        io.prepare_input(compiled_model, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, inference_time = inference_pytorch(compiled_model, args.number_iter,
                                                   io.get_slice_input, args.input_name, args.inference_mode,
                                                   device)

        log.info('Computing performance metrics')
        average_time, latency, fps = process_result(args.batch_size, inference_time)

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
            result_output(average_time, fps, latency)
        else:
            raw_result_output(average_time, fps, latency)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
