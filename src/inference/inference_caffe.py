import sys
import os
import argparse
import numpy as np
from PIL import Image
import caffe
import inference_output as io
import logging as log
import postprocessing_data as pp
from time import time
from utils import create_list_images

def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help = 'Path to an .caffemodel \
        file with a trained weights.', required = True, type = str, dest = 'model_caffemodel')
    parser.add_argument('-w', '--weights', help = 'Path to an .prototxt file \
        with a trained model.', required = True, type = str, dest = 'model_prototxt')
    parser.add_argument('-i', '--input', help = 'Path to data', required = True, type = str, 
        nargs = '+', dest = 'input')
    parser.add_argument('-b', '--batch_size', help = 'Size of the  \
        processed pack', default = 1, type = int, dest = 'batch_size')
    parser.add_argument('-l', '--labels', help = 'Labels mapping file',
        default = None, type = str, dest = 'labels')
    parser.add_argument('-nt', '--number_top', help = 'Number of top results',
        default = 10, type = int, dest = 'number_top')
    parser.add_argument('-t', '--task', help = 'Output processing method: \
        1.classification 2.detection 3.segmentation. \
        Default: without postprocess',
        default = 'feedforward', type = str, dest = 'task')
    parser.add_argument('--color_map', help = 'Classes color map',
        type = str, default = None, dest = 'color_map')
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float, dest = 'threshold')
    parser.add_argument('-ni', '--number_iter', help = 'Number of inference \
        iterations', default = 1, type = int, dest = 'number_iter')
    #parser.add_argument('-mi', '--mininfer', help = 'Min inference time of single pass',
    #    type = float, default = 0.0, dest = 'mininfer')
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool, dest = 'raw_output')
    return parser


def input_reshape(net, batch_size):
    channels = net.blobs['data'].data.shape[1]
    height = net.blobs['data'].data.shape[2]
    width = net.blobs['data'].data.shape[3]
    net.blobs['data'].reshape(batch_size, channels, height, width)
    net.reshape()

    return net


def load_network(caffemodel, prototxt, batch_size):
    caffe.set_mode_cpu()
    # загружаем сеть
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    # Меняем параметры местами, чтобы корректно обработать пришедшую картинку
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_channel_swap('data', (2,1,0))
    transformer.set_raw_scale('data', 255.0)

    if batch_size > 1:
        net = input_reshape(net, batch_size)

    return net, transformer


def load_images_to_network(input, net, transformer):
    image_paths = create_list_images(input)
    for i in range(len(image_paths)):
        im = np.array(Image.open(image_paths[i]))
        net.blobs['data'].data[i,:,:,:] = transformer.preprocess('data', im)


def process_result(batch_size, inference_time, total_time):
    inference_time = pp.three_sigma_rule(inference_time)
    average_time = pp.calculate_average_time(inference_time)
    latency = pp.calculate_latency(inference_time)
    fps = pp.calculate_fps(batch_size, latency)
    return average_time, latency, fps


def result_output(average_time, fps, latency, log):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))
    log.info('Latency : {0:.3f}'.format(latency))


def raw_result_output(average_time, fps, latency):
    print('{0:.3f},{1:.3f},{2:.3f}'.format(average_time, fps, latency))


def inference_caffe(batch_size, net, number_iter, input, transformer):
    time_infer = []
    t0_total = time()
    for i in range(number_iter):
        load_images_to_network(input, net, transformer)
        t0 = time()
        result = net.forward()
        t1 = time()
        time_infer.append(t1 - t0)
    t1_total = time()
    inference_total_time = t1_total - t0_total
    return result, time_infer, inference_total_time


def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    args = build_argparser().parse_args()
    
    try:
        net, transformer = load_network(args.model_caffemodel, 
            args.model_prototxt, args.batch_size)

        # Прямой проход по сети
        result, inference_time, total_time = inference_caffe(args.batch_size, 
            net, args.number_iter, args.input, transformer)

        # Результаты
        time, latency, fps = process_result(args.batch_size, inference_time, total_time)

        # Вывод
        input = create_list_images(args.input)
        if not args.raw_output:
            io.infer_output(net, result, input, args.labels, args.number_top,
                args.threshold, args.color_map, log, args.task)
            result_output(time, fps, latency, log)
        else:
            raw_result_output(time, fps, latency)
        
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)
    

if __name__ == '__main__':
   sys.exit(main() or 0)

