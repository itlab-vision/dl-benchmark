import os
import sys
import numpy as np
import logging as log
import cv2
from openvino.inference_engine import IENetwork, IEPlugin

def prepare_model(log, model, weights, cpu_extension, device_list, plugin_dir,
                  thread_num, stream_num):
    model_xml = model
    model_bin = weights
    if len(device_list) == 1:
        device = device_list[0]
    elif len(device_list) == 2:
        device = 'HETERO:{},{}'.format(device_list[0], device_list[1])
    else:
        log.error('Wrong count devices')
        sys.exit(1)
    log.info('Plugin initialization.');
    plugin = IEPlugin(device = device, plugin_dirs = plugin_dir)
    if cpu_extension and 'CPU' in device:
        plugin.add_cpu_extension(cpu_extension)
    log.info('Loading network files:\n\t {0}\n\t {1}'.format(
        model_xml, model_bin))
    net = IENetwork(model = model_xml, weights = model_bin)
    if plugin.device == 'CPU':
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [ l for l in net.layers.keys() \
            if l not in supported_layers ]
        if len(not_supported_layers) != 0:
            log.error('Following layers are not supported by the plugin \
                for specified device {0}:\n {1}'.format(plugin.device,
                ', '.join(not_supported_layers)))
            log.error('Please try to specify cpu extensions library path in \
                sample\'s command line parameters using -l or --cpu_extension \
                command line argument')
            sys.exit(1)
    if thread_num is not None:
        if 'CPU' in device_list:
            plugin.set_config({'CPU_THREADS_NUM': str(thread_num)})
        else:
            log.error('Parameter : Number of threads is used only for CPU')
            sys.exit(1)
    if stream_num is not None:
        if 'CPU' in device_list:
            plugin.set_config({'CPU_THROUGHPUT_STREAMS': str(stream_num)})
        else:
            log.error('Parameter : Number of streams is used only for CPU')
            sys.exit(1)
    if len(device_list) == 2:
        plugin.set_config({'TARGET_FALLBACK': device})
        plugin.set_initial_affinity(net)
    return net, plugin


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