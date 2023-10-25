import tvm
import logging as log
from scipy.special import softmax
import abc


class TVMConverter(metaclass=abc.ABCMeta):
    def __init__(self, args):
        self.args = args
        self.net = None

    @abc.abstractmethod
    def _get_device_for_framework(self):
        pass

    @abc.abstractmethod
    def _convert_model_from_framework(self, target, dev):
        pass

    def _get_target_device(self):
        device = self.args['device']
        if device == 'CPU':
            log.info(f'Inference will be executed on {device}')
            target = tvm.target.Target('llvm')
            dev = tvm.cpu(0)
        return target, dev

    def get_graph_module(self):
        target, dev = self._get_target_device()
        module = self._convert_model_from_framework(target, dev)
        return module


def create_dict_for_converter_mxnet(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'device': args.device,
    }
    return dictionary


def create_dict_for_converter_onnx(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'device': args.device,
    }
    return dictionary


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


def prepare_output(result, task, output_names):
    if task == 'feedforward':
        return {}
    if task == 'classification':
        return {output_names[0]: softmax(result.asnumpy())}
