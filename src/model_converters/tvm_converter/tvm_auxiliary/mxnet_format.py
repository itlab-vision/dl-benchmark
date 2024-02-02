import importlib
from converter import TVMConverter


class TVMConverterMXNetFormat(TVMConverter):
    def __init__(self, args):
        self.mxnet = importlib.import_module('mxnet')
        self.gluoncv = importlib.import_module('gluoncv')
        super().__init__(args)

    @property
    def source_framework(self):
        return 'MXNet'

    def _get_device_for_framework(self):
        if self.device == 'CPU':
            return self.mxnet.cpu()
        else:
            raise ValueError(f'Device {self.device} is not supported. Supported devices: CPU')

    def _get_mxnet_network(self):
        context = self._get_device_for_framework()

        if ((self.model_name is not None)
                and (self.model_path is None)
                and (self.model_params is None)):
            self.log.info(f'Loading network \"{self.model_name}\" from GluonCV model zoo')
            net = self.gluoncv.model_zoo.get_model(self.model_name, pretrained=True, ctx=context)
            return net

        elif ((self.model_path is not None) and (self.model_params is not None)):
            self.log.info(f'Deserializing network from file ({self.model_path}, {self.model_params})')
            net = self.mxnet.gluon.nn.SymbolBlock.imports(
                self.model_path, [self.input_name], self.model_params, ctx=context)
            return net

        else:
            raise ValueError('Incorrect arguments.')

    def _convert_model_from_framework(self):
        net = self._get_mxnet_network()
        shape_dict = {self.input_name: self.input_shape}
        model, params = self.tvm.relay.frontend.from_mxnet(net, shape_dict)
        return model, params
