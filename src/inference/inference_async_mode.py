#!/usr/bin/env python


import sys
import os
import argparse
import numpy as np
import logging as log
from time import time
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
    parser.add_argument("-r", "--requests", help = "A positive integer value \
        of infer requests to be created. Number of infer requests may be \
        limited by device capabilities", required = True, type = int)
    parser.add_argument("-b", "--batch_size", help = "Size of the  \
        processed pack", default = 1, type = int)
    parser.add_argument("-t", "--model_type", help = "Сhoose model type: \
         1.classification  2.detection 3.segmentation",
        required = True, type = str)
    parser.add_argument("-l", "--cpu_extension", help = "MKLDNN \
        (CPU)-targeted custom layers.Absolute path to a shared library \
        with the kernels implementation", type = str, default = None)
    parser.add_argument("-pp", "--plugin_dir", help = "Path to a plugin \
        folder", type = str, default = None)
    parser.add_argument("-d", "--device", help = "Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)", default = "CPU", type = str)
    parser.add_argument("-nt", "--number_top", help = "Number of top results",
        default = 10, type = int)
    parser.add_argument("-ni", "--number_iter", help = "Number of inference \
        iterations", default = 1, type = int)
    parser.add_argument("--labels", help = "Labels mapping file",
        default = None, type = str)
    parser.add_argument("--prob_threshold", help="Probability threshold \
        for detections filtering", default = 0.5, type = float)
    parser.add_argument("--color_map", help="Classes color map", 
        default = None, type = str)
    return parser


def prepare_model(log, model, weights, cpu_extension, device, plugin_dir,
                  input):
    model_xml = model
    model_bin = weights

    log.info("Plugin initialization.");
    plugin = IEPlugin(device = device, plugin_dirs = plugin_dir)
    if cpu_extension and 'CPU' in device:
        plugin.add_cpu_extension(cpu_extension)

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
    if os.path.isdir(input[0]):
        data = [input[0] + file for file in os.listdir(input[0])]
    else:
        data = input

    return net, plugin, data


def prepare_data(model, data):
    video = {".mp4" : 1, ".avi" : 2, ".mvo" : 3, ".mpeg" : 4, ".mov" : 5}
    image = {".jpg" : 1, ".png" : 2, ".bmp" : 3, ".gif" : 4, ".jpeg" : 5}
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
            image = cv2.resize(image, (h, w))
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images


def start_infer_video(path, exec_net, model, number_iter):
    input_blob = next(iter(model.inputs))
    curr_request_id = 0
    prev_request_id  = 1
    n, c, h, w  = model.inputs[input_blob].shape
    images_t = []
    res = []
    video = cv2.VideoCapture(path)
    ret, frame = 1, 0
    z = 0
    time_s = time()
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
            res.append(copy.copy(exec_net.requests[prev_request_id].
                    outputs[next(iter(model.outputs))]))
        prev_request_id, curr_request_id = curr_request_id, prev_request_id
        images_t.clear();
    if exec_net.requests[prev_request_id].wait(-1) == 0:
        res.append(exec_net.requests[prev_request_id].
                 outputs[next(iter(model.outputs))])
    time_e = time() - time_s  
    result = np.ndarray(shape = ((len(res) * n,) + 
        exec_net.requests[0].outputs[next(iter(model.outputs))].shape[1:]))
    for i, r in enumerate(res):
        result[i * n : (i + 1) * n] = r
    return result, time_e


