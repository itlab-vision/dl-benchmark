import sys
import importlib
from pathlib import Path
from time import time
from inference_tools.loop_tools import loop_inference, get_exec_time

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


class OutputPreparer:
    def __init__(self, framework):
        self.framework = framework

    def classification_task(self, result, output_names, not_softmax):
        if not_softmax:
            result = result[0].asnumpy()
        else:
            from scipy.special import softmax
            result = result[0].asnumpy()
            for i in range(result.shape[0]):
                result[i] = softmax(result[i])
        return {output_names[0]: result}

    def detection_task(self, result, output_names, params):
        np = importlib.import_module('numpy')
        if self.framework == 'mxnet':
            box_ids, scores, bboxes = result
            box_ids = (box_ids.asnumpy())[0]
            scores = (scores.asnumpy())[0]
            bboxes = (bboxes.asnumpy())[0]

            if 'center_net' in params['model_name']:
                box_ids = np.expand_dims(box_ids, axis=1)
                scores = np.expand_dims(scores, axis=1)

            tmp = np.concatenate([box_ids, scores, bboxes], axis=1)
            num_of_images = np.zeros((tmp.shape[0], 1))
            tmp = np.concatenate([num_of_images, tmp], axis=1)
            tmp = np.expand_dims(tmp, axis=0)
            tmp = np.expand_dims(tmp, axis=0)
            input_shape = params['input_shape']
            tmp[:, :, :, 3] /= input_shape[2]
            tmp[:, :, :, 4] /= input_shape[3]
            tmp[:, :, :, 5] /= input_shape[2]
            tmp[:, :, :, 6] /= input_shape[3]
            return {output_names[0]: tmp}


def create_dict_for_converter_mxnet(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'device': args.device,
        'opt_level': args.opt_level,
        'target': args.target,
    }
    return dictionary


def create_dict_for_converter_tvm(args):
    return create_dict_for_converter_mxnet(args)


def create_dict_for_converter_pytorch(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'device': args.device,
        'opt_level': args.opt_level,
        'module': args.module,
        'target': args.target,
    }
    return dictionary


def create_dict_for_converter_onnx(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'device': args.device,
        'opt_level': args.opt_level,
        'target': args.target,
    }
    return dictionary


def create_dict_for_transformer(args):
    dictionary = {
        'channel_swap': args.channel_swap,
        'mean': args.mean,
        'std': args.std,
        'norm': args.norm,
        'input_shape': args.input_shape,
        'batch_size': args.batch_size,
        'layout': args.layout,
    }
    return dictionary


def create_dict_for_converter_tensorflowlite(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'device': args.device,
        'opt_level': args.opt_level,
        'output_names': args.output_names,
        'target': args.target,
    }
    return dictionary


def create_dict_for_modelwrapper(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
    }
    return dictionary


def create_dict_for_output_preparer(args):
    dictionary = {
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
    }
    return dictionary


def inference_tvm(module, num_of_iterations, input_name, get_slice, test_duration):
    result = None
    time_infer = []
    num_of_outputs = module.get_num_outputs()
    if num_of_iterations == 1:
        slice_input = get_slice()
        t0 = time()
        module.set_input(input_name, slice_input[input_name])
        module.run()
        result = [module.get_output(i) for i in range(num_of_outputs)]
        t1 = time()
        time_infer.append(t1 - t0)
    else:
        time_infer, _ = loop_inference(num_of_iterations, test_duration)(inference_iteration)(get_slice,
                                                                                              input_name,
                                                                                              module)
    return result, time_infer


def inference_iteration(get_slice, input_name, module):
    slice_input = get_slice()
    _, exec_time = infer_slice(input_name, module, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(input_name, module, slice_input):
    num_of_outputs = module.get_num_outputs()
    module.set_input(input_name, slice_input[input_name])
    module.run()
    res = [module.get_output(i) for i in range(num_of_outputs)]
    return res


def prepare_output(result, task, output_names, not_softmax=False, framework='tvm', params=None):
    preparer = OutputPreparer(framework)
    if task == 'feedforward':
        return {}
    if task == 'classification':
        return preparer.classification_task(result, output_names, not_softmax)
    if task == 'detection':
        return preparer.detection_task(result, output_names, params)
