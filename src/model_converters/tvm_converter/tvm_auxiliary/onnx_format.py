import importlib
from converter import TVMConverter


class TVMConverterONNXFormat(TVMConverter):
    def __init__(self, args):
        self.onnx = importlib.import_module('onnx')
        super().__init__(args)
        self.model_onnx = None

    @property
    def source_framework(self):
        return 'ONNX'

    def get_input_name(self):
        return self.model_onnx.graph.input[0].name

    def _convert_model_from_framework(self):
        model_onnx = self.onnx.load(self.model_path)
        self.model_onnx = model_onnx
        shape_dict = {self.get_input_name(): self.input_shape}
        if self.high_level_ir == 'relay':
            model, params = self.tvm.relay.frontend.from_onnx(model_onnx, shape_dict)
        elif self.high_level_ir == 'relax':
            from tvm.relax.frontend.onnx import from_onnx
            from tvm.relax.frontend import detach_params
            model = from_onnx(model_onnx, shape_dict)
            model, params = detach_params(model)
        else:
            raise ValueError(f'Intermediate representation {self.high_level_ir} is not supported')
        return model, params
