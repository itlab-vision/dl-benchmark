import importlib
from converter import TVMConverter


class TVMConverterCaffeFormat(TVMConverter):
    def __init__(self, args):
        self.caffe = importlib.import_module('caffe')
        super().__init__(args)
        self.text_format = importlib.import_module('google.protobuf.text_format')

    @property
    def source_framework(self):
        return 'Caffe'

    def _convert_model_from_framework(self):
        shape_dict = {self.input_name: self.input_shape}
        dtype_dict = {self.input_name: 'float32'}
        init_net = self.caffe.proto.caffe_pb2.NetParameter()
        predict_net = self.caffe.proto.caffe_pb2.NetParameter()

        with open(self.model_path, 'r') as f:
            self.text_format.Merge(f.read(), predict_net)

        with open(self.model_params, 'rb') as f:
            init_net.ParseFromString(f.read())

        model, params = self.tvm.relay.frontend.from_caffe(init_net,
                                                           predict_net,
                                                           shape_dict,
                                                           dtype_dict)
        return model, params
