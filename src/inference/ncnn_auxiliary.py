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
    elif device == 'NVIDIA_GPU':
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


def prepare_output(result, task):
    if task == 'feedforward':
        return {}
    if task == 'classification':
        return {'classification': np.array(result)}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')
