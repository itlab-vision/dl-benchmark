import argparse
import sys
from pathlib import Path
import itertools
import numpy as np

from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from reporter.report_writer import ReportWriter

import cv2
from ncnn.model_zoo import get_model

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402
log = configure_logger()

sys.path.append(str(Path(__file__).parent.parent.parent))


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-m', '--model',
                        help='Model name',
                        choices=['squeezenet', 'shufflenetv2'],
                        default='squeezenet',
                        type=str,
                        dest='model')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results',
                        default=3,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification'],
                        default='classification',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--target_size',
                        help='Parameter image target size',
                        default=256,
                        type=int,
                        dest='target_size')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--num_threads',
                        help='Number of threads',
                        default=4,
                        type=int,
                        dest='num_threads')
    parser.add_argument('--time',
                        required=False,
                        default=0,
                        type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'ncnn_inference_report.json',
                        dest='report_path')
    args = parser.parse_args()

    return args


def inference_ncnn(args, images, number_iter, get_slice, test_duration):
    result = None
    time_infer = []
    log.info(f'Starting inference ({number_iter} iterations)')
    if number_iter == 1:
        slice_input = get_slice(images)
        result, exec_time = infer_slice(args, slice_input)
        time_infer.append(exec_time)
    else:
        time_infer = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice)
    log.info('Inference completed')
    return result, time_infer


def inference_iteration(get_slice):
    slice_input = get_slice(images)
    _, exec_time = infer_slice(args, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(args, slice_input):
    use_gpu = False
    if args.device == 'GPU':
        use_gpu = True
    net = get_model(args.model, num_threads=args.num_threads, use_gpu=use_gpu)
    res = {}
    for i in range(args.batch_size):
        image = slice_input[args.task][i]
        cls_scores = net(image)
        res[i] = cls_scores
    return res


def prepare_input(args, images):
    transformed_input = {}
    opened_images = []
    for image_path in images:
        image = cv2.imread(image_path)
        reshaped_image = cv2.resize(image, (256, 256))
        opened_images.append(reshaped_image)
    transformed_input[args.task] = itertools.cycle(opened_images)
    return transformed_input


def process_output(args, images, result, log):
    if args.number_iter != 1:
        log.warning('Model output is processed only for the number iteration = 1')
        return

    io.load_labels_map('image_net_synset.txt')

    for result_layer_index, cls_scores in result.items():
        log.info('Top {0} results:'.format(args.number_top))

        top_ind = np.argsort(cls_scores)[::-1][0:args.number_top]  # noqa: PLE1130
        log.info('Result for image {0}'.format(images[result_layer_index]))
        for id_ in top_ind:
            det_label = io._labels_map[id_] if io._labels_map else '#{0}'.format(id_)
            log.info('\t{:.7f} {}'.format(cls_scores[id_], det_label))  # noqa: P101


if __name__ == '__main__':
    args = cli_argument_parser()
    io = IOAdapter.get_io_adapter(args, None, None)

    report_writer = ReportWriter()
    report_writer.update_framework_info(name='ncnn')
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    images = io._IOAdapter__create_list_images(args.input)
    io._transformed_input = prepare_input(args, images)
    result, inference_time = inference_ncnn(args, images, args.number_iter,
                                            io.get_slice_input, args.time)
    if not args.raw_output:
        if args.number_iter == 1:
            process_output(args, images, result, log)
