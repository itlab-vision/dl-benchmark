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
from transformer import transformer
from io_model_wrapper import openvino_io_model_wrapper


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
        help = 'Path to MKLDNN (CPU, MYRIAD) custom layers',
        type = str, default = None, dest = 'extension')
    parser.add_argument('-c', '--cldnn_config', 
        help = 'Path to CLDNN config.',
        type = str, default = None, dest = 'cldnn_config')
    parser.add_argument('-d', '--device', help = 'Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Support HETERO and MULTI plugins. \
        Use HETERO:<Device1>,<Device2>,... for HETERO plugin. \
        Use MULTI:<Device1>,<Device2>,... for MULTI plugin. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)', default = 'CPU', type = str, dest = 'device')
    parser.add_argument('-p', '--priority', help = 'Priority for \
        multi-device inference in descending order. \
        Use format <Device1>,<Device2> First device has top priority',
        default = None, type = str, dest = 'priority')
    parser.add_argument('--labels', help = 'Labels mapping file',
        default = None, type = str, dest = 'labels')
    parser.add_argument('-nt', '--number_top', help = 'Number of top results',
        default = 10, type = int, dest = 'number_top')
    parser.add_argument('-ni', '--number_iter', help = 'Number of inference \
        iterations', default = 1, type = int, dest = 'number_iter')
    parser.add_argument('-nthreads', '--number_threads', help = 'Number of threads \
        to use for inference on the CPU. (Max by default)',
        type = int, default = None, dest = 'nthreads')
    parser.add_argument('-nstreams', '--number_streams', help = 'Number of streams \
        to use for inference on the CPU/GPU. \
        For HETERO and MULTI use format <Device1>:<NStreams1>,<Device2>:<Nstreams2>... \
        or just <nstreams>. Default value is determined automatically for a device', 
        type = str, default = None, dest = 'nstreams')
    parser.add_argument('-t', '--task', help = 'Output processing method. \
        Default: without postprocess',
        choices = ['classification', 'detection', 'segmentation', 'recognition-face',
        'person-attributes', 'age-gender', 'gaze', 'head-pose', 'person-detection-asl',
        'adas-segmentation', 'road-segmentation', 'license-plate', 'instance-segmentation',
        'single-image-super-resolution', 'sphereface'],
        default = 'feedforward', type = str, dest = 'task')
    parser.add_argument('--color_map', help = 'Classes color map', 
        default = None, type = str, dest = 'color_map')
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float, dest = 'threshold')
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool, dest = 'raw_output')
    return parser


def infer_async(exec_net, number_iter, get_slice):
    requests_counter = len(exec_net.requests)
    result = None
    slice_input = None
    if number_iter == 1:
        time_s = time()
        for request_id in range(requests_counter):
            slice_input = get_slice(request_id)
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
                    slice_input = get_slice(iteration)
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
        model_wrapper = openvino_io_model_wrapper()
        data_transformer = transformer()
        io = io_adapter.get_io_adapter(args, model_wrapper, data_transformer)
        iecore = utils.create_ie_core(args.extension, args.cldnn_config, args.device,
            args.nthreads,args.nstreams, 'async', log)
        net = utils.create_network(args.model_xml, args.model_bin, log)
        input_shapes = utils.get_input_shape(model_wrapper, net)
        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        net.batch_size = args.batch_size
        log.info('Prepare input data')
        io.prepare_input(net, args.input)
        log.info('Create executable network')
        config = {}
        if 'MULTI' in args.device and args.priority:
            config.update({'MULTI_DEVICE_PRIORITIES': args.priority})
        exec_net = iecore.load_network(network = net, device_name = args.device,
            config = config, num_requests = (args.requests or 0))
        log.info('Starting inference ({} iterations) with {} requests on {}'.
            format(args.number_iter, len(exec_net.requests), args.device))
        result, time = infer_async(exec_net, args.number_iter, io.get_slice_input)
        average_time, fps = process_result(time, args.batch_size, args.number_iter)
        if not args.raw_output:
            io.process_output(result, log)
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
