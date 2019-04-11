import sys
import argparse
import numpy as np
import logging as log
import prepare_data as pd
import inference_output as io
import postprocessing_data as pp
from time import time
import copy
import cv2


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help = 'Path to an .xml \
        file with a trained model.', required = True, type = str)
    parser.add_argument('-w', '--weights', help = 'Path to an .bin file \
        with a trained weights.', required = True, type = str)
    parser.add_argument('-i', '--input', help = 'Path to a folder with \
        images or path to an image files', required = True, type = str, nargs = '+')
    parser.add_argument('-r', '--requests', help = 'A positive integer value \
        of infer requests to be created. Number of infer requests may be \
        limited by device capabilities', required = True, type = int)
    parser.add_argument('-b', '--batch_size', help = 'Size of the  \
        processed pack', default = 1, type = int)
    parser.add_argument('-t', '--task', help = 'Output processing method: \
        1.classification 2.detection 3.segmentation. \
        Default: without postprocess',
        default = 'feedforward', type = str)
    parser.add_argument('-l', '--cpu_extension', help = 'MKLDNN \
        (CPU)-targeted custom layers. Absolute path to a shared library \
        with the kernels implementation', type = str, default = None)
    parser.add_argument('-pp', '--plugin_dir', help = 'Path to a plugin \
        folder', type = str, default = None)
    parser.add_argument('-d', '--device', help = 'Specify the target \
        device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
        Sample will look for a suitable plugin for device specified \
        (CPU by default)', default = ['CPU'], type = str, nargs = '+')
    parser.add_argument('-nt', '--number_top', help = 'Number of top results',
        default = 10, type = int)
    parser.add_argument('-ni', '--number_iter', help = 'Number of inference \
        iterations', default = 1, type = int)
    parser.add_argument('-nthreads', '--number_threads', help = 'Number of threads. \
        (Max by default)', type = int, default = None)
    parser.add_argument('-nstreams', '--number_streams', help = 'Number of streams.', 
        type = int, default = None)
    parser.add_argument('--labels', help = 'Labels mapping file',
        default = None, type = str)
    parser.add_argument('--prob_threshold', help = 'Probability threshold \
        for detections filtering', default = 0.5, type = float)
    parser.add_argument('--color_map', help = 'Classes color map', 
        default = None, type = str)
    parser.add_argument('--raw_output', help = 'Raw output without logs',
        default = False, type = bool)
    return parser


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
                frame = cv2.resize(frame, (w, h))       
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
    for j in range(number_iter):
        infer_request_handle = exec_net.start_async(request_id = 0,
            inputs = {input_blob: images[j * size % len(images): \
             ((j + 1) * size - 1) % len(images) + 1]})
        infer_status = infer_request_handle.wait()
        res.append(copy.copy(infer_request_handle.outputs[next(iter(model.outputs))]))   
    log.info('Processing output blob')
    time_e = time() - time_s
    result = []
    for r_l1 in res:
        for r_l2 in r_l1:
            result.append(r_l2)
    res = np.asarray(result[0: len(images)])
    return res, time_e


def start_infer_two_req(images, exec_net, model, number_iter):
    input_blob = next(iter(model.inputs))
    curr_request_id = 0
    prev_request_id  = 1
    time_s = time()
    size = model.batch_size
    res = []
    if (len(images) % model.batch_size != 0):
        raise ValueError('Wrong batch_size')
    for j in range(number_iter):
        exec_net.start_async(request_id = curr_request_id,
            inputs = {input_blob: images[j * size % len(images): \
             ((j + 1) * size - 1) % len(images) + 1]})
        if exec_net.requests[prev_request_id].wait(-1) == 0:
            res.append(copy.copy(exec_net.requests[prev_request_id].
                outputs[next(iter(model.outputs))]))
        prev_request_id, curr_request_id = curr_request_id, prev_request_id
    if exec_net.requests[prev_request_id].wait(-1) == 0:
        res.append(copy.copy(exec_net.requests[prev_request_id].
            outputs[next(iter(model.outputs))]))
    time_e = time() - time_s
    result = []
    for r_l1 in res:
        for r_l2 in r_l1:
            result.append(r_l2)
    res = np.asarray(result[0: len(images)])
    return res, time_e


def start_infer_n_req(images, exec_net, model, number_iter):
    input_blob = next(iter(model.inputs))
    requests_counter = len(exec_net.requests)
    requests_images = [-1 for i in range(requests_counter)]
    time_s = time()
    size = model.batch_size
    res = [-1 for i in range(len(images))]
    if (len(images) % model.batch_size != 0):
        raise ValueError('Wrong batch_size')
    requests_status = []
    k = requests_counter
    for request_id in range(requests_counter):
        exec_net.start_async(request_id = request_id,
        inputs = {input_blob: images[request_id * size % len(images): \
        ((request_id + 1) * size - 1) % len(images) + 1]})
        requests_images[request_id] = (request_id * size % len(images), 
            ((request_id + 1) * size - 1) % len(images) + 1)
    while k < number_iter:
        while not len(requests_status):
            for request_id in range(requests_counter):
                if exec_net.requests[request_id].wait(0) == 0:
                    requests_status.append(request_id)
        for request_id in requests_status:
            if not (k < number_iter):
                break
            exec_net.requests[request_id].wait(1)
            start = requests_images[request_id][0]
            r_size = requests_images[request_id][-1]
            tmp_buf = (exec_net.requests[request_id]. 
                        outputs[next(iter(model.outputs))])
            z = 0
            for i in range(start, r_size):
                if type(res[i]) is int:
                    res[i] = copy.copy(tmp_buf[z])
                else:
                    res.append(copy.copy(tmp_buf[z]))
                z += 1
            exec_net.start_async(request_id = request_id,
            inputs = {input_blob: images[k * size % len(images): \
            ((k + 1) * size - 1) % len(images) + 1]})
            requests_images[request_id] = (k * size % len(images), 
            ((k + 1) * size - 1) % len(images) + 1)
            k += 1
        requests_status.clear()
    else:
        for request_id in range(requests_counter):
            if exec_net.requests[request_id].wait(0) != 0:
                    requests_status.append(request_id)
        some_active = True
        while some_active:
            some_active = False
            for request_id in requests_status:
                if (exec_net.requests[request_id].wait(0) != 0):
                   some_active = True
                   break
        for request_id in requests_status:
            exec_net.requests[request_id].wait(1)
            start = requests_images[request_id][0]
            r_size = requests_images[request_id][-1]
            tmp_buf = (exec_net.requests[request_id]. 
                        outputs[next(iter(model.outputs))])
            z = 0
            for i in range(start, r_size):
                if type(res[i]) is int:
                    res[i] = copy.copy(tmp_buf[z])
                else:
                    res.append(copy.copy(tmp_buf[z]))
                z += 1
    res = np.asarray(res[0: len(images)][:])
    time_e = time() - time_s
    return res, time_e           


def infer_async(images, exec_net, model, number_iter):
    if type(images) is str:
        res = start_infer_video(images, exec_net, model, number_iter)
    elif len(exec_net.requests) == 1:
        res = start_infer_one_req(images, exec_net, model, number_iter)
    elif len(exec_net.requests) == 2:
       res = start_infer_two_req(images, exec_net, model, number_iter)
    else:
        res = start_infer_n_req(images, exec_net, model, number_iter)
    return res


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
        net, plugin = pd.prepare_model(log, args.model, args.weights,
            args.cpu_extension, args.device, args.plugin_dir, args.number_threads,
            args.number_streams)
        net.batch_size = args.batch_size
        data = pd.get_input_list(args.input)
        images = pd.prepare_data(net, data)
        log.info('Loading model to the plugin')
        exec_net = plugin.load(network = net, num_requests = args.requests)
        log.info('Starting inference ({} iterations)'.format(args.number_iter))
        res, time = infer_async(images, exec_net, net, args.number_iter)
        average_time, fps = process_result(time, args.batch_size, args.number_iter)
        if not args.raw_output:
            io.infer_output(res, images, data, args.labels, args.number_top,
                args.prob_threshold, args.color_map, log, args.task)
            result_output(average_time, fps, log)
        else:
            raw_result_output(average_time, fps)
        del net
        del exec_net
        del plugin
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)