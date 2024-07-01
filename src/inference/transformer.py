import cv2
import numpy as np

LAYER_LAYOUT_TO_IMAGE = {
    'NCHW': [0, 3, 1, 2],
    'NHWC': [0, 1, 2, 3],
    'NCWH': [0, 3, 2, 1],
    'NWCH': [0, 2, 3, 1],
    'NWHC': [0, 2, 1, 3],
    'NCDHW': [0, 4, 1, 2, 3],
    'NDCHW': [0, 1, 4, 2, 3],
    'NDHWC': [0, 1, 2, 3, 4],
    'NDCWH': [0, 1, 4, 3, 2],
    'NCHWD': [0, 2, 3, 4, 1],
    'NHWDC': [0, 2, 3, 1, 4],
    'NHWCD': [0, 2, 3, 4, 1],
    'NC': [0, 1],
    'NCH': [0, 1, 2],
}


class Transformer:
    @staticmethod
    def _transform(image):
        return image

    @staticmethod
    def get_shape_in_chw_order(shape, *args):
        return shape[1:]

    def transform_images(self, images, shape, element_type, *args):
        dataset_size = images.shape[0]
        new_shape = [dataset_size] + shape[1:]
        transformed_images = np.zeros(shape=new_shape, dtype=element_type)
        for i in range(dataset_size):
            transformed_images[i] = self._transform(images[i])
        return transformed_images


class OpenVINOTransformer(Transformer):
    def _transform(self, image, shape):
        if self.__is_nhwc(shape):
            return image
        return image.transpose(2, 0, 1)

    def __is_nhwc(self, shape):
        return (len(shape) in [3, 4]) and (shape[len(shape) - 1] in [1, 3])

    def get_shape_in_chw_order(self, shape, *args):
        if self.__is_nhwc(shape):
            return shape[3], shape[1], shape[2]
        return shape[1], shape[2], shape[3]

    def transform_images(self, images, shape, element_type, *args):
        dataset_size = images.shape[0]
        new_shape = [dataset_size, shape[1], shape[2], shape[3]]
        transformed_images = np.zeros(shape=new_shape, dtype=element_type)
        image_index = 0
        for i in range(dataset_size):
            image_index %= images.shape[0]
            transformed_images[i] = self._transform(images[image_index], shape)
            image_index += 1
        return transformed_images


class IntelCaffeTransformer(Transformer):
    def __init__(self, converting):
        self._converting = converting

    def __set_channel_swap(self, image):
        if 'channel_swap' in self._converting:
            image = image[self._converting['channel_swap'], :, :]

    def __set_mean(self, image):
        if 'mean' in self._converting:
            image[:, :, 0] -= self._converting['mean'][0]
            image[:, :, 1] -= self._converting['mean'][1]
            image[:, :, 2] -= self._converting['mean'][2]

    def __set_input_scale(self, image):
        if 'input_scale' in self._converting:
            image[:, :, 0] /= self._converting['input_scale'][0]
            image[:, :, 1] /= self._converting['input_scale'][1]
            image[:, :, 2] /= self._converting['input_scale'][2]

    def _transform(self, image):
        transformed_image = np.copy(image).astype(np.float32)
        transformed_image = transformed_image.transpose(2, 0, 1)
        self.__set_channel_swap(transformed_image)
        self.__set_mean(transformed_image)
        self.__set_input_scale(transformed_image)
        return transformed_image

    def transform_images(self, images, shape, element_type, *args):
        dataset_size = images.shape[0]
        new_shape = [dataset_size] + list(shape[1:])
        transformed_images = np.zeros(shape=new_shape, dtype=element_type)
        for i in range(dataset_size):
            transformed_images[i] = self._transform(images[i])
        return transformed_images


