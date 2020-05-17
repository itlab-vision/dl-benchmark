import os
import sys
import numpy as np
import logging as log
import cv2
from copy import copy
from openvino.inference_engine import IECore


def create_network(iecore, model_xml, model_bin, log):
    log.info('Loading network files:\n\t {0}\n\t {1}'.format(
        model_xml, model_bin))
    network = iecore.read_network(model = model_xml, weights = model_bin)
    return network


def add_extension(iecore, path_to_extension, path_to_cldnn_config, device, log):
    if path_to_extension:
        if 'GPU' in device:
            iecore.set_config({'CONFIG_FILE': path_to_cldnn_config}, 'GPU')
            log.info('GPU extensions is loaded {}'.format(path_to_extension))
        if 'CPU' in device or 'MYRIAD' in device:
            iecore.add_extension(path_to_extension, 'CPU')
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
        for key in result:
            result[key] = values
        return result
    for pair in values.split(','):
        key, value = pair.split(':')
        if key in device_list:
            result[key] = value
    return result


def set_config(iecore, devices, nthreads, nstreams, dump, mode):
    device_list = parse_devices(devices)
    streams_dict = parse_value_per_device(device_list, nstreams)
    for device in device_list:
        if device == 'CPU':
            if nthreads:
                iecore.set_config({'CPU_THREADS_NUM': str(nthreads)}, 'CPU')
            if 'MULTI' in devices and 'GPU' in devices:
                iecore.set_config({'CPU_BIND_THREAD': 'NO'}, 'CPU')
            if mode == 'async':
                cpu_throughput = {'CPU_THROUGHPUT_STREAMS': 'CPU_THROUGHPUT_AUTO'}
                if device in streams_dict.keys() and streams_dict[device]:
                    cpu_throughput['CPU_THROUGHPUT_STREAMS'] = streams_dict['CPU']
                iecore.set_config(cpu_throughput, 'CPU')
        if device == 'GPU':
            if 'MULTI' in devices and 'СPU' in devices:
                iecore.set_config({'CLDNN_PLUGIN_THROTTLE': '1'}, 'GPU')
            if mode == 'async':
                gpu_throughput = {'GPU_THROUGHPUT_STREAMS': 'GPU_THROUGHPUT_AUTO'}
                if device in streams_dict.keys() and streams_dict[device]:
                    gpu_throughput['GPU_THROUGHPUT_STREAMS'] = streams_dict['GPU']
                iecore.set_config(gpu_throughput, 'GPU')
        if device == 'MYRIAD':
            iecore.set_config({'LOG_LEVEL': 'LOG_INFO', 'VPU_LOG_LEVEL': 'LOG_WARNING'}, 'MYRIAD')
    if dump:
        if 'HETERO' in devices:
            iecore.set_config({'HETERO_DUMP_GRAPH_DOT': 'YES'}, 'HETERO')
        elif not('MULTI' in devices):
            iecore.set_config({'DUMP_EXEC_GRAPH_AS_DOT': 'exec_graph'}, devices)


def create_ie_core(path_to_extension, path_to_cldnn_config, device, nthreads, nstreams,
    dump, mode, log):
    log.info('Inference Engine initialization')
    ie = IECore()
    add_extension(ie, path_to_extension, path_to_cldnn_config, device, log)
    set_config(ie, device, nthreads, nstreams, dump, mode)
    return ie


def load_network(iecore, network, device, multi_priority, requests):
    config = {}
    if 'MULTI' in device and multi_priority:
        config.update({'MULTI_DEVICE_PRIORITIES': multi_priority})
    exec_net = iecore.load_network(network = network, device_name = device,
        num_requests = (requests or 0), config = config)
    return exec_net


def get_input_shape(io_model_wrapper, model):
    layer_shapes = dict()
    layer_names = io_model_wrapper.get_input_layer_names(model)
    for input_layer in layer_names:
        shape = ''
        for dem in io_model_wrapper.get_input_layer_shape(model, input_layer):
            shape += '{0}x'.format(dem)
        shape = shape[:-1]
        layer_shapes.update({input_layer : shape})
    return layer_shapes


def reshape_input(net, batch_size):
    new_shapes = {}
    for layer in net.inputs:
        shape = net.inputs[layer].shape
        shape[0] = batch_size
        new_shapes.update({layer : shape})
    net.reshape(new_shapes)
