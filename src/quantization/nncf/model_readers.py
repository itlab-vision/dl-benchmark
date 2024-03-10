import abc
import sys
import importlib
import ast
from pathlib import Path
from parameters import TVMReader


class NNCFModelReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self.model_name = self.args['ModelName']
        self.model_path = self.args['ModelJson']
        self.model_params = self.args['WeightsParams']
        self.input_name = self.args['InputName']
        self.output_name = self.args['OutputName']
        self.input_shape = ast.literal_eval(self.args['InputShape'])
        self.module = self.args['Module']
        self.device = self.args['Device']
        self._read_model()

    @abc.abstractmethod
    def _read_model(self):
        pass


class NNCFModelReaderTensorFLowFormat(NNCFModelReader):
    def __init__(self, log):
        super().__init__(log)
    
    def _read_model(self):
        sys.path.append(str(Path(__file__).parent.parent.parent))
        from src.model_converters.tf2tflite.tensorflow_common import (load_model, get_gpu_devices, is_gpu_available,  # noqa
                                                                      get_input_operation_name, restrisct_gpu_usage)  # noqa
        input_op_names = get_input_operation_name(self.input_name)
        self.model, _ = load_model(model_path=self.model_path,
                                   input_names=input_op_names,
                                   output_names=self.output_name,
                                   const_inputs=[],
                                   log=self._log)


class NNCFModelReaderONNXFormat(NNCFModelReader):
    def __init__(self, log):
        super().__init__(log)

    def _read_model(self):
        import onnx
        self.model = onnx.load(self.model_path)


class NNCFModelReaderPyTorchFormat(NNCFModelReader):
    def __init__(self, log):
        super().__init__(log)
    
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
                sys.path.append(str(Path(__file__).resolve().parents[3]))
                from inference.configs.tvm_configs.mask_rcnn_config import TraceWrapper, do_trace
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


    def _read_model(self):
        if self.model_path is not None:
            self.model = self.__get_model_from_path(self.model_path, self.input_shape)
        else:
            self.model = self.__get_model_from_module(self.model_name, self.input_shape,
                                                      self.model_params, self.module, self.device)