import os
import cv2 as cv
import numpy as np
from addict import Dict
from compression.api.data_loader import DataLoader


class DatasetsDataLoader(DataLoader):
    def __init__(self, config):
        if not isinstance(config, Dict):
            config = Dict(config)
        super().__init__(config)

        with open(config['annotation_file'], 'rt') as f:
             dataset = f.read().strip().split('\n') 

        self.preprocessing_config = Dict(config['preprocessing'])
        self.images = []
        self.annotations = []

        for data in dataset:
            img_path, label = data.rsplit(' ')
            label = int(label) + 1

            img_path = os.path.join(config['data_source'], img_path)

            self.images.append(img_path)
            self.annotations.append(label)

        self.images = self.images[:config['set_size']]


    def __len__(self):
        return len(self.images)


    def __getitem__(self, item):
        img = cv.imread(self.images[item])

        image_means = self.preprocessing_config['means']
        image_size_h = self.preprocessing_config['image_resize']['height']
        image_size_w = self.preprocessing_config['image_resize']['width']

        img = cv.resize(img, (image_size_h, image_size_w))
        img = np.expand_dims(img, axis=0)
        img = (img - image_means)
        img = img.astype(np.float32)
        img = img.transpose((0, 3, 1, 2))

        return (item, self.annotations[item]), img
