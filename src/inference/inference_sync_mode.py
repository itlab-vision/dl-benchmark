import sys
import os
import argparse 
import numpy as np
import logging as log
import postprocessing_data as pp
from time import time
import cv2
from openvino.inference_engine import IENetwork, IEPlugin


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help = 'Path to an .xml \
        file with a trained model.', required = True, type = str)
    parser.add_argument('-w', '--weights', help = 'Path to an .bin file \
        with a trained weights.', required = True, type = str)
    parser.add_argument('-i', '--input', help = 'Path to a folder with \
        images or path to an image files', required = True, type = str, nargs = '+')
    parser.add_argument('-b', '--batch_size', help = 'Size of the  \
        processed pack', default = 1, type = int)
    parser.add_argument('-l', '--cpu_extension', help = 'MKLDNN \
        (CPU)-targeted custom layers.Absolute path to a shared library \
        with the kernels implementation', type = str, default = None)
    parser.add_argument('-pp', '--plugin_dir', help = 'Path to a plugin \
        folder', type = str, default = None)
    parser.add_argument('-d', '--device', help = 'Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)', default = 'CPU', type = str)
    parser.add_argument('--labels', help = 'Labels mapping file',
        default = None, type = str)
    parser.add_argument('-nt', '--number_top', help = 'Number of top results',
        default = 10, type = int)
    parser.add_argument('-ni', '--number_iter', help = 'Number of inference \
        iterations', default = 1, type = int)
    parser.add_argument('-pc', '--perf_counts', help = 'Report performance \
        counters', action = 'store_true', default = False)
    parser.add_argument('-t', '--model_type', help = 'Choose model type: \
        0.without output 1.classification 2.detection 3.segmentation',
        default = '', type = str)
    parser.add_argument('--color_map', help = 'Classes color map', type = str, default = None)
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float)
    parser.add_argument('-mi', '--mininfer', help = 'Min inference time of single pass',
        type = float, default = 0.0)
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool)
    return parser


def convert_image(net, data):
    n, c, h, w = net.inputs[next(iter(net.inputs))].shape
    images = np.ndarray(shape = (len(data), c, h, w))
    for i in range(n):
        image = cv2.imread(data[i])
        if image.shape[:-1] != (h, w):
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))
        images[i] = image
    return images


def prepare_model(model, weights, cpu_extension, device, plugin_dirs, input, log):
    model_xml = model
    model_bin = weights
    plugin = IEPlugin(device = device, plugin_dirs = plugin_dirs)
    if cpu_extension and 'CPU' in device:
        plugin.add_cpu_extension(args.cpu_extension)
    log.info('Loading network files:\n\t{}\n\t{}'.format(model_xml, model_bin))
    net = IENetwork.from_ir(model = model_xml, weights = model_bin)
    if 'CPU' in plugin.device:
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error('Following layers are not supported by the plugin for specified device {}:\n {}'.
                      format(plugin.device, ', '.join(not_supported_layers)))
            log.error('Please try to specify cpu extensions library path in sample\'s command line parameters using -l '
                      'or --cpu_extension command line argument')
            sys.exit(1)
    if os.path.isdir(input[0]):
        data = [os.path.join(input[0], file) for file in os.listdir(input[0])]
    else:
        data = input
    return net, plugin, data


def infer_sync(images, exec_net, net, number_it):
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    size = net.batch_size
    result = []
    time_infer = []
    for i in range(number_it):
        t0 = time()
        res = exec_net.infer(inputs = {input_blob : images[(i * size) % len(images) : (((i + 1) * size - 1) % len(images)) + 1:]})
        time_infer.append((time() - t0))
        for j in range(size):
            result.append(res[out_blob][j])
    return result, time_infer


def classification_output(res, number_top, inputs, labels, log):
    log.info('Top {} results: '.format(number_top))
    if labels:
        with open(labels, 'r') as f:
            labels_map = [x.split(sep = ' ', maxsplit = 1)[-1].strip() for x in f]
    else:
        labels_map = None
    for i, probs in enumerate(res):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-number_top:][::-1]
        print('Image {}\n'.format(inputs[i]))
        for id in top_ind:
            det_label = labels_map[id] if labels_map else '#{}'.format(id)
            print('{:.7f} {}'.format(probs[id], det_label))
        print('\n')


def segmentation_output(res, color_map, log):
    c = 3
    h, w = res.shape[2:]
    if not color_map:
        color_map = 'color_map.txt'
    classes_color_map = []
    with open(color_map, 'r') as f:
        for line in f:
            classes_color_map.append([int(x) for x in line.split()]) 
    for batch, data in enumerate(res):
        classes_map = np.zeros(shape = (h, w, c), dtype = np.int)
        for i in range(h):
            for j in range(w):
                if len(data[:, i, j]) == 1:
                    pixel_class = int(data[:, i, j])
                else:
                    pixel_class = np.argmax(data[:, i, j])
                classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
        out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch))
        cv2.imwrite(out_img, classes_map)
        log.info('Result image was saved to {}'.format(out_img))


def detection_output(res, data, prob_threshold, log):
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
        out_img = os.path.join(os.path.dirname(__file__), 'out_detection_{}.JPEG'.format(i))
        cv2.imwrite(out_img, image)
        log.info('Result image was saved to {}'.format(out_img))    


def infer_output(res, net, type_model, labels, color_map, inputs, number_top, 
        prob_threshold, images, log):
    if type_model == '':
        return
    elif type_model == 'classification':
        classification_output(res, number_top, inputs, labels, log)
    elif type_model == 'segmentation':
        segmentation_output(res, color_map, log)
    elif type_model == 'detection':
        detection_output(res, inputs, prob_threshold, log)


def process_result(inference_time, batch_size, min_infer_time):
    correct_time = pp.delete_incorrect_time(inference_time, min_infer_time)
    correct_time = pp.three_sigma_rule(correct_time)
    average_time = pp.calculate_average_time(correct_time)
    latency = pp.calculate_latency(correct_time)
    fps = pp.calculate_fps(batch_size, average_time)
    return average_time, latency, fps


def result_output(average_time, fps, latency):
    print('Average time of single pass : {0:.3f}'.format(average_time))
    print('FPS : {0:.3f}'.format(fps))
    print('Latency : {0:.3f}'.format(latency))


def raw_result_output(average_time, fps, latency):
    print('{0:.3f},{0:.3f},{0:.3f}'.format(average_time, fps, latency))


def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    args = build_argparser().parse_args()
    try:
        net, plugin, data = prepare_model(args.model, args.weights,
            args.cpu_extension, args.device, args.plugin_dir, args.input, log)
        net.batch_size = args.batch_size
        images = convert_image(net, data)log.info('Loading model to the plugin')
        exec_net = plugin.load(network = net)
        log.info('Starting inference ({} iterations)'.format(args.number_iter))
        res, time = infer_sync(images, exec_net, net, args.number_iter)
        average_time, latency, fps = process_result(time, args.batch_size, args.mininfer)
        if not args.raw_output:
            infer_output(res, net, args.model_type, args.labels, args.color_map, data, args.number_top, 
                args.prob_threshold, images, log)
            result_output(average_time, latency, fps)
        else:
            raw_result_output(average_time, fps, latency)
        del net
        del exec_net
        del plugin
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)