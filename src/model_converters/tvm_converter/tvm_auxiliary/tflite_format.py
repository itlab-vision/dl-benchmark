import importlib

Converter = importlib.import_module('converter').Converter


class TensorFlowLiteToTVMConverter(Converter):
    def __init__(self, args):
        self.tflite = importlib.import_module('tflite')
        super().__init__(args)
        self.framework = 'TFLite'

    def _get_tf_model(self, model_path):
        tflite_model_buf = open(model_path, 'rb').read()
        tflite_model = self.tflite.Model.GetRootAsModel(tflite_model_buf, 0)
        return tflite_model

    def _convert_model_from_framework(self):
        model_path = self.args['model_path']
        model_tf = self._get_tf_model(model_path)
        shape_dict = {self.args['input_name']: self.args['input_shape']}
        dtype = {self.args['input_name']: 'float32'}
        self.log.info('Creating graph module from TensorFlow model')
        model, params = self.tvm.relay.frontend.from_tflite(model_tf,
                                                            shape_dict=shape_dict,
                                                            dtype_dict=dtype)
        return model, params
