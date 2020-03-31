import numpy as np

class transformer:
    def transform(self, image):
        return image


class intelcaffe_transformer(transformer):
    def __init__(self, converting):
        self._converting = converting


    def transform(self, image):
        img = image.astype(np.float32, copy = False)
        if 'channel_swap' in self._converting:
            img = img[self._converting['channel_swap'], :, :]
        if 'raw_scale' in self._converting:
            img *= self._converting['raw_scale']
        if 'mean' in self._converting:
            img[0] -= self._converting['mean'][0]
            img[1] -= self._converting['mean'][1]
            img[2] -= self._converting['mean'][2]
        return img        
