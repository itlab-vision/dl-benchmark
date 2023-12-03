import os
import sys
import numpy as np
from pathlib import Path

from ncnn.model_zoo import get_model

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
sys.path.append(str(Path(__file__).parent.parent.parent))
from logger_conf import configure_logger  # noqa: E402
log = configure_logger()


def get_device(device, task):
    log.info(f'Get device for {task}')
    if device == 'CPU':
        log.info(f'{task.title()} will be executed on {device}')
        return False
    elif device == 'GPU':
        log.info(f'{task.title()} will be executed on {device}')
        return True
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')


def load_model(model, num_threads, device, task):
    use_gpu = get_device(device, task)
    net = get_model(model, num_threads=num_threads, use_gpu=use_gpu)
    return net


def get_images_names(images_path):
    images_path = os.path.abspath(images_path[0])
    images_path_list = [os.path.join(images_path, file) for file in os.listdir(images_path)]
    return images_path_list


def process_output(io, number_iter, number_top, images_path, result, log):
    if number_iter != 1:
        log.warning('Model output is processed only for the number iteration = 1')
        return

    log.info('Inference results')
    images_path_list = get_images_names(images_path)
    total_images = len(images_path_list)

    io.load_labels_map('image_net_synset.txt')
    for result_layer_index, cls_scores in result.items():
        log.info('Top {0} results:'.format(number_top))

        top_ind = np.argsort(cls_scores)[::-1][0:number_top]  # noqa: PLE1130
        # https://github.com/gforcada/flake8-pep3101/issues/23
        log.info('Result for image {0}'.format(images_path_list[result_layer_index % total_images]))  # noqa: S001
        for id_ in top_ind:
            det_label = io._labels_map[id_] if io._labels_map else '#{0}'.format(id_)
            log.info('\t{:.7f} {}'.format(cls_scores[id_], det_label))  # noqa: P101
