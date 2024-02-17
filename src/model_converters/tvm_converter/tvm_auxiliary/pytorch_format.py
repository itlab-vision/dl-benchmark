import importlib
import sys
from pathlib import Path
from converter import TVMConverter


class TVMConverterPyTorchFormat(TVMConverter):
    def __init__(self, args):
        self.torch = importlib.import_module('torch')
        super().__init__(args)

    @property
    def source_framework(self):
        return 'PyTorch'

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
            if self.model_name == 'maskrcnn_resnet50_fpn':
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
        if self.model_path is not None:
            return self.__get_model_from_path(self.model_path, self.input_shape)
        else:
            return self.__get_model_from_module(self.model_name, self.input_shape,
                                                self.model_params, self.module, self.device)

    def _convert_model_from_framework(self):
        scripted_model = self._get_pytorch_model()
        shape_list = [(self.input_name, self.input_shape)]
        model, params = self.tvm.relay.frontend.from_pytorch(scripted_model, shape_list)
        return model, params
