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
