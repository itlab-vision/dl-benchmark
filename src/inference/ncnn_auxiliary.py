import os
import sys
import numpy as np
from pathlib import Path

from ncnn.model_zoo import get_model

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
sys.path.append(str(Path(__file__).parent.parent.parent))
from logger_conf import configure_logger  # noqa: E402
log = configure_logger()

TASK_MAP = {
    'classification': ['squeezenet', 'shufflenetv2'],
    'detection': ['faster_rcnn', 'rfcn', 'mobilenet_ssd', 'mobilenetv2_ssdlite',
                  'mobilenetv3_ssdlite', 'squeezenet_ssd', 'mobilenet_yolov2',
                  'mobilenetv2_yolov3', 'yolov4_tiny', 'yolov5s', 'yolov8s'],
    'face-detection': ['retinaface'],
}


def validate_task(model, task):
    if task == 'feedforward':
        return
    elif model in TASK_MAP[task]:
        return
    else:
        log.info(f'The model {model} is not supported for task {task}')
        raise ValueError('The task is wrong for this model')


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


def load_model(args):
    use_gpu = get_device(args.device, args.task)
    net = get_model(args.model, num_threads=args.num_threads, use_gpu=use_gpu)
    return net


def get_images_names(images_path):
    images_path = os.path.abspath(images_path[0])
    images_path_list = [os.path.join(images_path, file) for file in os.listdir(images_path)]
    return images_path_list


def prepare_output(results, task, model_wrapper):
    if results is None:
        return None
    if task == 'feedforward':
        return {}
    if task == 'classification':
        return {'classification': np.array(results)}
    if task == 'detection':
        box_ids, scores, bboxes, detected_obj = [], [], [], []
        for result in results:
            detected_obj.append(len(result))
            for obj in result:
                box_ids.append(obj.label)
                scores.append(obj.prob)
                bboxes.extend([obj.rect.x,
                               obj.rect.y,
                               obj.rect.x + obj.rect.w,
                               obj.rect.y + obj.rect.h])
        box_ids = np.expand_dims(box_ids, axis=1)
        scores = np.expand_dims(scores, axis=1)
        bboxes = np.array(bboxes).reshape(-1, 4)

        tmp = np.concatenate([box_ids, scores, bboxes], axis=1)
        num_of_images = np.zeros((tmp.shape[0], 1))
        start = 0
        for i in range(len(detected_obj)):
            end = start + detected_obj[i]
            num_of_images[start:end] = i
            start = end

        tmp = np.concatenate([num_of_images, tmp], axis=1)
        tmp = np.expand_dims(tmp, axis=0)
        tmp = np.expand_dims(tmp, axis=0)
        input_shape = model_wrapper.get_input_layer_shape(model=None, layer_name=None)
        tmp[:, :, :, 3] /= input_shape[2]
        tmp[:, :, :, 4] /= input_shape[1]
        tmp[:, :, :, 5] /= input_shape[2]
        tmp[:, :, :, 6] /= input_shape[1]
        return {'detection': tmp}
    if task == 'face-detection':
        result = {
            'labels': [],
            'boxes': [],
        }
        for i, face in enumerate(results[0]):
            result['labels'].append(i)
            result['boxes'].append([face.rect.x,
                                    face.rect.y,
                                    face.rect.x + face.rect.w,
                                    face.rect.y + face.rect.h,
                                    face.prob])
        result['labels'].append(-1)
        return result
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')
