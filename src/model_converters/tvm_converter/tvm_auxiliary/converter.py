import importlib
import abc
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


class Converter(metaclass=abc.ABCMeta):
    def __init__(self, args):
        self.args = args
        self.graph = None
        self.mod = None
        self.params = None
        self.log = log
        self.framework = 'tvm'
        self.tvm = importlib.import_module('tvm')
        self.graph_executor = importlib.import_module('tvm.contrib.graph_executor')

    @abc.abstractmethod
    def _convert_model_from_framework(self):
        pass

    @staticmethod
    def get_converter(args):
        framework = args['framework'].lower()
        if framework == 'pytorch':
            converter = importlib.import_module('pytorch_format')
            return converter.PyTorchToTVMConverter(args)
        elif framework == 'onnx':
            converter = importlib.import_module('onnx_format')
            return converter.ONNXToTVMConverter(args)
        elif framework == 'mxnet':
            converter = importlib.import_module('mxnet_format')
            return converter.MXNetToTVMConverter(args)
        elif framework == 'tflite':
            converter = importlib.import_module('tflite_format')
            return converter.TensorFlowLiteToTVMConverter(args)
        elif framework == 'caffe':
            converter = importlib.import_module('caffe_format')
            return converter.CaffeToTVMConverter(args)
        elif framework == 'tvm':
            converter = importlib.import_module('tvm_format')
            return converter.TVMConverter(args)

    def _get_target_device(self, task='Inference'):
        device = self.args['device']
        target_str = self.args['target']
        if device == 'CPU':
            self.log.info(f'{task} will be executed on {device}')
            try:
                target = self.tvm.target.Target(target_str)
            except AttributeError:
                target = None
            dev = self.tvm.cpu(0)
        else:
            raise ValueError(f'Device {device} is not supported. Supported devices: CPU')
        return target, dev

    def get_tvm_model(self):
        self.log.info(f'Get TVM model from {self.framework} model')
        self.mod, self.params = self._convert_model_from_framework()
        return self.mod, self.params

    def save_tvm_model(self):
        model_name = self.args['model_name']
        path_save_model = self.args['output_dir']

        if path_save_model is None:
            path_save_model = os.getcwd()

        self.log.info(f'Saving model \"{model_name}\" to \"{path_save_model}\"')
        if not os.path.exists(path_save_model):
            os.mkdir(path_save_model)

        self.log.info(f'Saving weights of the model {model_name}')
        with open(f'{path_save_model}/{model_name}.params', 'wb') as fo:
            fo.write(self.tvm.relay.save_param_dict(self.params))

        self.log.info(f'Saving model {model_name}')
        with open(f'{path_save_model}/{model_name}.json', 'w') as fo:
            fo.write(self.tvm.ir.save_json(self.mod))

    def get_graph_module_from_lib(self, lib):
        _, dev = self._get_target_device()
        self.graph = self.graph_executor.GraphModule(lib['default'](dev))
        return self.graph

    def get_lib(self):
        target, _ = self._get_target_device()
        model = self._convert_model_from_framework()

        self.log.info('Model compilation')
        if self.args['vm']:
            rly_vm = self.tvm.relay.vm
            with self.tvm.transform.PassContext(opt_level=self.args['opt_level']):
                executable = rly_vm.compile(model[0], target=target, params=model[1])
            code, lib = executable.save()
            return code, lib
        else:
            with self.tvm.transform.PassContext(opt_level=self.args['opt_level']):
                lib = self.tvm.relay.build(model[0], target=target, params=model[1])
            return [lib]

    def export_lib(self):
        path_save_lib = self.args['output_dir']
        lib_name = self.args['lib_name']
        if path_save_lib is None:
            path_save_lib = os.getcwd()

        self.log.info(f'Saving library of model \"{lib_name}\" to \"{path_save_lib}\"')
        if not os.path.exists(path_save_lib):
            os.mkdir(path_save_lib)

        lib = self.get_lib()
        if len(lib) == 1:
            lib[0].export_library(f'{path_save_lib}/{lib_name}')
        else:
            lib[1].export_library(f'{path_save_lib}/{lib_name}')
            lib_name = Path(lib_name).with_suffix('')

            with open(f'{path_save_lib}/{lib_name}.ro', 'wb') as fo:
                fo.write(lib[0])

    def get_graph_module_from_vm(self, mod, params, target, dev):
        rly_vm = self.tvm.relay.vm
        vm = self.tvm.runtime.vm
        if self.mod_type == 'so' and self.params_type == 'ro':
            executable = vm.Executable.load_exec(params, mod)
        else:
            with self.tvm.transform.PassContext(opt_level=self.args['opt_level']):
                executable = rly_vm.compile(mod, target=target, params=params)
        des_vm = vm.VirtualMachine(executable, dev)
        return des_vm

    def get_graph_module_from_relay(self, mod, params, target, dev):
        with self.tvm.transform.PassContext(opt_level=self.args['opt_level']):
            lib = self.tvm.relay.build(mod, target=target, params=params)
        self.graph = self.graph_executor.GraphModule(lib['default'](dev))
        return self.graph

    def get_graph_module(self):
        target, dev = self._get_target_device()
        self.log.info(f'Get TVM model from {self.framework} model')
        model = self._convert_model_from_framework()

        self.log.info(f'Creating graph module from {self.framework} model')
        if len(model) == 2:
            if self.args['vm']:
                return self.get_graph_module_from_vm(model[0], model[1], target, dev)
            else:
                return self.get_graph_module_from_relay(model[0], model[1], target, dev)
        else:
            return self.get_graph_module_from_lib(model[0])
