import numpy as np
import mxnet
import gluoncv
import logging as log
import os
import warnings


def prepare_output(result, output_names, task, model_wrapper):
    if task == 'feedforward':
        return {}
    if (output_names is None) or len(output_names) == 0:
        raise ValueError('The number of output tensors does not match the number of corresponding output names')
    if task == 'classification':
        return {output_names[0]: (result.softmax()).asnumpy()}
    if task == 'detection':
        box_ids, scores, bboxes = result
        box_ids = (box_ids.asnumpy())[0]
        scores = (scores.asnumpy())[0]
        bboxes = (bboxes.asnumpy())[0]

        if 'center_net' in model_wrapper.get_model_name():
            box_ids = np.expand_dims(box_ids, axis=1)
            scores = np.expand_dims(scores, axis=1)

        tmp = np.concatenate([box_ids, scores, bboxes], axis=1)
        num_of_images = np.zeros((tmp.shape[0], 1))
        tmp = np.concatenate([num_of_images, tmp], axis=1)
        tmp = np.expand_dims(tmp, axis=0)
        tmp = np.expand_dims(tmp, axis=0)
        input_shape = model_wrapper.get_input_layer_shape(model=None, layer_name=None)
        tmp[:, :, :, 3] /= input_shape[2]
        tmp[:, :, :, 4] /= input_shape[3]
        tmp[:, :, :, 5] /= input_shape[2]
        tmp[:, :, :, 6] /= input_shape[3]
        return {output_names[0]: tmp}
    if task == 'segmentation':
        result = mxnet.nd.squeeze(mxnet.nd.argmax(result[0], 1)).asnumpy()
        result = np.expand_dims(result, axis=0)
        return {output_names[0]: result}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def get_device(device, task):
    log.info(f'Get device for {task}')
    if device == 'CPU':
        log.info(f'{task.title()} will be executed on {device}')
        return mxnet.cpu()
    elif device == 'NVIDIA_GPU':
        log.info(f'{task.title()} will be executed on {device}')
        return mxnet.gpu()
    else:
        log.info(f'The device {device} is not supported')
        raise ValueError('The device is not supported')


def load_network_gluon(model_json, model_params, context, input_name):
    log.info(f'Deserializing network from file ({model_json}, {model_params})')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        deserialized_net = mxnet.gluon.nn.SymbolBlock.imports(
            model_json, [input_name], model_params, ctx=context)
    return deserialized_net


def load_network_gluon_model_zoo(model_name, hybrid, context, save_model,
                                 path_save_model, task='inference'):

    log.info(f'Loading network \"{model_name}\" from GluonCV model zoo')
    net = gluoncv.model_zoo.get_model(model_name, pretrained=True, ctx=context)

    if save_model is True:
        log.info(f'Saving model \"{model_name}\" to \"{path_save_model}\"')
        if path_save_model is None:
            path_save_model = os.getcwd()
        path_save_model = os.path.join(path_save_model, model_name)
        if not os.path.exists(path_save_model):
            os.mkdir(path_save_model)
        gluoncv.utils.export_block(os.path.join(path_save_model, model_name), net,
                                   preprocess=None, layout='CHW', ctx=context)

    if task == 'inference':
        log.info(f'Info about the network:\n{net}')

        log.info(f'Hybridizing model to accelerate inference: {hybrid}')
        if hybrid is True:
            net.hybridize()
    return net


def create_dict_for_transformer(args):
    dictionary = {
        'channel_swap': args.channel_swap,
        'mean': args.mean,
        'std': args.std,
        'norm': args.norm,
        'input_shape': args.input_shape,
        'batch_size': args.batch_size,
    }
    return dictionary


def create_dict_for_quantwrapper(args):
    dictionary = {
        'calib_mode': args.calib_mode,
        'quant_dtype': args.quant_dtype,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_json': args.model_json,
        'model_params': args.model_params,
        'input_name': args.input_name,
        'quant_mode': args.quant_mode,
    }
    return dictionary


def create_dict_for_modelwrapper(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
    }
    return dictionary
