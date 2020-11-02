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


class intelcaffe_io_model_wrapper(io_model_wrapper):
    def get_input_layer_names(self, net):
        return net.inputs

    def get_input_layer_shape(self, net, layer_name):
        return net.blobs[layer_name].data.shape


class tensorflow_io_model_wrapper(io_model_wrapper):
    def __init__(self, args):
        self._shape = args.input_shape
        self._batch = args.batch_size

    def _create_list_with_input_shape(self):
        return [self._batch, self._shape[0], self._shape[1], self._shape[2]]

    def get_input_layer_names(self, graph):
        inputs = [x for x in graph.get_operations() if x.type == "Placeholder"]
        input_names = []
        for input in inputs:
            for output in input.outputs:
                input_names.append(output.name)
        return input_names

    def get_input_layer_shape(self, graph, layer_name):
        if self._shape is None:
            try:
                shape = graph.get_tensor_by_name(layer_name).shape.as_list()
            except Exception:
                raise ValueError('Couldn\'t get the correct shape. Try setting the \'input_shape\' parameter manually.')
        else:
            shape = self._create_list_with_input_shape()
        if shape[0] is None:
            shape[0] = self._batch
        if None in shape[1:]:
            raise ValueError('Invalid shape {}. Try setting the \'input_shape\' parameter manually.'.format(shape))
        return shape

    def get_outputs_layer_names(self, graph, outputs_names=None):
        if outputs_names:
            return outputs_names
        nodes_map = {}
        for node in graph.as_graph_def().node:
            for parent in node.input:
                nodes_map.update({parent: nodes_map.get(parent, []) + [node.name]})
        not_outputs_types = {'Const', 'Assign', 'NoOp', 'Placeholder', 'Assert'}
        names = [
            x.name.split('import/')[-1] for x in graph.as_graph_def().node
            if x.name not in nodes_map and x.op not in not_outputs_types
        ]
        if not names:
            raise ValueError('Output blobs in the graph cannot be found')
        return names