def start_infer_one_req(images, exec_net, model, number_iter):
    input_blob = next(iter(model.inputs))
    time_s = time()
    res = []
    size = model.batch_size
    if (len(images) % model.batch_size != 0):
        raise ValueError('Wrong batch_size')
    for i in range(len(images) // model.batch_size):
        for j in range(number_iter):
            infer_request_handle = exec_net.start_async(request_id = 0,
                inputs = {input_blob: images[i * size: (i + 1) * size]})
            infer_status = infer_request_handle.wait()
        res.append(copy.copy(infer_request_handle.outputs[next(iter(model.outputs))]))   
    log.info("Processing output blob")
    time_e = time() - time_s
    result = []
    for r_l1 in res:
        for r_l2 in r_l1:
            result.append(r_l2)
    res = np.asarray(result)
    return res, time_e


def start_infer_two_req(images, exec_net, model,  number_iter):
    input_blob = next(iter(model.inputs))
    curr_request_id = 0
    prev_request_id  = 1
    time_s = time()
    size = model.batch_size
    res = []
    if (len(images) % model.batch_size != 0):
        raise ValueError('Wrong batch_size')
    for i in range(len(images) // model.batch_size):
        for j in range(number_iter):
            exec_net.start_async(request_id = curr_request_id,
                inputs = {input_blob: images[i * size: (i + 1) * size]})
            if exec_net.requests[prev_request_id].wait(-1) == 0:
                pass
            prev_request_id, curr_request_id = curr_request_id, prev_request_id
        if exec_net.requests[prev_request_id].wait(-1) == 0:
            res.append(copy.copy(exec_net.requests[prev_request_id].
                outputs[next(iter(model.outputs))]))
    time_e = time() - time_s
    result = []
    for r_l1 in res:
        for r_l2 in r_l1:
            result.append(r_l2)
    res = np.asarray(result)
    return res, time_e


def infer_async(images, exec_net, model, number_iter):
    if type(images) is str:
        res = start_infer_video(images, exec_net, model, number_iter)
    elif len(exec_net.requests) == 1:
        res = start_infer_one_req(images, exec_net, model, number_iter)
    else:
        res = start_infer_two_req(images, exec_net, model, number_iter)
    return res


def classification_output(res, data, labels, number_top, log):
    log.info("Top {} results: \n".format(number_top))
    if labels:
        labels = "image_net_synset.txt"
        with open(labels, 'r') as f:
            labels_map = [ x.split(sep = ' ', maxsplit = 1)[-1].strip() \
                for x in f ]
    else:
        labels_map = None
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


def segmentation_output(res, color_map, log):
    c = 3
    h, w = res.shape[2:]
    if not color_map:
        color_map = "color_map.txt"
    classes_color_map = []
    with open(color_map, 'r') as f:
        for line in f:
            classes_color_map.append([int(x) for x in line.split()]) 
    for batch, data in enumerate(res):
        classes_map = np.zeros(shape=(h, w, c), dtype=np.int)
        for i in range(h):
            for j in range(w):
                if len(data[:, i, j]) == 1:
                    pixel_class = int(data[:, i, j])
                else:
                    pixel_class = np.argmax(data[:, i, j])
                classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
        out_img = os.path.join(os.path.dirname(__file__), "out_{}.bmp".format(batch))
        cv2.imwrite(out_img, classes_map)
        log.info("Result image was saved to {}".format(out_img))


def detection_output(res, data, prob_threshold):
    for i, r in enumerate(res):
        image = cv2.imread(data[i])
        initial_h, initial_w = image.shape[:2]
        for obj in r[0]:
            if obj[2] > prob_threshold:
                xmin = int(obj[3] * initial_w)
                ymin = int(obj[4] * initial_h)
                xmax = int(obj[5] * initial_w)
                ymax = int(obj[6] * initial_h)
                class_id = int(obj[1])
                color = (min(class_id * 12.5, 255), min(class_id * 7, 255),
                    min(class_id * 5, 255))
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.imshow("Detection Results", image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()


def infer_output(res, images, data, labels, number_top, prob_threshold,
        color_map, log, model_type):
    if model_type == "classification": 
        classification_output(res, data, labels, number_top, log)
    elif model_type == "detection":
        detection_output(res, data, prob_threshold)
    elif model_type == "segmentation":
        segmentation_output(res, color_map, log)


def main():
    log.basicConfig(format = "[ %(levelname)s ] %(message)s",
        level = log.INFO, stream = sys.stdout)
    args = build_parser().parse_args()
    try:
        net, plugin, data = prepare_model(log, args.model, args.weights,
            args.cpu_extension, args.device, args.plugin_dir, args.input)
        net.batch_size = args.batch_size
        images = prepare_data(net, data)
        log.info("Loading model to the plugin")
        exec_net = plugin.load(network = net, num_requests = args.requests)
        log.info("Starting inference ({} iterations)".format(args.number_iter))
        res, time = infer_async(images, exec_net, net, args.number_iter)
        infer_output(res, images, data, args.labels, args.number_top,
            args.prob_threshold, args.color_map, log, args.model_type)
        del net
        del exec_net
        del plugin
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))

if __name__ == '__main__':
    sys.exit(main() or 0)

