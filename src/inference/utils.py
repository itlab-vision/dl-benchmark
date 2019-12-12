import os
import sys
import numpy as np
import logging as log
import cv2
from copy import copy
from openvino.inference_engine import IENetwork, IECore


def create_network(model_xml, model_bin, log):
    log.info('Loading network files:\n\t {0}\n\t {1}'.format(
        model_xml, model_bin))
    network = IENetwork(model = model_xml, weights = model_bin)
    return network


def add_extension(iecore, path_to_extension, device, log):
    if path_to_extension:
        if device == 'GPU':
            iecore.set_config({'CONFIG_FILE': path_to_extension}, device)
            log.info('GPU extensions is loaded {}'.format(path_to_extension))
        if device == 'CPU' or device == 'MYRIAD':
            iecore.add_extension(path_to_extension, device)
            log.info('CPU extensions is loaded {}'.format(path_to_extension))


def set_config(iecore, device, nthreads, nstreams, mode):
    config = {}
    if device == 'CPU':
        if nthreads:
            config.update({'CPU_THREADS_NUM': str(nthreads)})
        if mode == 'async':
            cpu_throughput = {'CPU_THROUGHPUT_STREAMS': 'CPU_THROUGHPUT_AUTO'}
            if nstreams:
                cpu_throughput['CPU_THROUGHPUT_STREAMS'] = str(nstreams)
            config.update(cpu_throughput)
    if device == 'GPU':
        if mode == 'async':
            gpu_throughput = {'GPU_THROUGHPUT_STREAMS': 'GPU_THROUGHPUT_AUTO'}
            if nstreams:
                gpu_throughput['GPU_THROUGHPUT_STREAMS'] = str(nstreams)
            config.update(gpu_throughput)
    if device == 'MYRIAD':
        config.update({'LOG_LEVEL': 'LOG_INFO', 'VPU_LOG_LEVEL': 'LOG_WARNING'})
    iecore.set_config(config, device)


def create_ie_core(path_to_extension, device, nthreads, nstreams, mode, log):
    log.info('Inference Engine initialization')
    ie = IECore()
    add_extension(ie, path_to_extension, device, log)
    set_config(ie, device, nthreads, nstreams, mode)
    return ie


def get_input_shape(model):
    layers_shape = dict()
    for input_layer in model.inputs:
        shape = ''
        for dem in model.inputs[input_layer].shape:
            shape += '{0}x'.format(dem)
        shape = shape[:-1]
        layers_shape.update({input_layer : shape})
    return layers_shape


def convert_images(shape, data):
    n, c, h, w  = shape
    images = np.ndarray(shape = (len(data), c, h, w))
    for i in range(len(data)):
        image = cv2.imread(data[i])
        if (image.shape[:-1] != (h, w)):
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images


def fill_input(input, batch_size):
    index = 0
    result = input.copy()
    while(len(result) < batch_size):
        result.append(copy(result[index]))
        index += 1
    return result


def create_list_images(input):
    images = []
    input_is_correct = True
    if os.path.exists(input[0]):
        if os.path.isdir(input[0]):
            path = os.path.abspath(input[0])
            images = [os.path.join(path, file) for file in os.listdir(path)]
        elif os.path.isfile(input[0]):
            for image in input:
                if not os.path.isfile(image):
                    input_is_correct = False
                    break
                images.append(os.path.abspath(image))
        else:
            input_is_correct = False
    if not input_is_correct:
        raise ValueError("Wrong path to image or to directory with images")
    return images


def check_correct_input(len_values):
    ideal = len_values[0]
    for len in len_values:
        if len != ideal:
            raise ValueError("Mismatch batch sizes for different input layers")


def parse_tensors(filename):
    with open(filename, "r") as file:
        input = file.readlines()
    input = [line.strip() for line in input]
    shape = [int(number) for number in input[0].split(';')]
    input.pop(0)
    value = []
    for str in input:
        value.append([float(number) for number in str.split(';')])
    result = np.array(value, dtype = np.float32)
    result = result.reshape(shape)
    return result


def prepare_input(model, input, batch_size):
    result = {}
    if ':' in input[0]:
        len_values = []
        for str in input:
            key, value = str.split(':')
            shape = model.inputs[key].shape
            file_format = value.split('.')[-1]
            if 'csv' == file_format:
                value = parse_tensors(value)
                len_values.append(value.shape[0])
            else:
                value = value.split(',')
                len_values.append(len(value))
                value = fill_input(value, batch_size)
                value = create_list_images(value)
                value = convert_images(shape, value)
            result.update({key : value})
        check_correct_input(len_values)
    else:
        input_blob = next(iter(model.inputs))
        shape = model.inputs[input_blob].shape
        file_format = input[0].split('.')[-1]
        if 'csv' == file_format:
            value = parse_tensors(input[0])
        else:
            list = fill_input(input, batch_size)
            list = create_list_images(list)
            value = convert_images(shape, list)
        result.update({input_blob : value})
    return result