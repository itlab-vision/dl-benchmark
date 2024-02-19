import importlib
from converter import TVMConverter


class TVMConverterTFLiteFormat(TVMConverter):
    def __init__(self, args):
        self.tflite = importlib.import_module('tflite')
        super().__init__(args)

    @property
    def source_framework(self):
        return 'TFLite'

    def _get_tf_model(self, model_path):
        tflite_model_buf = open(model_path, 'rb').read()
        tflite_model = self.tflite.Model.GetRootAsModel(tflite_model_buf, 0)
        return tflite_model

    def _convert_model_from_framework(self):
        model_tf = self._get_tf_model(self.model_path)
        shape_dict = {self.input_name: self.input_shape}
        dtype = {self.input_name: 'float32'}
        model, params = self.tvm.relay.frontend.from_tflite(model_tf,
                                                            shape_dict=shape_dict,
                                                            dtype_dict=dtype)
        return model, params
