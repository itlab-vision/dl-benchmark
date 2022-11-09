import numpy as np


class Transformer:
    @staticmethod
    def _transform(image):
        return image

    @staticmethod
    def get_shape_in_chw_order(shape):
        return shape[1:]

    def transform_images(self, images, shape, element_type):
        b = shape[0]
        transformed_images = np.zeros(shape=shape, dtype=element_type)
        for i in range(b):
            transformed_images[i] = self._transform(images[i])
        return transformed_images


class OpenVINOTransformer(Transformer):
    def _transform(self, image, shape):
        if self.__is_nhwc(shape):
            return image
        return image.transpose(2, 0, 1)

    def __is_nhwc(self, shape):
        return (len(shape) in [3, 4]) and (shape[len(shape) - 1] in [1, 3])

    def get_shape_in_chw_order(self, shape):
        if self.__is_nhwc(shape):
            return shape[3], shape[1], shape[2]
        return shape[1], shape[2], shape[3]

    def transform_images(self, images, shape, element_type):
        b = shape[0]
        transformed_images = np.zeros(shape=shape, dtype=element_type)
        image_index = 0
        for i in range(b):
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
            image[0] -= self._converting['mean'][0]
            image[1] -= self._converting['mean'][1]
            image[2] -= self._converting['mean'][2]

    def __set_input_scale(self, image):
        if 'input_scale' in self._converting:
            image[0] *= self._converting['input_scale']
            image[1] *= self._converting['input_scale']
            image[2] *= self._converting['input_scale']

    def _transform(self, image):
        transformed_image = np.copy(image)
        transformed_image = transformed_image.transpose(1, 2, 0)
        self.__set_channel_swap(transformed_image)
        self.__set_mean(transformed_image)
        self.__set_input_scale(transformed_image)
        return transformed_image


class TensorFlowTransformer(Transformer):
    def __init__(self, converting):
        self._converting = converting

    def get_shape_in_chw_order(self, shape):
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
            image[:, :, 0] /= self._converting['input_scale']
            image[:, :, 1] /= self._converting['input_scale']
            image[:, :, 2] /= self._converting['input_scale']

    def _transform(self, image):
        transformed_image = np.copy(image).astype(np.float64)
        self.__set_channel_swap(transformed_image)
        self.__set_mean(transformed_image)
        self.__set_input_scale(transformed_image)
        return transformed_image

    def transform_images(self, images, shape, element_type):
        b = shape[0]
        transformed_images = np.zeros(shape=shape, dtype=element_type)
        for i in range(b):
            transformed_images[i] = self._transform(images[i])
        return transformed_images
