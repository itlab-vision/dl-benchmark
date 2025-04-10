import importlib
import abc
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


class TVMConverter(metaclass=abc.ABCMeta):
    def __init__(self, args):
        self.model_name = args.get('model_name', None)
        self.model_path = args.get('model_path', None)
        self.model_params = args.get('model_params', None)
        self.input_name = args.get('input_name', None)
        self.input_shape = args.get('input_shape', None)
        self.device = args.get('device', None)
        self.opt_level = args.get('opt_level', None)
        self.target_str = args.get('target', None)
        self.module = args.get('module', None)
        self.high_level_ir = args.get('high_level_ir', None)
        self.vm = args.get('vm', None)

        self.output_dir = args.get('output_dir', None)
        self.lib_name = args.get('lib_name', None)

        self.mod_type = self.get_file_type(self.model_path)
        self.params_type = self.get_file_type(self.model_params)

        self.graph = None
        self.mod = None
        self.params = None
        self.log = log
        self.tvm = importlib.import_module('tvm')
        if self.high_level_ir == 'relay':
            self.tvm.relay = importlib.import_module('tvm.relay')
        elif self.high_level_ir == 'relax':
            self.tvm.relax = importlib.import_module('tvm.relax')
        else:
            raise ValueError(f'Intermediate representation {self.high_level_ir} is not supported')
        self.graph_executor = importlib.import_module('tvm.contrib.graph_executor')

    def get_file_type(self, file_path):
        if file_path is not None:
            return Path(file_path).suffix[1:]
        else:
            return None

    @abc.abstractmethod
    def _convert_model_from_framework(self):
        pass

    @property
    @abc.abstractmethod
    def source_framework(self):
        return 'TVM'

    @staticmethod
    def get_converter(args):
        framework = args['source_framework'].lower()
        if framework == 'pytorch':
            from pytorch_format import TVMConverterPyTorchFormat
            return TVMConverterPyTorchFormat(args)
        elif framework == 'onnx':
            from onnx_format import TVMConverterONNXFormat
            return TVMConverterONNXFormat(args)
        elif framework == 'mxnet':
            from mxnet_format import TVMConverterMXNetFormat
            return TVMConverterMXNetFormat(args)
        elif framework == 'tflite':
            from tflite_format import TVMConverterTFLiteFormat
            return TVMConverterTFLiteFormat(args)
        elif framework == 'caffe':
            from caffe_format import TVMConverterCaffeFormat
            return TVMConverterCaffeFormat(args)
        elif framework == 'tvm':
            from tvm_format import TVMConverterTVMFormat
            return TVMConverterTVMFormat(args)

    def _get_target_device(self, task='Inference'):
        if self.device == 'CPU':
            self.log.info(f'{task} will be executed on {self.device}')
            try:
                target = self.tvm.target.Target(self.target_str)
            except AttributeError:
                target = None
            dev = self.tvm.cpu(0)
        else:
            raise ValueError(f'Device {self.device} is not supported. Supported devices: CPU')
        return target, dev

    def get_tvm_model(self):
        self.log.info(f'Get TVM model from {self.source_framework} model')
        self.mod, self.params = self._convert_model_from_framework()
        return self.mod, self.params

    def save_tvm_model(self):
        if self.output_dir is None:
            self.output_dir = os.getcwd()

        self.log.info(f'Saving model \"{self.model_name}\" to \"{self.output_dir}\"')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.log.info(f'Saving weights of the model {self.model_name}')
        with open(f'{self.output_dir}/{self.model_name}.params', 'wb') as fo:
            fo.write(self.tvm.runtime.save_param_dict(self.params))

        self.log.info(f'Saving model {self.model_name}')
        with open(f'{self.output_dir}/{self.model_name}.json', 'w') as fo:
            fo.write(self.tvm.ir.save_json(self.mod))

    def get_graph_module_from_relay_lib(self, lib):
        _, dev = self._get_target_device()
        self.graph = self.graph_executor.GraphModule(lib['default'](dev))
        return self.graph

    def get_graph_module_from_relax_lib(self, lib):
        if self.vm:
            _, dev = self._get_target_device()
            des_vm = self.tvm.relax.VirtualMachine(lib, dev)
            return des_vm
        else:
            raise ValueError('Intermediate representation Relax supports execution only via VirtualMachine')

    def get_lib(self):
        target, _ = self._get_target_device()
        model = self._convert_model_from_framework()

        self.log.info('Model compilation')
        if self.high_level_ir == 'relay':
            return self.__get_lib_from_relay(target, model)
        elif self.high_level_ir == 'relax':
            return self.__get_lib_from_relax(target, model)
        else:
            raise ValueError(f'Intermediate representation {self.high_level_ir} is not supported')

    def __get_lib_from_relay(self, target, model):
        if self.vm:
            rly_vm = self.tvm.relay.vm
            with self.tvm.transform.PassContext(opt_level=self.opt_level):
                executable = rly_vm.compile(model[0], target=target, params=model[1])
            code, lib = executable.save()
            return code, lib
        else:
            with self.tvm.transform.PassContext(opt_level=self.opt_level):
                lib = self.tvm.relay.build(model[0], target=target, params=model[1])
            return [lib]

    def __get_lib_from_relax(self, target, model):
        if self.vm:
            with self.tvm.transform.PassContext(opt_level=self.opt_level):
                lib = self.tvm.relax.build(model[0], target=target, params=model[1])
            return [lib]
        else:
            raise ValueError('Intermediate representation Relax supports execution only via VirtualMachine')

    def export_lib(self):
        if self.output_dir is None:
            self.output_dir = os.getcwd()

        self.log.info(f'Saving library of model \"{self.lib_name}\" to \"{self.output_dir}\"')
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        lib = self.get_lib()
        if len(lib) == 1:
            lib[0].export_library(f'{self.output_dir}/{self.lib_name}')
        else:
            lib[1].export_library(f'{self.output_dir}/{self.lib_name}')
            lib_name = Path(self.lib_name).with_suffix('')

            with open(f'{self.output_dir}/{lib_name}.ro', 'wb') as fo:
                fo.write(lib[0])

    def get_graph_module_from_relay(self, mod, params, target, dev):
        if self.vm:
            vm = self.tvm.runtime.vm
            rly_vm = self.tvm.relay.vm
            if self.mod_type == 'so' and self.params_type == 'ro':
                executable = vm.Executable.load_exec(params, mod)
            else:
                with self.tvm.transform.PassContext(opt_level=self.opt_level):
                    executable = rly_vm.compile(mod, target=target, params=params)
            des_vm = vm.VirtualMachine(executable, dev)
            return des_vm
        else:
            with self.tvm.transform.PassContext(opt_level=self.opt_level):
                lib = self.tvm.relay.build(mod, target=target, params=params)
            self.graph = self.graph_executor.GraphModule(lib['default'](dev))
            return self.graph

    def get_graph_module_from_relax(self, mod, params, target, dev):
        if self.vm:
            with self.tvm.transform.PassContext(opt_level=self.opt_level):
                executable = self.tvm.relax.build(mod, target=target, params=params)
            des_vm = self.tvm.relax.VirtualMachine(executable, dev)
            return des_vm
        else:
            raise ValueError('Intermediate representation Relax supports execution only via VirtualMachine')

    def get_graph_module(self):
        target, dev = self._get_target_device()
        self.log.info(f'Get TVM model from {self.source_framework} model')
        model = self._convert_model_from_framework()

        self.log.info(f'Creating graph module from {self.source_framework} model')
        if self.high_level_ir == 'relay':
            if len(model) == 2:
                return self.get_graph_module_from_relay(model[0], model[1], target, dev)
            return self.get_graph_module_from_relay_lib(model[0])
        if self.high_level_ir == 'relax':
            if len(model) == 2:
                return self.get_graph_module_from_relax(model[0], model[1], target, dev)
            return self.get_graph_module_from_relax_lib(model[0])
        raise ValueError(f'Intermediate representation {self.high_level_ir} is not supported')
