import sys
import argparse
import tensorflow as tf  # pylint: disable=E0401
import numpy as np
import logging as log
import postprocessing_data as pp
from time import time
from io_adapter import io_adapter
from transformer import tensorflow_transformer
from io_model_wrapper import tensorflow_io_model_wrapper


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help='Path to an .pb or .meta file with a trained model.', required=True, type=str, dest='model_path')
    parser.add_argument('-i', '--input', help='Path to data', required=True, type=str, nargs='+', dest='input')
    parser.add_argument('-b', '--batch_size', help='Size of the processed pack', default=1, type=int, dest='batch_size')
    parser.add_argument('-l', '--labels', help='Labels mapping file', default=None, type=str, dest='labels')
    parser.add_argument('-nt', '--number_top', help='Number of top results', default=10, type=int, dest='number_top')
    parser.add_argument(
        '-t', '--task',
        help='Output processing method. Default: without postprocess',
        choices=['classification', 'detection', 'yolo_tiny_voc', 'yolo_v2_coco',
                 'yolo_v2_tiny_coco', 'yolo_v3_tf', 'mask-rcnn'],
        default='feedforward', type=str, dest='task'
    )
    parser.add_argument('--color_map', help='Classes color map', type=str, default=None, dest='color_map')
    parser.add_argument('--prob_threshold', help='Probability threshold for detections filtering', default=0.5, type=float, dest='threshold')
    parser.add_argument('-ni', '--number_iter', help='Number of inference iterations', default=1, type=int, dest='number_iter')
    parser.add_argument('--raw_output', help='Raw output without logs', default=False, type=bool, dest='raw_output')
    parser.add_argument('--channel_swap', help='Parameter channel swap', default=[2, 1, 0], type=int, nargs=3, dest='channel_swap')
    parser.add_argument('--mean', help='Parameter mean', default=[0, 0, 0], type=float, nargs=3, dest='mean')
    parser.add_argument('--input_scale', help='Parameter input scale', default=1.0, type=float, dest='input_scale')
    parser.add_argument('-d', '--device', help='Specify the target device to infer on (CPU by default)', default='CPU', type=str, dest='device')
    parser.add_argument('--input_shape', help='Input tensor shape in "height width channels" order', default=None, type=int, nargs=3, dest='input_shape')
    parser.add_argument('--output_names', help='Name of the output tensor', default=None, type=str, nargs='+', dest='output_names')
    parser.add_argument('--num_inter_threads', help='Number of threads used for parallelism between independent operations', default=None, type=int, dest='num_inter_threads')
    parser.add_argument('--num_intra_threads', help='Number of threads used within an individual op for parallelism', default=None, type=int, dest='num_intra_threads')
    return parser


def get_input_shape(io_model_wrapper, model):
    layer_shapes = dict()
    layer_names = io_model_wrapper.get_input_layer_names(model)
    for input_layer in layer_names:
        shape = ''
        for dem in io_model_wrapper.get_input_layer_shape(model, input_layer):
            shape += '{0}x'.format(dem)
        shape = shape[:-1]
        layer_shapes.update({input_layer: shape})
    return layer_shapes


def prepare_output(result, outputs_name, task):
    if len(result) != len(outputs_name):
        raise ValueError('The number of output layers does not match the number of resulting tensors.')
    if task in ['yolo_tiny_voc', 'yolo_v2_coco', 'yolo_v2_tiny_coco', 'yolo_v3_tf']:
        result = [res.transpose(0, 3, 1, 2) for res in result]
    elif task in ['detection']:
        outputs_name = ['detection_output']
        batch = len(result[0])
        n = int(max(result[3]))
        new_result = np.zeros(shape=(1, 1, batch * n, 7))
        for bb in range(batch):
            num_detections = int(result[3][bb])
            for idx in range(num_detections):
                label = result[0][bb][idx]
                conf = result[1][bb][idx]
                coords = result[2][bb][idx]
                coords[0], coords[1] = coords[1], coords[0]
                coords[2], coords[3] = coords[3], coords[2]
                new_result[0][0][bb * n + idx] = [bb, label, conf, *coords]
        result = [new_result]
    elif task in ['mask-rcnn']:
        outputs_name = ['reshape_do_2d', 'masks']
        num_detections = int(result[3][0])
        detection_result = np.zeros(shape=(num_detections + 1, 7))
        mask = result[4]
        new_mask = np.zeros(shape=(num_detections, mask.shape[1], mask.shape[2], mask.shape[3]))
        for idx in range(num_detections):
            label = int(result[0][0][idx])
            conf = result[1][0][idx]
            coords = result[2][0][idx]
            coords[0], coords[1] = coords[1], coords[0]
            coords[2], coords[3] = coords[3], coords[2]
            detection_result[idx] = [0, label, conf, *coords]
            new_mask[idx][label - 1] = mask[0][idx]
        detection_result[num_detections][0] = -1
        result = [detection_result, new_mask]
    return {outputs_name[i]: result[i] for i in range(len(result))}


