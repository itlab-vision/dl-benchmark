import numpy as np
import mxnet

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