import abc


class IOModelWrapper:
    @abc.abstractmethod
    def get_input_layer_names(self, model):
        pass

    @abc.abstractmethod
    def get_input_layer_shape(self, model, layer_name):
        pass

    @abc.abstractmethod
    def get_input_layer_dtype(self, model, layer_name):
        pass


class OpenVINOIOModelWrapper(IOModelWrapper):
    def get_input_layer_names(self, model):
        names = []
        for input_ in model.inputs:
            names.append(input_.get_any_name())
        return names

    def get_input_layer_shape(self, model, node_name):
        for input_ in model.inputs:
            if node_name == input_.get_any_name():
                return input_.get_shape()
        return None

    def get_input_layer_dtype(self, model, node_name):
        from openvino.runtime.utils.types import get_dtype
        for input_ in model.inputs:
            if node_name == input_.get_any_name():
                return get_dtype(input_.get_element_type())


class IntelCaffeIOModelWrapper(IOModelWrapper):
    def get_input_layer_names(self, model):
        return model.inputs

    def get_input_layer_shape(self, model, layer_name):
        return model.blobs[layer_name].data.shape

    def get_input_layer_dtype(self, model, layer_name):
        return model.blobs[layer_name].data.dtype


class TensorFlowIOModelWrapper(IOModelWrapper):
    def __init__(self, args):
        self._shape = args.input_shape
        self._batch = args.batch_size
        self._input_name = args.input_name

    def _create_list_with_input_shape(self):
        return [self._batch, self._shape[0], self._shape[1], self._shape[2]]

    def get_input_layer_names(self, graph):
        if self._input_name:
            return self._input_name
        inputs = [x for x in graph.get_operations() if x.type == 'Placeholder']
        input_names = []
        for input_ in inputs:
            for output in input_.outputs:
                input_names.append(output.name)
        return input_names

    def get_input_layer_shape(self, graph, layer_name):
        if self._shape is None:
            try:
                shape = graph.get_tensor_by_name(layer_name).shape.as_list()
            except Exception:
                raise ValueError('Could not get the correct shape. '
                                 'Try setting the "input_shape" parameter manually.')
        else:
            shape = self._create_list_with_input_shape()
        if shape[0] is None:
            shape[0] = self._batch
        if None in shape[1:]:
            raise ValueError(f'Invalid shape {shape}. Try setting the "input_shape" parameter manually.')
        return shape

    @staticmethod
    def get_outputs_layer_names(graph, outputs_names=None):
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

    def get_input_layer_dtype(self, graph, layer_name):
        return graph.get_tensor_by_name(layer_name).dtype.as_numpy_dtype


class TensorFlowLiteIOModelWrapper(IOModelWrapper):
    def __init__(self, input_shapes, batch_size):
        self._shapes = input_shapes
        self._batch = batch_size
        self._input_names = input_shapes.keys()

    def get_input_layer_names(self, interpreter):
        if self._input_names:
            return list(self._input_names)
        inputs = interpreter.get_input_details()
        input_names = []
        for input_ in inputs:
            input_names.append(input_['name'])
        return input_names

    def get_input_layer_shape(self, interpreter, layer_name):
        if not self._shapes:
            try:
                inputs = interpreter.get_input_details()
                for input_ in inputs:
                    if layer_name == input_['name']:
                        shape = input_['shape']
                        break
            except Exception:
                raise ValueError('Could not get the correct shape. '
                                 'Try setting the "input_shape" parameter manually.')
        else:
            shape = list(self._shapes[layer_name])
        shape[0] = self._batch
        if None in shape[1:]:
            raise ValueError(f'Invalid shape {shape}. Try setting the "input_shape" parameter manually.')
        return shape

    @staticmethod
    def get_outputs_layer_names(interpreter, outputs_names=None):
        if outputs_names:
            return outputs_names
        outputs = interpreter.get_output_details()
        output_names = []
        for output_ in outputs:
            output_names.append(output_['name'])
        if not output_names:
            raise ValueError('Output blobs in the graph cannot be found')
        return output_names

    def get_input_layer_dtype(self, interpreter, layer_name):
        inputs = interpreter.get_input_details()
        for input_ in inputs:
            if layer_name == input_['name']:
                return input_['dtype']


class MXNetIOModelWrapper(IOModelWrapper):
    def __init__(self, args):
        # model wrapper supports only one input (batch of images)
        self._input_names = [args['input_name']]
        self._input_shapes = [args['input_shape']]
        self._model_name = args['model_name']

    def get_input_layer_names(self, model):
        return self._input_names

    def get_input_layer_shape(self, model, layer_name):
        return self._input_shapes[0]

    def get_input_layer_dtype(self, model, layer_name):
        import numpy as np
        return np.float32

    def get_model_name(self):
        return self._model_name


class OpenCVIOModelWrapper(IOModelWrapper):
    def __init__(self, args):
        self._input_name = [args['input_layer_name']]
        self._input_shape = [args['input_layer_shape']]

    def get_input_layer_names(self, model):
        return self._input_name

    def get_input_layer_shape(self, model, layer_name):
        return self._input_shape[0]

    def get_input_layer_dtype(self, model, layer_name):
        from numpy import float32
        return float32


