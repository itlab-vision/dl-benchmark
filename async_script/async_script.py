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
    parser.add_argument("-r", "--Requests", help = "A positive integer value of infer requests to be created. Number of infer"
                         "requests may be limited by device capabilities", required = True, type = int)
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

def model_preparation(log):
    args = build_parser().parse_args()
    model_xml = args.model
    model_bin = args.weights
    log.info("Plugin initialization.");
    plugin = IEPlugin(device = args.device, plugin_dirs = args.plugin_dir)
    if args.cpu_extension and 'CPU' in args.device:
        plugin.add_cpu_extension(args.cpu_extension)
    log.info("Loading network files:\n\t {}\n\t {}".format(os.path.split(model_xml)[1], os.path.split(model_bin)[1]))
    net = IENetwork.from_ir(model_xml, model_bin)
    if "CPU" in plugin.device:
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(plugin.device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)      
    if os.path.isdir(args.input[0]):
        data = [args.input[0] + file for file in os.listdir(args.input[0])]
    else:
        data = args.input

    return net, plugin, data, args


def image_convert(model, data, log):
    n, c, h, w  = model.inputs[next(iter(model.inputs))]
    images = np.ndarray(shape = (model.inputs[next(iter(model.inputs))]))
    for i in range(n):
        image = cv2.imread(data[i])
        if (image.shape[:-1] != (h,w)):
                log.warning("Image {} is resized from {} to {}.".format(os.path.split(data[i])[1], 
                             image.shape[:-1], (h,w)))
                image = cv2.resize(image, (h, w))    	
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images

def video_convert(model, data, log):
    n, c, h, w  = model.inputs[next(iter(model.inputs))]
    return n    

def data_preparation(model, data, log):
    video = {".mp4" : 1, ".avi" : 2, ".mvo" : 3, ".mpeg" : 4}
    image = {".jpg" : 1, ".png" : 2, ".bmp" : 3, ".gif" : 4}
    file = str(os.path.splitext(data[0])[1])
    if file in image:
        prep_data = image_convert(model, data, log)
    return prep_data

def start_infer_async(images, exec_net, model,  args):
    input_blob = next(iter(model.inputs))
    for i in range(args.number_iter):
        infer_request_handle = exec_net.start_async(request_id = 0, inputs = {input_blob: images})
        infer_status = infer_request_handle.wait()

    log.info("Processing output blob")
    res = infer_request_handle.outputs[next(iter(model.outputs))] 
    return res

def start_true_infer_async(images, exec_net, model,  args):
    input_blob = next(iter(model.inputs))
    curr_request_id = 0
    next_request_id  = 1
    res = np.ndarray(shape = (len(images), 4, 1000))
    j = 0
    k = 0
    for i in range(args.number_iter):
        for j in range(len(images)):
            exec_net.start_async(request_id = next_request_id, inputs = {input_blob: images[j]})
            if exec_net.requests[curr_request_id].wait(-1) == 0:
                res[j] = exec_net.requests[curr_request_id].outputs[next(iter(model.outputs))]
            elif exec_net.requests[next_request_id].wait(-1) == 0:
                res[j] = exec_net.requests[next_request_id].outputs[next(iter(model.outputs))]
            curr_request_id, next_request_id = next_request_id, curr_request_id
    log.info("Processing output blob")
    #res = exec_net.requests[next_request_id].outputs[next(iter(model.outputs))] 
    return res

def infer_output(res, data, args, log):
    log.info("Top {} results: \n".format(args.number_top))
    if not args.labels:
    	args.labels = "image_net_synset.txt"
    with open(args.labels, 'r') as f:
        labels_map = [x.split(sep = ' ', maxsplit = 1)[-1].strip() for x in f]

    for i in range(len(res)):
        probs = np.squeeze(res[i])
        top_ind = np.argsort(probs)[-args.number_top:][::-1]
        print("Image {}\n".format(os.path.split(data[i])[1]))
        for id in top_ind:
            det_label = labels_map[id] if labels_map else "#{}".format(id)
            print("{:.7f} {}".format(probs[id], det_label))
        print("\n")   

def main():
    log.basicConfig(format = "[ %(levelname)s ] %(message)s", level = log.INFO, stream = sys.stdout)
    net, plugin, data, args = model_preparation(log)
    net.batch_size = len(data)
    images = data_preparation(net, data, log)
    log.info("Loading model to the plugin")
    exec_net = plugin.load(network = net, num_requests = args.Requests)
    log.info("Starting inference ({} iterations)".format(args.number_iter))
    res = start_true_infer_async(images, exec_net, net, args)
    del net
    print(res)
    #infer_output(res, data, args, log)
    del exec_net
    del plugin


if __name__ == '__main__':
    sys.exit(main() or 0)    