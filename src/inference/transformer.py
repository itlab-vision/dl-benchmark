import numpy as np


class transformer:
    def _transform(self, image):
        return image

    def get_shape_in_chw_order(self, shape):
        return shape[1:]

    def transform_images(self, images):
        b, c, h, w = images.shape
        transformed_images = np.zeros(shape=(b, c, h, w))
        for i in range(b):
            transformed_images[i] = self._transform(images[i])
        return transformed_images


class intelcaffe_transformer(transformer):
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
        self.__set_channel_swap(transformed_image)
        self.__set_mean(transformed_image)
        self.__set_input_scale(transformed_image)
        return transformed_image


class tensorflow_transformer(transformer):
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

    def transform_images(self, images):
        images = images.transpose(0, 2, 3, 1)
        b, h, w, c = images.shape
        transformed_images = np.zeros(shape=(b, h, w, c))
        for i in range(b):
            transformed_images[i] = self._transform(images[i])
        return transformed_images
