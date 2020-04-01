import cv2
import sys
import utils
import argparse
import numpy as np
import logging as log
import postprocessing_data as pp
from time import time
from io_adapter import io_adapter
from transformer import transformer
from io_model_wrapper import openvino_io_model_wrapper


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
    parser.add_argument('-t', '--task', help = 'Output processing method. \
        Default: without postprocess',
        choices = ['classification', 'detection', 'segmentation', 'recognition-face',
        'person-attributes', 'age-gender', 'gaze', 'head-pose', 'person-detection-asl',
        'adas-segmentation', 'road-segmentation', 'license-plate', 'instance-segmentation',
        'single-image-super-resolution', 'sphereface'],
        default = 'feedforward', type = str, dest = 'task')
    parser.add_argument('--color_map', help = 'Classes color map',
        type = str, default = None, dest = 'color_map')
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float, dest = 'threshold')
    parser.add_argument('-mi', '--mininfer', help = 'Min inference time of single pass',
        type = float, default = 0.0, dest = 'mininfer')
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool, dest = 'raw_output')
    return parser


def infer_sync(exec_net, number_iter, get_slice):
    result = None
    time_infer = []
    slice_input = None
    if number_iter == 1:
        slice_input = get_slice(0)
        t0 = time()
        result = exec_net.infer(inputs = slice_input)
        time_infer.append((time() - t0))
    else:
        for i in range(number_iter):
            slice_input = get_slice(i)
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
        model_wrapper = openvino_io_model_wrapper()
        data_transformer = transformer()
        io = io_adapter.get_io_adapter(args, model_wrapper, data_transformer)
        iecore = utils.create_ie_core(args.extension, args.cldnn_config, args.device,
            args.nthreads, None, 'sync', log)
        net = utils.create_network(args.model_xml, args.model_bin, log)
        input_shapes = utils.get_input_shape(model_wrapper, net)
        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        net.batch_size = args.batch_size
        log.info('Prepare input data')
        io.prepare_input(net, args.input)
        log.info('Create executable network')
        config = {}
        if args.priority:
            config.update({'MULTI_DEVICE_PRIORITIES': args.priority})
        exec_net = iecore.load_network(network = net, device_name = args.device, config = config)
        log.info('Starting inference ({} iterations) on {}'.
            format(args.number_iter, args.device))
        result, time = infer_sync(exec_net, args.number_iter, io.get_slice_input)
        average_time, latency, fps = process_result(time, args.batch_size, args.mininfer)
        if not args.raw_output:
            io.process_output(result, log)
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
