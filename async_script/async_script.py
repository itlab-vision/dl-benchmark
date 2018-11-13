#!/usr/bin/env python


import sys
import os
import argparse
import numpy as np
import logging as log
import time
import copy

import cv2

from openvino.inference_engine import IENetwork, IEPlugin


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help = "Path to an .xml \
        file with a trained model.", required = True, type = str)
    parser.add_argument("-w", "--weights", help = "Path to an .bin file \
        with a trained weights.", required = True, type = str)
    parser.add_argument("-i", "--input", help = "Path to a folder with \
        images or path to an image files", required = True, type = str, nargs = "+")
    parser.add_argument("-r", "--Requests", help = "A positive integer value \
        of infer requests to be created. Number of infer requests may be \
        limited by device capabilities", required = True, type = int)
    parser.add_argument("-b", "--batch_size", help = "Size of the  \
     processed pack", default = 1, type = int)
    parser.add_argument("-l", "--cpu_extension", help = "MKLDNN \
        (CPU)-targeted custom layers.Absolute path to a shared library \
        with the kernels implementation", type = str, default = None)
    parser.add_argument("-pp", "--plugin_dir", help = "Path to a plugin \
        folder", type = str, default = None)
    parser.add_argument("-d", "--device", help = "Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)", default = "CPU", type = str)
    parser.add_argument("--labels", help = "Labels mapping file",
        default = None, type = str)
    parser.add_argument("-nt", "--number_top", help = "Number of top results",
        default = 10, type = int)
    parser.add_argument("-ni", "--number_iter", help = "Number of inference \
        iterations", default = 1, type = int)

    return parser


def prepare_model(log):
    args = build_parser().parse_args()
    model_xml = args.model
    model_bin = args.weights

    log.info("Plugin initialization.");
    plugin = IEPlugin(device = args.device, plugin_dirs = args.plugin_dir)
    if args.cpu_extension and 'CPU' in args.device:
        plugin.add_cpu_extension(args.cpu_extension)

    log.info("Loading network files:\n\t {0}\n\t {1}".format(
        model_xml, model_bin))
    net = IENetwork.from_ir(model_xml, model_bin)
    if "CPU" in plugin.device:
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [ l for l in net.layers.keys() \
            if l not in supported_layers ]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin \
                for specified device {0}:\n {1}".format(plugin.device,
                ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in \
                sample's command line parameters using -l or --cpu_extension \
                command line argument")
            sys.exit(1)      
    if os.path.isdir(args.input[0]):
        data = [args.input[0] + file for file in os.listdir(args.input[0])]
    else:
        data = args.input

    return net, plugin, data, args


def convert_image(model, data):
    n, c, h, w  = model.inputs[next(iter(model.inputs))]
    images = np.ndarray(shape = (model.inputs[next(iter(model.inputs))]))
    for i in range(n):
        image = cv2.imread(data[i])
        if (image.shape[:-1] != (h, w)):
            image = cv2.resize(image, (h, w))
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images

def prepare_data(model, data):
    video = {".mp4" : 1, ".avi" : 2, ".mvo" : 3, ".mpeg" : 4, ".mov" : 5}
    image = {".jpg" : 1, ".png" : 2, ".bmp" : 3, ".gif" : 4}
    file = str(os.path.splitext(data[0])[1]).lower()
    if file in image:
        prep_data = convert_image(model, data)
    elif file in video:
        prep_data = data[0]
    return prep_data


