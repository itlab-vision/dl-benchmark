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
    parser.add_argument('--default_device', help = 'Default device for heterogeneous inference',
        choices = ['CPU', 'GPU', 'MYRIAD', 'FGPA'], 
        default = None, type = str, dest = 'default_device')
    parser.add_argument('-p', '--priority', help = 'Priority for \
        multi-device inference in descending order. \
        Use format <Device1>,<Device2> First device has top priority',
        default = None, type = str, dest = 'priority')
    parser.add_argument('-a', '--affinity', help = 'Path to file \
        with affinity per layer in format <layer> <device> \
        for heterogeneous inference', default = None,
        type = str, dest = 'affinity')
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
    parser.add_argument('--dump', help = 'Dump information about the model exectution',
        type = bool, default = False, dest = 'dump')
    parser.add_argument('-t', '--task', help = 'Output processing method. \
        Default: without postprocess',
        choices = ['classification', 'detection', 'segmentation', 'recognition-face',
        'person-attributes', 'age-gender', 'gaze', 'head-pose', 'person-detection-asl',
        'adas-segmentation', 'road-segmentation', 'license-plate', 'instance-segmentation',
        'single-image-super-resolution', 'sphereface', 'person-detection-action-recognition-old',
        'person-detection-action-recognition-new', 'person-detection-raisinghand-recognition',
        'person-detection-action-recognition-teacher', 'human-pose-estimation', 
        'action-recognition-encoder', 'driver-action-recognition-encoder', 'reidentification', 
        'driver-action-recognition-decoder', 'action-recognition-decoder', 'face-detection', 
	'yolo_v2', 'yolo_v2_tiny'],
        default = 'feedforward', type = str, dest = 'task')
    parser.add_argument('--color_map', help = 'Classes color map', 
        default = None, type = str, dest = 'color_map')
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float, dest = 'threshold')
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool, dest = 'raw_output')
    return parser


def infer_async(exec_net, number_iter, get_slice):
    result = None
    requests = exec_net.requests
    for i in range(len(requests)):
        utils.set_input_to_blobs(requests[i], get_slice(i))
    iteration = len(requests)
    inference_time = time()
    for request in requests:
        request.async_infer()
    while iteration < number_iter:
        idle_id = exec_net.get_idle_request_id()
        if idle_id < 0:
            exec_net.wait(num_requests=1)
            idle_id = exec_net.get_idle_request_id()
        utils.set_input_to_blobs(requests[idle_id], get_slice(iteration))
        requests[idle_id].async_infer()
        iteration += 1
    exec_net.wait()
    inference_time = time() - inference_time
    if number_iter == 1:
        list = [copy(request.outputs) for request in requests]
        result = dict.fromkeys(list[0].keys(), None)
        for key in result:
            result[key] = np.concatenate([array[key] for array in list], axis = 0)
    return result, inference_time


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
            args.nthreads, args.nstreams, args.dump, 'async', log)
        net = utils.create_network(iecore, args.model_xml, args.model_bin, log)
        utils.configure_network(iecore, net, args.device, args.default_device, args.affinity)
        input_shapes = utils.get_input_shape(model_wrapper, net)
        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        utils.reshape_input(net, args.batch_size)
        log.info('Prepare input data')
        io.prepare_input(net, args.input)
        log.info('Create executable network')
        exec_net = utils.load_network(iecore, net, args.device, args.priority, args.requests)
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