def load_network(tensorflow, model, output_names=None):
    suffix = model.rpartition('.')[2]
    if suffix == 'pb':
        return load_model_from_pb(tensorflow, model)
    elif suffix == 'meta':
        return load_model_from_checkpoint(tensorflow, model, output_names)
    else:
        raise ValueError('Unsupported file format of the model: {}'.format(suffix))


def load_model_from_pb(tensorflow, model):
    with tensorflow.io.gfile.GFile(model, 'rb') as f:
        graph_def = tensorflow.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
    with tensorflow.Graph().as_default() as graph:
        tensorflow.import_graph_def(graph_def)
        return graph


def load_model_from_checkpoint(tensorflow, model, output_names):
    graph = tensorflow.Graph()
    prefix = model.rpartition('.')[0]
    with tf.compat.v1.Session() as sess:
        saver = tf.compat.v1.train.import_meta_graph(model)
        sess.run(tf.compat.v1.global_variables_initializer())
        saver.restore(sess, prefix)
        frozen_graph_def = tf.compat.v1.graph_util.convert_variables_to_constants(
            sess,
            sess.graph_def,
            output_names)
    with graph.as_default():
        tensorflow.import_graph_def(frozen_graph_def, name='')
    return graph


def inference_tensorflow(graph, inputs_names, outputs_names, number_iter, get_slice, num_intra_threads, num_inter_threads):
    result = None
    time_infer = []
    slice_input = None
    try:
        tensors = [graph.get_tensor_by_name('import/{}:0'.format(name)) for name in outputs_names]
    except Exception:
        tensors = [graph.get_tensor_by_name('{}:0'.format(name)) for name in outputs_names]
    config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=num_intra_threads, inter_op_parallelism_threads=num_inter_threads)
    with tf.compat.v1.Session(graph=graph, config=config) as sess:
        if number_iter == 1:
            slice_input = get_slice(0)
            t0 = time()
            result = sess.run(tensors, slice_input)
            t1 = time()
            time_infer.append(t1 - t0)
        else:
            for i in range(number_iter):
                slice_input = get_slice(i)
                t0 = time()
                sess.run(tensors, slice_input)
                t1 = time()
                time_infer.append(t1 - t0)
        return result, time_infer


def process_result(batch_size, inference_time):
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


def create_dict_for_transformer(args):
    dictionary = {'channel_swap': args.channel_swap, 'mean': args.mean,
                  'input_scale': args.input_scale}
    return dictionary


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    try:
        model_wrapper = tensorflow_io_model_wrapper(args)
        data_transformer = tensorflow_transformer(create_dict_for_transformer(args))
        io = io_adapter.get_io_adapter(args, model_wrapper, data_transformer)
        log.info('Loading network files:\n\t {0}'.format(args.model_path))
        graph = load_network(tf, args.model_path, args.output_names)
        input_shapes = get_input_shape(model_wrapper, graph)
        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        log.info('Prepare input data')
        io.prepare_input(graph, args.input)
        log.info('Starting inference ({} iterations)'.format(args.number_iter))

        inputs_names = model_wrapper.get_input_layer_names(graph)
        outputs_names = model_wrapper.get_outputs_layer_names(graph, args.output_names)
        result, inference_time = inference_tensorflow(graph, inputs_names, outputs_names,
                                                      args.number_iter, io.get_slice_input,
                                                      args.num_intra_threads, args.num_inter_threads)

        time, latency, fps = process_result(args.batch_size, inference_time)
        if not args.raw_output:
            result = prepare_output(result, outputs_names, args.task)
            io.process_output(result, log)
            result_output(time, fps, latency, log)
        else:
            raw_result_output(time, fps, latency)
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
