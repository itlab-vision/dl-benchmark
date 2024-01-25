import importlib

Converter = importlib.import_module('converter').Converter


class CaffeToTVMConverter(Converter):
    def __init__(self, args):
        self.caffe = importlib.import_module('caffe')
        super().__init__(args)
        self.text_format = importlib.import_module('google.protobuf.text_format')
        self.framework = 'Caffe'

    def _convert_model_from_framework(self):
        model_path = self.args['model_path']
        model_params = self.args['model_params']
        shape_dict = {self.args['input_name']: self.args['input_shape']}
        dtype_dict = {self.args['input_name']: 'float32'}
        init_net = self.caffe.proto.caffe_pb2.NetParameter()
        predict_net = self.caffe.proto.caffe_pb2.NetParameter()

        with open(model_path, 'r') as f:
            self.text_format.Merge(f.read(), predict_net)

        with open(model_params, 'rb') as f:
            init_net.ParseFromString(f.read())

        model, params = self.tvm.relay.frontend.from_caffe(init_net,
                                                           predict_net,
                                                           shape_dict,
                                                           dtype_dict)
        return model, params