class TensorFlowTransformer(Transformer):
    def __init__(self, converting: dict):
        self._converting = converting

    def get_shape_in_chw_order(self, shape, *args):
        h, w, c = shape[1:]
        return c, h, w

    def __set_channel_swap(self, image):
        if 'channel_swap' in self._converting:
            image = image[:, :, self._converting['channel_swap']]

    def __set_mean(self, image):
        if 'mean' in self._converting:
            image[:, :, 0] -= self._converting['mean'][0]
            image[:, :, 1] -= self._converting['mean'][1]
            image[:, :, 2] -= self._converting['mean'][2]

    def __set_input_scale(self, image):
        if 'input_scale' in self._converting:
            image[:, :, 0] /= self._converting['input_scale'][0]
            image[:, :, 1] /= self._converting['input_scale'][1]
            image[:, :, 2] /= self._converting['input_scale'][2]

    def _transform(self, image):
        transformed_image = np.copy(image).astype(np.float64)
        self.__set_channel_swap(transformed_image)
        self.__set_mean(transformed_image)
        self.__set_input_scale(transformed_image)
        return transformed_image

    def transform_images(self, images, shape, element_type, *args):
        dataset_size = images.shape[0]
        new_shape = [dataset_size] + shape[1:]
        transformed_images = np.zeros(shape=new_shape, dtype=element_type)
        for i in range(dataset_size):
            transformed_images[i] = self._transform(images[i])
        return transformed_images


class TensorFlowLiteTransformer(TensorFlowTransformer):
    def __init__(self, converting):
        self._converting = converting

    def get_shape_in_chw_order(self, shape, input_name):
        layout = self._converting[input_name]['layout']
        sort = np.argsort(LAYER_LAYOUT_TO_IMAGE[layout])
        shape = np.array(shape)[sort]
        chw = shape[1:]
        if len(shape) in [4, 5]:
            chw = shape[-1], shape[-3], shape[-2]
        return chw

    def __set_channel_swap(self, image, input_name):
        channel_swap = self._converting[input_name]['channel_swap']
        if channel_swap is not None:
            image = image[:, :, :, channel_swap]

    def __set_mean(self, image, input_name):
        mean = self._converting[input_name]['mean']
        if mean is not None:
            image -= mean

    def __set_input_scale(self, image, input_name):
        input_scale = self._converting[input_name]['input_scale']
        if input_scale is not None:
            image /= input_scale

    def __set_layout_order(self, image, input_name):
        layout = self._converting[input_name]['layout']
        if layout is not None:
            layout = LAYER_LAYOUT_TO_IMAGE[layout]
            image = image.transpose(layout)
        return image

    def _transform(self, image, input_name):
        transformed_image = np.copy(image).astype(np.float64)
        self.__set_channel_swap(transformed_image, input_name)
        self.__set_mean(transformed_image, input_name)
        self.__set_input_scale(transformed_image, input_name)
        transformed_image = self.__set_layout_order(transformed_image, input_name)
        return transformed_image

    def transform_images(self, images, shape, element_type, input_name):
        transformed_images = np.zeros(shape=shape)
        transformed_images = self._transform(images, input_name)
        return transformed_images.astype(element_type)


class MXNetTransformer(Transformer):
    def __init__(self, converting):
        self._converting = converting

    def __set_norm(self, image):
        import mxnet
        if self._converting['norm'] is True:
            mean = mxnet.nd.array([self._converting['mean'][0],
                                   self._converting['mean'][1],
                                   self._converting['mean'][2]])
            std = mxnet.nd.array([self._converting['std'][0],
                                  self._converting['std'][1],
                                  self._converting['std'][2]])
            normalized_image = mxnet.image.color_normalize(
                mxnet.nd.array(image).astype(np.float32) / 255, mean=mean, std=std)
            return normalized_image
        return image

    def __set_channel_swap(self, image):
        if self._converting['channel_swap'] is not None:
            transposing_form = (self._converting['channel_swap'][0],
                                self._converting['channel_swap'][1],
                                self._converting['channel_swap'][2])
            transposed_image = image.transpose(transposing_form)
            return transposed_image
        return image

    def _transform(self, image):
        normalized_image = self.__set_norm(image)
        transposed_image = self.__set_channel_swap(normalized_image)
        return transposed_image

    def transform_images(self, images, shape, element_type, *args):
        import mxnet

        dataset_size = images.shape[0]
        new_shape = [dataset_size] + shape[1:]
        transformed_images = mxnet.nd.zeros(shape=new_shape, dtype=element_type)
        for i in range(dataset_size):
            transformed_images[i] = self._transform(images[i])
        return transformed_images


