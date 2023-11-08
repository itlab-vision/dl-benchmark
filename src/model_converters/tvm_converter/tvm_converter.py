import logging as log
import tvm
import importlib
import abc
import warnings


class Converter(metaclass=abc.ABCMeta):
    def __init__(self, args):
        self.args = args
        self.graph = None
        self.mod = None
        self.params = None
        self.framework = 'tvm'

    @abc.abstractmethod
    def _get_device_for_framework(self):
        pass

    @abc.abstractmethod
    def _convert_model_from_framework(self, target, dev):
        pass

    def _get_target_device(self, task='Inference'):
        device = self.args['device']
        if device == 'CPU':
            log.info(f'{task} will be executed on {device}')
            target = tvm.target.Target('llvm')
            dev = tvm.cpu(0)
        return target, dev

    def get_tvm_model(self):
        target, dev = self._get_target_device()
        log.info(f'Get TVM model from {self.framework} model')
        self.mod, self.params = self._convert_model_from_framework(target, dev)
        return self.mod, self.params

    def save_tvm_model(self):
        model_name = self.args['model_name']
        log.info(f'Saving weights of the model {model_name}')
        with open(f'{model_name}.params', 'wb') as fo:
            fo.write(tvm.relay.save_param_dict(self.params))
        log.info(f'Saving model {model_name}')
        with open(f'{model_name}.json', 'w') as fo:
            fo.write(tvm.ir.save_json(self.mod))

    def get_graph_module(self):
        target, dev = self._get_target_device()
        log.info(f'Get TVM model from {self.framework} model')
        mod, params = self._convert_model_from_framework(target, dev)
        log.info(f'Creating graph module from {self.framework} model')
        with tvm.transform.PassContext(opt_level=self.args['opt_level']):
            lib = tvm.relay.build(mod, target=target, params=params)
        self.graph = tvm.contrib.graph_executor.GraphModule(lib['default'](dev))
        return self.graph


class PyTorchToTVMConverter(Converter):
    def __init__(self, args):
        super().__init__(args)
        self.framework = 'Pytorch'

    def _get_device_for_framework(self):
        return super()._get_device_for_framework()

    def _get_pytorch_model(self):
        import torch
        model_name = self.args['model_name']
        module = self.args['module']
        model_path = self.args['model_path']
        input_shape = self.args['input_shape']
        weights = self.args['model_params']
        device = self.args['device']
        input_data = torch.randn(input_shape)
        if model_path is not None:
            log.info(f'Loading model from path {model_path}')
            file_type = model_path.split('.')[-1]
            supported_extensions = ['pt']
            if file_type not in supported_extensions:
                raise ValueError(f'The file type {file_type} is not supported')
            model = torch.load(model_path)
            model = model.eval()
            scripted_model = torch.jit.trace(model, input_data).eval()
            return scripted_model
        else:
            log.info(f'Loading model {model_name} from module')
            model_cls = importlib.import_module(module).__getattribute__(model_name)

            if weights is None or weights == '':
                log.info('Loading pretrained model')
                model = model_cls(weights=True)
                scripted_model = torch.jit.trace(model, input_data).eval()
                return scripted_model
            else:
                log.info(f'Loading model with weights from file {weights}')
                model = model_cls()
                checkpoint = torch.load(weights, map_location=device.lower())
                model.load_state_dict(checkpoint, strict=False)
                model = model.eval()
                scripted_model = torch.jit.trace(model, input_data).eval()
                return scripted_model

    def _convert_model_from_framework(self, target, dev):
        input_shape = self.args['input_shape']
        scripted_model = self._get_pytorch_model()
        input_name = self.args['input_name']
        shape_list = [(input_name, input_shape)]
        model, params = tvm.relay.frontend.from_pytorch(scripted_model, shape_list)
        return model, params


class ONNXToTVMConverter(Converter):
    def __init__(self, args):
        super().__init__(args)
        self.framework = 'ONNX'

    def _get_device_for_framework(self):
        return super()._get_device_for_framework()

    def _convert_model_from_framework(self, target, dev):
        import onnx
        model_path = self.args['model_path']
        model_onnx = onnx.load(model_path)
        shape_dict = {self.args['input_name']: self.args['input_shape']}
        model, params = tvm.relay.frontend.from_onnx(model_onnx, shape_dict)
        return model, params


class MXNetToTVMConverter(Converter):
    def __init__(self, args):
        super().__init__(args)
        self.framework = 'MXNet'

    def _get_device_for_framework(self):
        import mxnet
        device = self.args['device']
        if device == 'CPU':
            return mxnet.cpu()
        elif device == 'NVIDIA_GPU':
            return mxnet.gpu()
        else:
            log.info(f'The device {device} is not supported')
            raise ValueError('The device is not supported')

    def _get_mxnet_network(self):
        import mxnet
        import gluoncv
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
        shape_dict = {self.args['input_name']: self.args['input_shape']}
        log.info('Creating graph module from MXNet model')
        model, params = tvm.relay.frontend.from_mxnet(net, shape_dict)
        return model, params


class TVMConverter(Converter):
    def __init__(self, args):
        super().__init__(args)
        self.framework = 'TVM'

    def _get_deserialized_tvm_model(self):
        model_path = self.args['model_path']
        model_params = self.args['model_params']
        with open(model_params, 'rb') as fo:
            params = tvm.relay.load_param_dict(fo.read())

        with open(model_path, 'r') as fo:
            mod = fo.read()

        self.mod = tvm.ir.load_json(mod)
        self.params = params
        return self.mod, self.params

    def _get_device_for_framework(self):
        return super()._get_device_for_framework()

    def _convert_model_from_framework(self, target, dev):
        return self._get_deserialized_tvm_model()
