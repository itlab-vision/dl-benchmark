import sys
import argparse
import numpy as np
import logging as log
import prepare_data as pd
import inference_output as io
import postprocessing_data as pp
from time import time
import cv2


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
    parser.add_argument('-t', '--task', help = 'Output processing method: \
        1.classification 2.detection 3.segmentation. \
        Default: without postprocess',
        default = 'feedforward', type = str)
    parser.add_argument('--color_map', help = 'Classes color map', type = str, default = None)
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float)
    parser.add_argument('-mi', '--mininfer', help = 'Min inference time of single pass',
        type = float, default = 0.0)
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool)
    return parser


def infer_sync(images, exec_net, net, number_it):
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    size = net.batch_size
    result = []
    time_infer = []
    for i in range(number_it):
        t0 = time()
        res = exec_net.infer(inputs = {input_blob : images[(i * size)
            % len(images) : (((i + 1) * size - 1) % len(images)) + 1:]})
        time_infer.append((time() - t0))
        for j in range(size):
            result.append(res[out_blob][j])
    npres = np.asarray(result[0: len(images)])
    return npres, time_infer


def process_result(inference_time, batch_size, min_infer_time):
    correct_time = pp.delete_incorrect_time(inference_time, min_infer_time)
    correct_time = pp.three_sigma_rule(correct_time)
    average_time = pp.calculate_average_time(correct_time)
    latency = pp.calculate_latency(correct_time)
    fps = pp.calculate_fps(batch_size, average_time)
    return average_time, latency, fps


def result_output(average_time, fps, latency, log):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))
    log.info('Latency : {0:.3f}'.format(latency))


def raw_result_output(average_time, fps, latency):
    print('{0:.3f},{1:.3f},{2:.3f}'.format(average_time, fps, latency))


def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    args = build_argparser().parse_args()
    try:
        net, plugin, data = pd.prepare_model(log, args.model, args.weights,
            args.cpu_extension, args.device, args.plugin_dir, args.input)
        net.batch_size = args.batch_size
        images = pd.prepare_data(net, data)
        log.info('Loading model to the plugin')
        exec_net = plugin.load(network = net)
        log.info('Starting inference ({} iterations)'.format(args.number_iter))
        res, time = infer_sync(images, exec_net, net, args.number_iter)
        average_time, latency, fps = process_result(time, args.batch_size, args.mininfer)
        if not args.raw_output:
            io.infer_output(res, images, data, args.labels, args.number_top,
                args.prob_threshold, args.color_map, log, args.task)
            result_output(average_time, fps, latency, log)
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