class PyTorchIOModelWrapper(IOModelWrapper):
    def __init__(self, input_shapes, batch_size, tensor_rt_dtype, custom_precision, custom_input_type):
        self._shapes = input_shapes
        self._batch = batch_size
        self._input_names = input_shapes.keys()
        self._tensor_rt_dtype = tensor_rt_dtype
        self._custom_precision = custom_precision
        self._custom_input_type = custom_input_type

    def get_input_layer_names(self, model):
        return list(self._input_names)

    def get_input_layer_shape(self, model, layer_name):
        input_shape = self._shapes[layer_name]
        return [self._batch, *input_shape[1:]]

    def get_input_layer_dtype(self, model, layer_name):
        from numpy import float32, float16
        if self._tensor_rt_dtype:
            import torch
            if self._tensor_rt_dtype in [torch.float, torch.float32]:
                return float32
            elif self._tensor_rt_dtype in [torch.half, torch.float16]:
                return float16
        elif self._custom_input_type:
            return self._custom_input_type
        elif self._custom_precision:
            if '32' in self._custom_precision:
                return float32
            elif '16' in self._custom_precision:
                return float16
        return float32


class ONNXIOModelWrapper(IOModelWrapper):
    def __init__(self, inputs, batch):
        self._inputs = inputs
        self._batch = batch

    def get_input_layer_names(self, model):
        if self._inputs:
            return list(self._inputs.keys())

        inputs_info = model.get_inputs()
        return [input_layer.name for input_layer in inputs_info]

    def get_input_layer_shape(self, model, layer_name):
        if self._inputs:
            input_shape = self._inputs[layer_name]
        else:
            inputs_info = model.get_inputs()
            for model_input in inputs_info:
                if model_input.name == layer_name:
                    input_shape = model_input.shape
        try:
            return [self._batch, *input_shape[1:]]
        except TypeError:
            return [input_shape]

    def get_input_layer_dtype(self, model, layer_name):
        inputs_info = model.get_inputs()
        for model_input in inputs_info:
            if model_input.name == layer_name:
                dtype = model_input.type.replace('tensor(', '').replace(')', '')
                if dtype == 'float':
                    dtype += '32'
                return dtype

        from numpy import float32
        return float32


class TVMIOModelWrapper(IOModelWrapper):
    def __init__(self, args):
        self._input_names = [args['input_name']]
        self._input_shapes = [args['input_shape']]
        self._model_name = args['model_name']

    def get_input_layer_names(self, model):
        return self._input_names

    def get_input_layer_shape(self, model, layer_name):
        return self._input_shapes[0]

    def get_input_layer_dtype(self, model, layer_name):
        import numpy as np
        return np.float32

    def get_model_name(self):
        return self._model_name


class ONNXIOModelWrapperCpp(IOModelWrapper):
    def __init__(self, model):
        self._input_shape = model.get_inputs()[0].shape
        self._input_name = model.get_inputs()[0].name

    def get_input_layer_names(self, model):
        return self._input_name

    def get_input_layer_shape(self, model, layer_name):
        return self._input_shape

    def get_input_layer_dtype(self, model, layer_name):
        from numpy import float32
        return float32


class DGLPyTorchWrapper(IOModelWrapper):
    def __init__(self, model):
        self._input_shape = next(model.parameters()).size()
        self._input_name = list(model.state_dict())[0]
        self._input_dtype = next(model.parameters()).dtype

    def get_input_layer_names(self, model):
        return self._input_name

    def get_input_layer_shape(self, model, layer_name):
        return self._input_shape

    def get_input_layer_dtype(self, model, layer_name):
        return self._input_dtype


class TFLiteIOModelWrapperCpp(IOModelWrapper):
    def __init__(self, batch_size):
        self._batch = batch_size

    def get_input_layer_names(self, interpreter):
        inputs = interpreter.get_input_details()
        input_names = []
        for input_ in inputs:
            input_names.append(input_['name'])
        return input_names

    def get_input_layer_shape(self, interpreter, layer_name):
        try:
            inputs = interpreter.get_input_details()
            for input_ in inputs:
                if layer_name == input_['name']:
                    shape = input_['shape']
                    break
        except Exception:
            raise ValueError('Could not get the correct shape. '
                             'Try setting the "input_shape" parameter manually.')
        shape[0] = self._batch
        if None in shape[1:]:
            raise ValueError(f'Invalid shape {shape}. Try setting the "input_shape" parameter manually.')
        return shape

    @staticmethod
    def get_outputs_layer_names(interpreter, outputs_names=None):
        if outputs_names:
            return outputs_names
        outputs = interpreter.get_output_details()
        output_names = []
        for output_ in outputs:
            output_names.append(output_['name'])
        if not output_names:
            raise ValueError('Output blobs in the graph cannot be found')
        return output_names

    def get_input_layer_dtype(self, interpreter, layer_name):
        inputs = interpreter.get_input_details()
        for input_ in inputs:
            if layer_name == input_['name']:
                return input_['dtype']


class NcnnIOModelWrapper(IOModelWrapper):
    def __init__(self, args):
        # model wrapper supports only one input (batch of images)
        self._input_names = [args.input_name]
        self._input_shapes = [args.input_shape]
        self._model_name = args.model

    def get_input_layer_names(self, model):
        return self._input_names

    def get_input_layer_shape(self, model, layer_name):
        return self._input_shapes[0]

    def get_input_layer_dtype(self, model, layer_name):
        import numpy as np
        return np.uint8

    def get_model_name(self):
        return self._model_name


class RknnIOModelWrapperCpp(IOModelWrapper):
    def __init__(self, args):
        self._input_shape = args.shape

    def get_input_layer_shape(self):
        return self._input_shape

    def get_input_layer_dtype(self):
        import numpy as np
        return np.uint8
