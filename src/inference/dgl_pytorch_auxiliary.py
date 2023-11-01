from inference_tools.loop_tools import get_exec_time
import logging as log
import torch


@get_exec_time()
def infer_slice(device, inputs, model, input_kwarg_name=None, task_type=None):
    if task_type in ['text-translation']:
        infer_func = model.translate_batch
    else:
        infer_func = model

    if input_kwarg_name:
        infer_func(**{input_kwarg_name: inputs})
    else:
        infer_func(*inputs)

    if device.type == 'cuda':
        torch.cuda.synchronize()


def get_device_to_infer(device):
    log.info('Get device for inference')
    if device == 'CPU':
        log.info(f'Inference will be executed on {device}')

        return torch.device('cpu')
    elif device == 'NVIDIA_GPU':
        log.info(f'Inference will be executed on {device}')

        return torch.device('cuda')
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')
