import numpy as np


class transformer:
    def transform(self, image):
        return image


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


    def transform(self, image):
        transformed_image = np.copy(image)
        self.__set_channel_swap(transformed_image)
        self.__set_mean(transformed_image)
        self.__set_input_scale(transformed_image)
        return transformed_image         
