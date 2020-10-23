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
    def get_input_layer_names(self, graph):
        # graph == tf.compat.v1.get_default_graph()
        inputs = [x for x in graph.get_operations() if x.type == "Placeholder"]
        input_names = []
        for input in inputs:
            for output in input.outputs:
                input_names.append(output.name)
        return input_names

    # Должно работать не для всех моделей (resnet_50 - не раб)
    def get_input_layer_shape(self, graph, layer_name):
        # graph == tf.compat.v1.get_default_graph()
        shape = graph.get_tensor_by_name(layer_name).shape.as_list()
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
