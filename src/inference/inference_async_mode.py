import cv2
import sys
import utils
import argparse
import numpy as np
import logging as log
import postprocessing_data as pp
from time import time
from copy import copy
from io_adapter import io_adapter


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help = 'Path to an .xml \
        file with a trained model.', required = True, type = str, dest = 'model_xml')
    parser.add_argument('-w', '--weights', help = 'Path to an .bin file \
        with a trained weights.', required = True, type = str, dest = 'model_bin')
    parser.add_argument('-i', '--input', help = 'Data for input layers in format: \
        input_layer_name:path_to_image1,path_to_image2.. \
        or input_layer_name:path_to_folder_with_images', required = True, type = str,
        nargs = '+', dest = 'input')
    parser.add_argument('-r', '--requests', help = 'A positive integer value \
        of infer requests to be created. Number of infer requests may be \
        limited by device capabilities', default = None, type = int, dest = 'requests')
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
    parser.add_argument('-nstreams', '--number_streams', help = 'Number of streams.', 
        type = int, default = None, dest = 'nstreams')
    parser.add_argument('-t', '--task', help = 'Output processing method. \
        Default: without postprocess',
        choices = ['classification', 'detection', 'segmentation', 'recognition-face',
        'person-attributes', 'age-gender', 'gaze', 'head-pose'], 
        default = 'feedforward', type = str, dest = 'task')
    parser.add_argument('--color_map', help = 'Classes color map', 
        default = None, type = str, dest = 'color_map')
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float, dest = 'threshold')
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool, dest = 'raw_output')
    return parser


def infer_async(input, batch_size, exec_net, number_iter):
    requests_counter = len(exec_net.requests)
    size = batch_size
    result = None
    slice_input = dict.fromkeys(input.keys(), None)
    if number_iter == 1:
        time_s = time()
        for request_id in range(requests_counter):
            for key in input:
                slice_input[key] = input[key][request_id * size % len(input[key]):
                    ((request_id + 1) * size - 1) % len(input[key]) + 1]
            exec_net.start_async(request_id = request_id,
                inputs = slice_input)
        for request_id in range(requests_counter):
            exec_net.requests[request_id].wait(-1)
        time_e = time() - time_s
        list = [copy(exec_net.requests[request_id].outputs) for request_id in range(requests_counter)]
        result = dict.fromkeys(list[0].keys(), None)
        for key in result:
            result[key] = np.concatenate([array[key] for array in list], axis = 0)
    else:
        time_s = time()
        iteration = 0
        requests_status = [0 for i in range(requests_counter)]
        while iteration < number_iter:
            for request_id in range(requests_counter):
                if requests_status[request_id] == 0:
                    for key in input:
                        slice_input[key] = input[key][iteration * size % len(input[key]):
                            ((iteration + 1) * size - 1) % len(input[key]) + 1]
                    exec_net.start_async(request_id = request_id,
                        inputs = slice_input)
                    requests_status[request_id] = 1
                    iteration += 1
            for request_id in range(requests_counter):
                if exec_net.requests[request_id].wait(0) == 0:
                    requests_status[request_id] = 0
        for request_id in range(requests_counter):
            exec_net.requests[request_id].wait(-1)
        time_e = time() - time_s
    return result, time_e


def process_result(inference_time, batch_size, iteration_count):
    average_time = inference_time / iteration_count
    fps = pp.calculate_fps(batch_size * iteration_count, inference_time)
    return average_time, fps


def result_output(average_time, fps, log):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))


def raw_result_output(average_time, fps):
    print('{0:.3f},{1:.3f}'.format(average_time, fps))


def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    args = build_parser().parse_args()
    try:
        io = io_adapter.get_io_adapter(args)
        iecore = utils.create_ie_core(args.extension, args.device,
            args.nthreads,args.nstreams, 'async', log)
        net = utils.create_network(args.model_xml, args.model_bin, log)
        input_shapes = utils.get_input_shape(net)
        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        net.batch_size = args.batch_size
        log.info('Prepare input data')
        input = io.prepare_input(net, args.input)
        log.info('Create executable network')
        exec_net = iecore.load_network(network = net, device_name = args.device,
            num_requests = (args.requests or 0))
        log.info('Starting inference ({} iterations) with {} requests on {}'.
            format(args.number_iter, len(exec_net.requests), args.device))
        result, time = infer_async(input, net.batch_size, exec_net, args.number_iter)
        average_time, fps = process_result(time, args.batch_size, args.number_iter)
        if not args.raw_output:
            io.process_output(net, result, log)
            result_output(average_time, fps, log)
        else:
            raw_result_output(average_time, fps)
        del net
        del exec_net
        del iecore
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)