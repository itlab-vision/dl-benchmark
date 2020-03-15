import cv2
import sys
import utils
import argparse
import numpy as np
import logging as log
import postprocessing_data as pp
from time import time
from io_adapter import io_adapter


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help = 'Path to an .xml \
        file with a trained model.', required = True, type = str, dest = 'model_xml')
    parser.add_argument('-w', '--weights', help = 'Path to an .bin file \
        with a trained weights.', required = True, type = str, dest = 'model_bin')
    parser.add_argument('-i', '--input', help = 'Data for input layers in format: \
        input_layer_name:path_to_image1,path_to_image2.. \
        or input_layer_name:path_to_folder_with_images', required = True, type = str,
        nargs = '+', dest = 'input')
    parser.add_argument('-b', '--batch_size', help = 'Size of the  \
        processed pack', default = 1, type = int, dest = 'batch_size')
    parser.add_argument('-l', '--extension', 
        help = 'Path to MKLDNN (CPU, MYRIAD) custom layers OR Path to CLDNN config.',
        type = str, default = None, dest = 'extension')
    parser.add_argument('-d', '--device', help = 'Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)', default = 'CPU', type = str, dest = 'device')
    parser.add_argument('--labels', help = 'Labels mapping file',
        default = None, type = str, dest = 'labels')
    parser.add_argument('-nt', '--number_top', help = 'Number of top results',
        default = 10, type = int, dest = 'number_top')
    parser.add_argument('-ni', '--number_iter', help = 'Number of inference \
        iterations', default = 1, type = int, dest = 'number_iter')
    parser.add_argument('-nthreads', '--number_threads', help = 'Number of threads. \
        (Max by default)', type = int, default = None, dest = 'nthreads')
    parser.add_argument('-t', '--task', help = 'Output processing method. \
        Default: without postprocess',
        choices = ['classification', 'detection', 'segmentation', 'recognition-face',
        'person-attributes', 'age-gender', 'gaze'], default = 'feedforward', type = str,
        dest = 'task')
    parser.add_argument('--color_map', help = 'Classes color map',
        type = str, default = None, dest = 'color_map')
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float, dest = 'threshold')
    parser.add_argument('-mi', '--mininfer', help = 'Min inference time of single pass',
        type = float, default = 0.0, dest = 'mininfer')
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool, dest = 'raw_output')
    return parser


def infer_sync(input, batch_size, exec_net, number_it):
    size = batch_size
    result = None
    time_infer = []
    slice_input = dict.fromkeys(input.keys(), None)
    if number_it == 1:
        for key in input:
            slice_input[key] = input[key][0:batch_size]
        t0 = time()
        result = exec_net.infer(inputs = slice_input)
        time_infer.append((time() - t0))
    else:
        for i in range(number_it):
            for key in input:
                slice_input[key] = input[key][(i * size) % len(input[key]):
                    (((i + 1) * size - 1) % len(input[key])) + 1:]
            t0 = time()
            exec_net.infer(inputs = slice_input)
            time_infer.append((time() - t0))
    return result, time_infer


def process_result(inference_time, batch_size, min_infer_time):
    correct_time = pp.delete_incorrect_time(inference_time, min_infer_time)
    correct_time = pp.three_sigma_rule(correct_time)
    average_time = pp.calculate_average_time(correct_time)
    latency = pp.calculate_latency(correct_time)
    fps = pp.calculate_fps(batch_size, latency)
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
        io = io_adapter.get_io_adapter(args)
        iecore = utils.create_ie_core(args.extension, args.device,
            args.nthreads, None, 'sync', log)
        net = utils.create_network(args.model_xml, args.model_bin, log)
        input_shapes = utils.get_input_shape(net)
        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        net.batch_size = args.batch_size
        log.info('Prepare input data')
        input = io.prepare_input(net, args.input)
        log.info('Create executable network')
        exec_net = iecore.load_network(network = net, device_name = args.device)
        log.info('Starting inference ({} iterations) on {}'.
            format(args.number_iter, args.device))
        result, time = infer_sync(input, net.batch_size, exec_net, args.number_iter)
        average_time, latency, fps = process_result(time, args.batch_size, args.mininfer)
        if not args.raw_output:
            io.process_output(net, result, log)
            result_output(average_time, fps, latency, log)
        else:
            raw_result_output(average_time, fps, latency)
        del net
        del exec_net
        del iecore
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)