def start_infer_video(path, exec_net, model, number_iter):
    input_blob = next(iter(model.inputs))
    curr_request_id = 0
    prev_request_id  = 1
    n, c, h, w  = model.inputs[input_blob]
    images_t = []
    res = []
    video = cv2.VideoCapture(path)
    ret, frame = 1, 0
    z = 0
    while video.isOpened():
        for k in range(n):
            ret, frame = video.read()
            if not ret:
                break
            if (frame.shape[:-1] != (h, w)):
                frame = cv2.resize(frame, (h, w))       
                frame = frame.transpose((2, 0, 1))
            images_t.append(frame)
        if (len(images_t) == 0):
            break
        while len(images_t) < n:
            images_t.append(images_t[0])
        images = np.asarray(images_t)      
        exec_net.start_async(request_id = curr_request_id,
                inputs = {input_blob: images})
        if exec_net.requests[prev_request_id].wait(-1) == 0:
            res.append(copy.deepcopy(exec_net.requests[prev_request_id].
                    outputs[next(iter(model.outputs))]))
        prev_request_id, curr_request_id = curr_request_id, prev_request_id
        images_t.clear();
    if exec_net.requests[prev_request_id].wait(-1) == 0:
        res.append(exec_net.requests[prev_request_id].
                 outputs[next(iter(model.outputs))])
    result = np.ndarray(shape = ((len(res) * n,) + 
        exec_net.requests[0].outputs[next(iter(model.outputs))].shape[1:]))
    for i, r in enumerate(res):
        result[i * n : (i + 1) * n] = r


    return result

       

def infer_async(images, exec_net, model, number_iter):
    if type(images) is str:
        res = start_infer_video(images, exec_net, model, number_iter)
    elif len(exec_net.requests) == 1:
        res = start_infer_one_req(images, exec_net, model, number_iter)
    else:
        res = start_infer_two_req(images, exec_net, model, number_iter)
    
    return res

def start_infer_one_req(images, exec_net, model, number_iter):
    input_blob = next(iter(model.inputs))
    for i in range(number_iter):
        infer_request_handle = exec_net.start_async(request_id = 0,
            inputs = {input_blob: images})
        infer_status = infer_request_handle.wait()

    log.info("Processing output blob")
    res = infer_request_handle.outputs[next(iter(model.outputs))] 
    return res


def start_infer_two_req(images, exec_net, model,  number_iter):
    input_blob = next(iter(model.inputs))
    curr_request_id = 0
    prev_request_id  = 1
    res = np.ndarray(shape = ((model.batch_size,) + 
        exec_net.requests[0].outputs[next(iter(model.outputs))].shape))
    for i in range(number_iter):
        for j, image in enumerate(images):
            exec_net.start_async(request_id = curr_request_id,
                inputs = {input_blob: image})
            if exec_net.requests[prev_request_id].wait(-1) == 0:
                res[j - 1] = (exec_net.requests[prev_request_id].
                    outputs[next(iter(model.outputs))])
            prev_request_id, curr_request_id = curr_request_id, prev_request_id
    if exec_net.requests[prev_request_id].wait(-1) == 0:
        res[model.batch_size - 1] = (exec_net.requests[prev_request_id].
            outputs[next(iter(model.outputs))])
    result = np.ndarray(shape = res.shape[1:])
    print(result.shape)
    for i, r in enumerate(res):
        result[i] = r[0]
    return result


def infer_output(res, data, labels, number_top, log):

    log.info("Top {} results: \n".format(number_top))
    if not labels:
        labels = "image_net_synset.txt"
    with open(labels, 'r') as f:
        labels_map = [ x.split(sep = ' ', maxsplit = 1)[-1].strip() \
            for x in f ]

    for i, probs in enumerate(res):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-number_top:][::-1]
        if len(data) > 1:
            print("Image {}\n".format(os.path.split(data[i])[1]))
        else:
            print("Image {}\n".format(os.path.split(data[0])[1]))
        for id in top_ind:
            det_label = labels_map[id] if labels_map else "#{}".format(id)
            print("{:.7f} {}".format(probs[id], det_label))
        print("\n")  


def main():
    log.basicConfig(format = "[ %(levelname)s ] %(message)s",
        level = log.INFO, stream = sys.stdout)
    net, plugin, data, args = prepare_model(log)
    net.batch_size = (args.batch_size if args.batch_size > 1 
        else len(data))
    images = prepare_data(net, data)
    log.info("Loading model to the plugin")
    exec_net = plugin.load(network = net, num_requests = args.Requests)
    log.info("Starting inference ({} iterations)".format(args.number_iter))
    res = infer_async(images, exec_net, net, args.number_iter)
    infer_output(res, data, args.labels, args.number_top, log)
    del net
    del exec_net
    del plugin


if __name__ == '__main__':
    sys.exit(main() or 0)

