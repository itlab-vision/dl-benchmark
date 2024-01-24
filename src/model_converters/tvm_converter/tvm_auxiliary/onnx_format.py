import importlib

Converter = importlib.import_module('src.model_converters.tvm_converter.tvm_auxiliary.converter').Converter


class ONNXToTVMConverter(Converter):
    def __init__(self, args):
        self.onnx = importlib.import_module('onnx')
        super().__init__(args)
        self.framework = 'ONNX'
        self.model_onnx = None

    def get_input_name(self):
        return self.model_onnx.graph.input[0].name

    def _convert_model_from_framework(self):
        model_path = self.args['model_path']
        input_shape = self.args['input_shape']
        model_onnx = self.onnx.load(model_path)
        self.model_onnx = model_onnx
        shape_dict = {model_onnx.graph.input[0].name: input_shape}
        model, params = self.tvm.relay.frontend.from_onnx(model_onnx, shape_dict)
        return model, params
