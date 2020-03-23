import abc


class io_model_wrapper:
    @abc.abstractmethod
    def get_input_layer_names(self, net):
        pass


    @abc.abstractmethod
    def get_input_layer_shape(self, net, layer_name):
        pass


class openvino_io_model_wrapper(io_model_wrapper):
    def get_input_layer_names(self, net):
        return list(net.inputs.keys())


    def get_input_layer_shape(self, net, layer_name):
        return net.inputs[layer_name].shape
