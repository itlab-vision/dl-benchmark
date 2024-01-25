import importlib

Converter = importlib.import_module('converter').Converter


class MXNetToTVMConverter(Converter):
    def __init__(self, args):
        self.mxnet = importlib.import_module('mxnet')
        self.gluoncv = importlib.import_module('gluoncv')
        super().__init__(args)
        self.framework = 'MXNet'

    def _get_device_for_framework(self):
        device = self.args['device']
        if device == 'CPU':
            return self.mxnet.cpu()
        else:
            raise ValueError(f'Device {device} is not supported. Supported devices: CPU')

    def _get_mxnet_network(self):
        model_name = self.args['model_name']
        model_path = self.args['model_path']
        weights = self.args['model_params']
        context = self._get_device_for_framework()

        if ((model_name is not None)
                and (model_path is None)
                and (weights is None)):
            self.log.info(f'Loading network \"{model_name}\" from GluonCV model zoo')
            net = self.gluoncv.model_zoo.get_model(model_name, pretrained=True, ctx=context)
            return net

        elif ((model_path is not None) and (weights is not None)):
            self.log.info(f'Deserializing network from file ({model_path}, {weights})')
            net = self.mxnet.gluon.nn.SymbolBlock.imports(
                model_path, [self.args['input_name']], weights, ctx=context)
            return net

        else:
            raise ValueError('Incorrect arguments.')

    def _convert_model_from_framework(self):
        net = self._get_mxnet_network()
        shape_dict = {self.args['input_name']: self.args['input_shape']}
        model, params = self.tvm.relay.frontend.from_mxnet(net, shape_dict)
        return model, params
