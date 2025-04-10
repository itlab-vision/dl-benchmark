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

    def __get_model_from_path(self):
        self.log.info(f'Loading model from path {self.model_path}')
        file_type = self.model_path.split('.')[-1]
        supported_extensions = ['pt']
        if file_type not in supported_extensions:
            raise ValueError(f'The file type {file_type} is not supported')
        model = self.torch.load(self.model_path)
        model = model.eval()
        return self._script_model(model)

    def __get_model_from_module(self):
        self.log.info(f'Loading model {self.model_name} from module')
        model_cls = importlib.import_module(self.module).__getattribute__(self.model_name)
        if self.model_params is None or self.model_params == '':
            self.log.info('Loading pretrained model')
            if self.model_name == 'maskrcnn_resnet50_fpn':
                sys.path.append(str(Path(__file__).resolve().parents[3]))
                from inference.configs.tvm_configs.mask_rcnn_config import TraceWrapper
                model = TraceWrapper(model_cls(pretrained=True))
            else:
                model = model_cls(weights=True)
        else:
            self.log.info(f'Loading model with weights from file {self.model_params}')
            model = model_cls()
            checkpoint = self.torch.load(self.model_params, map_location=self.device.lower())
            model.load_state_dict(checkpoint, strict=False)
            model = model.eval()
        return self._script_model(model)

    def _script_model(self, model):
        input_data = self.torch.randn(self.input_shape)
        if self.high_level_ir == 'relay':
            if self.model_name == 'maskrcnn_resnet50_fpn':
                with self.torch.no_grad():
                    _ = model(input_data)
                    from inference.configs.tvm_configs.mask_rcnn_config import do_trace
                    scripted_model = do_trace(model, input_data)
                return scripted_model
            else:
                scripted_model = self.torch.jit.trace(model, input_data).eval()
                return scripted_model
        elif self.high_level_ir == 'relax':
            from torch import fx
            return fx.symbolic_trace(model)

    def _get_pytorch_model(self):
        if self.model_path is not None:
            return self.__get_model_from_path()
        else:
            return self.__get_model_from_module()

    def _convert_model_from_framework(self):
        scripted_model = self._get_pytorch_model()
        if self.high_level_ir == 'relay':
            shape_list = [(self.input_name, self.input_shape)]
            model, params = self.tvm.relay.frontend.from_pytorch(scripted_model, shape_list)
            return model, params
        elif self.high_level_ir == 'relax':
            input_info = [(self.input_shape, 'float32')]
            from tvm.relax.frontend.torch import from_fx
            from tvm.relax.frontend import detach_params
            model = from_fx(scripted_model, input_info)
            model, params = detach_params(model)
            return model, params
        else:
            raise ValueError(f'Intermediate representation {self.high_level_ir} is not supported')
