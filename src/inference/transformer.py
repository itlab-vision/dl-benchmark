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
    

    def __set_raw_scale(self, image):
        if 'raw_scale' in self._converting:
            image[0] *= self._converting['raw_scale']
            image[1] *= self._converting['raw_scale']
            image[2] *= self._converting['raw_scale']

    
    def __set_mean(self, image):
        if 'mean' in self._converting:
            image[0] -= self._converting['mean'][0]
            image[1] -= self._converting['mean'][1]
            image[2] -= self._converting['mean'][2]


    def transform(self, image):
        image = image.astype(np.float32, copy=False)
        self.__set_channel_swap(image)
        self.__set_mean(image)
        self.__set_raw_scale(image)
        return image        
