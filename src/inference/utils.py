import os
import sys
import numpy as np
import logging as log
import cv2
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


def get_input_list(input):
    if os.path.isdir(input[0]):
        data = [os.path.join(input[0], file) for file in os.listdir(input[0])]
    else:
        data = input
    return data


def prepare_data(model, data):
    video = {'.mp4' : 1, '.avi' : 2, '.mvo' : 3, '.mpeg' : 4, '.mov' : 5}
    image = {'.jpg' : 1, '.png' : 2, '.bmp' : 3, '.gif' : 4, '.jpeg' : 5}
    file = str(os.path.splitext(data[0])[1]).lower()
    if file in image:
        prep_data = convert_image(model, data)
    elif file in video:
        prep_data = data[0]
    return prep_data


def convert_image(model, data):
    n, c, h, w  = model.inputs[next(iter(model.inputs))].shape
    images = np.ndarray(shape = (len(data), c, h, w))
    for i in range(len(data)):
        image = cv2.imread(data[i])
        if (image.shape[:-1] != (h, w)):
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images