class OpenCVTransformer(Transformer):
    def __init__(self, converting):
        self._converting = converting
        self._std = np.asarray(converting['std'], dtype=np.float32)
        self._std.shape = (1, 3, 1, 1)
        del self._converting['std']
        self._layout = self._converting['layout']
        del self._converting['layout']

    def get_shape_in_chw_order(self, shape, *args):
        h, w, c = shape[1:]
        return c, h, w

    def __set_layout_order(self, image):
        if self._layout is not None:
            self._layout = LAYER_LAYOUT_TO_IMAGE[self._layout]
            image = image.transpose(self._layout)
        return image

    def _transform(self, image):
        blob = cv2.dnn.blobFromImage(image, **self._converting)
        transformed_blob = self.__set_layout_order(blob / self._std)
        return transformed_blob

    def transform_images(self, images, shape, element_type, *args):
        blob = cv2.dnn.blobFromImages(images, **self._converting)
        transformed_blob = self.__set_layout_order(blob / self._std)
        return transformed_blob


class PyTorchTransformer(TensorFlowLiteTransformer):
    pass


class ONNXRuntimeTransformer(TensorFlowLiteTransformer):
    pass


class TVMTransformer(Transformer):
    def __init__(self, converting):
        self._converting = converting

    def get_shape_in_chw_order(self, shape, input_name):
        layout = self._converting['layout']
        sort = np.argsort(LAYER_LAYOUT_TO_IMAGE[layout])
        shape = np.array(shape)[sort]
        chw = shape[1:]
        if len(shape) in [4, 5]:
            chw = shape[-1], shape[-3], shape[-2]
        return chw

    def __set_channel_swap(self, image, input_name):
        channel_swap = self._converting['channel_swap']
        if channel_swap is not None:
            image = image[:, :, :, channel_swap]

    def __set_norm(self, image, input_name):
        image /= [np.float32(255), np.float32(255), np.float32(255)]

    def __set_mean(self, image, input_name):
        mean = self._converting['mean']
        if mean is not None:
            image -= mean

    def __set_input_scale(self, image, input_name):
        input_scale = self._converting['std']
        if input_scale is not None:
            image /= input_scale

    def __set_layout_order(self, image, input_name):
        layout = self._converting['layout']
        if layout is not None:
            layout = LAYER_LAYOUT_TO_IMAGE[layout]
            image = image.transpose(layout)
        return image

    def _transform(self, image, input_name):
        transformed_image = np.copy(image).astype(np.float64)
        self.__set_channel_swap(transformed_image, input_name)
        if self._converting['norm']:
            self.__set_norm(transformed_image, input_name)
        self.__set_mean(transformed_image, input_name)
        self.__set_input_scale(transformed_image, input_name)
        transformed_image = self.__set_layout_order(transformed_image, input_name)
        return transformed_image

    def transform_images(self, images, shape, element_type, input_name):
        transformed_images = self._transform(images, input_name)
        return transformed_images.astype(element_type)


class ONNXRuntimeTransformerCpp(Transformer):
    def __init__(self, model):
        self._model = model

    def get_shape_in_chw_order(self, shape, *args):
        return shape[1:]

    def transform_images(self, images, shape, element_type, *args):
        return images


class PyTorchTransformerCpp(Transformer):
    def __init__(self):
        pass

    def get_shape_in_chw_order(self, shape, *args):
        c, h, w = shape[1:]
        return c, h, w

    def transform_images(self, images, shape, element_type, *args):
        return images


class NcnnTransformer(Transformer):
    def _transform(self, image, shape):
        return image

    def get_shape_in_chw_order(self, shape, *args):
        return shape[3], shape[1], shape[2]

    def transform_images(self, images, shape, element_type, *args):
        dataset_size = images.shape[0]
        new_shape = [dataset_size, shape[1], shape[2], shape[3]]
        transformed_images = np.zeros(shape=new_shape, dtype=element_type)
        for i in range(dataset_size):
            transformed_images[i] = self._transform(images[i], shape)
        return transformed_images
