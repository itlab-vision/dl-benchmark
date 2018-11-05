#!/usr/bin/env python


import sys
import os
import argparse
import cv2
import numpy as np
import logging as log
import time
from openvino.inference_engine import IENetwork, IEPlugin

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help = "Path to an .xml file with a trained model.", required = True, type = str)
    parser.add_argument("-w", "--weights", help = "Path to an .bin file with a trained weights.", required = True, type = str)
    parser.add_argument("-i", "--input", help = "Path to a folder with images or path to an image files", required = True,
                        type = str, nargs = "+")
    parser.add_argument("-l", "--cpu_extension", 
                        help = "MKLDNN (CPU)-targeted custom layers.Absolute path to a shared library with the kernels "
                            "impl.", type = str, default = None)
    parser.add_argument("-pp", "--plugin_dir", help = "Path to a plugin folder", type = str, default = None)
    parser.add_argument("-d", "--device",
                        help = "Specify the target device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device specified (CPU by default)", default = "CPU",
                        type = str)
    parser.add_argument("--labels", help = "Labels mapping file", default = None, type = str)
    parser.add_argument("-nt", "--number_top", help = "Number of top results", default = 10, type = int)
    parser.add_argument("-ni", "--number_iter", help = "Number of inference iterations", default = 1, type = int)
    parser.add_argument("-pc", "--perf_counts", help = "Report performance counters", action = "store_true", default = False)

    return parser

def image_convert(model, data):
    n = net.inputs[next(iter(net.inputs))][0]
    images = np.ndarray(shape = (net.inputs[next(iter(net.inputs))]))
    for i in range(n):
        image = cv2.imread(image_list[i])
        if (image.shape[:-1] != (h,w)):
                log.warning("Image {} is resized from {} to {}.".format(os.path.split(image_list[i])[1], 
                             image.shape[:-1], (h,w)))
                image = cv2.resize(image, (h, w))    	
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images

def data_preparation(model, path):
    if os.path.isdir(path[0]):
        date = [path[0] + file for file in os.listdir(path[0])]
    else:
        data = path
    net.batch_size = len(data)
    video = {".mp4" : 1, ".avi" : 2, ".mvo" : 3, ".mpeg" : 4}
    image = {".jpg" : 1, ".png" : 2, ".bmp" : 3, ".gif" : 4}
    file = str(os.path.splitext(data[0])[1])
    if file in image:
        prep_data = image_convert(model, data)
    images = []

    return prep_data

def main():
    log.basicConfig(format = "[ %(levelname)s ] %(message)s", level = log.INFO, stream = sys.stdout)
    args = build_parser().parse_args()
    model_xml = args.model
    model_bin = args.weights
    log.info("Loading network files:\n\t {}\n\t {}".format(os.path.split(model_xml)[1], os.path.split(model_bin)[1]))
    net = IENetwork.from_ir(model_xml, model_bin)
    log.info("Preparing input blobs.")
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    image_list = []
    data = data_preparation(net, args.input)
    if os.path.isdir(args.input[0]):
        net.batch_size = len(os.listdir(args.input[0]))
        image_list = [args.input[0] + img for img in os.listdir(args.input[0])]
    else:
        net.batch_size = len(args.input)
        image_list = args.input
    log.info("Batch size is {}.".format(net.batch_size))    
    n, c, h, w = net.inputs[input_blob]
    images = np.ndarray(shape = (n, c, h, w))

    for i in range(n):
        image = cv2.imread(image_list[i])
        if (image.shape[:-1] != (h,w)):
                log.warning("Image {} is resized from {} to {}.".format(os.path.split(image_list[i])[1], 
                             image.shape[:-1], (h,w)))
                image = cv2.resize(image, (h, w))    	
        image = image.transpose((2, 0, 1))
        images[i] = image
    log.info("Plugin initialization.");
    plugin = IEPlugin(device = args.device, plugin_dirs = args.plugin_dir)
    log.info("Loading model to the plugin")
    exec_net = plugin.load(network = net)
    del net

    log.info("Starting inference ({} iterations)".format(args.number_iter))
    for i in range(args.number_iter):
        infer_request_handle = exec_net.start_async(request_id = 0, inputs = {input_blob: images})
        infer_status = infer_request_handle.wait()

    log.info("Processing output blob")
    res = infer_request_handle.outputs[out_blob]
    log.info("Top {} results: \n".format(args.number_top))
    if not args.labels:
    	args.labels = "image_net_synset.txt"
    with open(args.labels, 'r') as f:
        labels_map = [x.split(sep = ' ', maxsplit = 1)[-1].strip() for x in f]

    for i, probs in enumerate(res):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-args.number_top:][::-1]
        print("Image {}\n".format(os.path.split(image_list[i])[1]))
        for id in top_ind:
            det_label = labels_map[id] if labels_map else "#{}".format(id)
            print("{:.7f} {}".format(probs[id], det_label))
        print("\n")

    del exec_net
    del plugin


if __name__ == '__main__':
    sys.exit(main() or 0)    