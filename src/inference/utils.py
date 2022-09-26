from copy import copy
from openvino.runtime import Core, Tensor, PartialShape  # pylint: disable=E0401


def create_model(core, model_xml, model_bin, log):
    log.info('Loading model files:\n\t {0}\n\t {1}'.format(
        model_xml, model_bin))
    model = core.read_model(model=model_xml, weights=model_bin)
    return model


def parse_affinity(affinity_file):
    affinity = {}
    with open(affinity_file, 'r') as f:
        for line in f:
            node, device = line.strip().split(' ')
            affinity.update({node: device})
    return affinity


def configure_model(core, model, device, default_device, affinity_file):
    if 'HETERO' not in device:
        return
    nodes = model.get_ops()
    if affinity_file:
        if not default_device:
            raise ValueError('--default_device is required parameter for heterogeneous inference')
        affinity = parse_affinity(affinity_file)
        for node in nodes:
            if node.get_friendly_name() in affinity.keys():
                node.get_rt_info()["affinity"] = affinity[node.get_friendly_name()]
            else:
                node.get_rt_info()["affinity"] = default_device
    else:
        supported_ops = core.query_model(model=model, device_name=device)
        for node in nodes:
            affinity = supported_ops[node.get_friendly_name()]
            node.get_rt_info()["affinity"] = affinity


def add_extension(core, path_to_extension, path_to_intel_gpu_config, device, log):
    if path_to_extension:
        if 'GPU' in device:
            core.set_property('GPU', {'CONFIG_FILE': path_to_intel_gpu_config})
            log.info('GPU extensions is loaded {}'.format(path_to_extension))
        if 'CPU' in device or 'MYRIAD' in device:
            core.add_extension(path_to_extension, 'CPU')
            log.info('CPU extensions is loaded {}'.format(path_to_extension))


def parse_devices(device):
    device_list = []
    if ':' in device:
        device_list = device.partition(':')[2].split(',')
    else:
        device_list.append(device)
    return device_list


def parse_value_per_device(device_list, values):
    result = dict.fromkeys(device_list, None)
    if values is None:
        return result
    if values.isdecimal():
        new_result = result
        for key in result:
            new_result[key] = values
        return result
    for pair in values.split(','):
        key, value = pair.split(':')
        if key in device_list:
            result[key] = value
    return result


def set_property(core, devices, nthreads, nstreams, dump, mode):
    device_list = parse_devices(devices)
    streams_dict = parse_value_per_device(device_list, nstreams)
    for device in device_list:
        if device == 'CPU':
            if nthreads:
                core.set_property('CPU', {'CPU_THREADS_NUM': str(nthreads)})
            if 'MULTI' in devices and 'GPU' in devices:
                core.set_property({'CPU_BIND_THREAD': 'NO'}, 'CPU')
            if mode == 'async':
                cpu_throughput = {'CPU_THROUGHPUT_STREAMS': 'CPU_THROUGHPUT_AUTO'}
                if device in streams_dict.keys() and streams_dict[device]:
                    cpu_throughput['CPU_THROUGHPUT_STREAMS'] = streams_dict['CPU']
                core.set_property('CPU', cpu_throughput)
        if device == 'GPU':
            if 'MULTI' in devices and 'СPU' in devices:
                core.set_property('GPU', {'GPU_QUEUE_THROTTLE': '1'})
            if mode == 'async':
                gpu_throughput = {'GPU_THROUGHPUT_STREAMS': 'GPU_THROUGHPUT_AUTO'}
                if device in streams_dict.keys() and streams_dict[device]:
                    gpu_throughput['GPU_THROUGHPUT_STREAMS'] = streams_dict['GPU']
                core.set_property('GPU', gpu_throughput)
    if dump:
        if 'HETERO' in devices:
            core.set_property('HETERO', {'OPENVINO_HETERO_VISUALIZE': 'YES'})
        elif 'MULTI' not in devices:
            core.set_property(devices, {'DUMP_EXEC_GRAPH_AS_DOT': 'exec_graph'})


def create_core(path_to_extension, path_to_intel_gpu_config, device, nthreads, nstreams,
                dump, mode, log):
    log.info('Inference Engine initialization')
    core = Core()
    add_extension(core, path_to_extension, path_to_intel_gpu_config, device, log)
    set_property(core, device, nthreads, nstreams, dump, mode)
    return core


def compile_model(core, model, device, multi_priority):
    properties = {}
    if 'MULTI' in device and multi_priority:
        properties.update({'MULTI_DEVICE_PRIORITIES': multi_priority})
    compiled_model = core.compile_model(model, device, properties)
    return compiled_model


def get_input_shape(io_model_wrapper, model):
    layer_shapes = dict()
    layer_names = io_model_wrapper.get_input_layer_names(model)
    for input_layer in layer_names:
        shape = ''
        for dim in io_model_wrapper.get_input_layer_shape(model, input_layer):
            shape += '{0}x'.format(dim)
        shape = shape[:-1]
        layer_shapes.update({input_layer: shape})
    return layer_shapes


def reshape_input(model, batch_size):
    new_shapes = {}
    for input in model.inputs:
        shape = input.get_partial_shape()
        shape[0] = batch_size
        new_shapes.update({input.get_any_name(): shape})
    model.reshape(new_shapes)


def set_input_to_blobs(request, input):
    model_inputs = request.model_inputs
    for layer_name, data in input.items():
        found_tensor = False
        for model_input in model_inputs:
            if model_input.get_any_name() == layer_name:
                if PartialShape(data.shape) != model_input.get_partial_shape():
                    raise ValueError("Input data and input layer with name {0} has different shapes: \
                                     {1} and {2}".format(layer_name, PartialShape(data.shape), model_input.get_partial_shape()))
                new_tensor = Tensor(data)
                request.set_tensor(model_input.get_any_name(), new_tensor)
                found_tensor = True

        if not found_tensor:
            raise ValueError("No input layer with name {}".format(layer_name))


def get_request_result(request):
    result = dict()
    for output_node, tensor in request.results.items():
        result[output_node.get_any_name()] = copy(tensor)
    return result
