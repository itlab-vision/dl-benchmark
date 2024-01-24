import importlib
import sys
from pathlib import Path


Converter = importlib.import_module('src.model_converters.tvm_converter.tvm_auxiliary.converter').Converter


class PyTorchToTVMConverter(Converter):
    def __init__(self, args):
        self.torch = importlib.import_module('torch')
        super().__init__(args)
        self.framework = 'PyTorch'

    def __get_model_from_path(self, model_path, input_shape):
        self.log.info(f'Loading model from path {model_path}')
        input_data = self.torch.randn(input_shape)
        file_type = model_path.split('.')[-1]
        supported_extensions = ['pt']
        if file_type not in supported_extensions:
            raise ValueError(f'The file type {file_type} is not supported')
        model = self.torch.load(model_path)
        model = model.eval()
        scripted_model = self.torch.jit.trace(model, input_data).eval()
        return scripted_model

    def __get_model_from_module(self, model_name,
                                input_shape, weights,
                                module, device):
        self.log.info(f'Loading model {model_name} from module')
        input_data = self.torch.randn(input_shape)
        model_cls = importlib.import_module(module).__getattribute__(model_name)
        if weights is None or weights == '':
            self.log.info('Loading pretrained model')
            if self.args['model_name'] == 'maskrcnn_resnet50_fpn':
                sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
                from src.inference.configs.tvm_configs.mask_rcnn_config import TraceWrapper, do_trace
                model = TraceWrapper(model_cls(pretrained=True))
                model.eval()
                with self.torch.no_grad():
                    _ = model(input_data)
                    script_module = do_trace(model, input_data)
                return script_module
            else:
                model = model_cls(weights=True)
                scripted_model = self.torch.jit.trace(model, input_data).eval()
                return scripted_model
        else:
            self.log.info(f'Loading model with weights from file {weights}')
            model = model_cls()
            checkpoint = self.torch.load(weights, map_location=device.lower())
            model.load_state_dict(checkpoint, strict=False)
            model = model.eval()
            scripted_model = self.torch.jit.trace(model, input_data).eval()
            return scripted_model

    def _get_pytorch_model(self):
        model_name = self.args['model_name']
        module = self.args['module']
        model_path = self.args['model_path']
        input_shape = self.args['input_shape']
        weights = self.args['model_params']
        device = self.args['device']
        if model_path is not None:
            return self.__get_model_from_path(model_path, input_shape)
        else:
            return self.__get_model_from_module(model_name, input_shape,
                                                weights, module, device)

    def _convert_model_from_framework(self):
        input_shape = self.args['input_shape']
        scripted_model = self._get_pytorch_model()
        input_name = self.args['input_name']
        shape_list = [(input_name, input_shape)]
        model, params = self.tvm.relay.frontend.from_pytorch(scripted_model, shape_list)
        return model, params