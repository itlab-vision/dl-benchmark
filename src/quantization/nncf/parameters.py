import abc
import ast
import os
import nncf
import sys
import cv2
import numpy as np
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from inference.transformer import TVMTransformer  # noqa: E402


class TVMReader(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self._log = log

    def add_arguments(self, args):
        self.args = args
        self._get_arguments()

    @abc.abstractmethod
    def _get_arguments(self):
        pass


class NNCFDatasetReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self.dataset_name = self.args['DatasetName']
        self.dataset_path = self.args['DatasetPath']

        self.channel_swap = (np.asarray(ast.literal_eval(self.args['ChannelSwap']), dtype=np.float32)
                             if self.args['ChannelSwap'] is not None else [2, 1, 0])

        self.norm = (ast.literal_eval(self.args['Normalization'])
                     if self.args['Normalization'] is not None else False)

        self.layout = self.args['Layout']

        self.mean = (np.asarray(ast.literal_eval(self.args['Mean']), dtype=np.float32)
                     if self.args['Mean'] is not None else [0., 0., 0.])

        self.std = (np.asarray(ast.literal_eval(self.args['Std']), dtype=np.float32)
                    if self.args['Std'] is not None else [1., 1., 1.])

        self.image_size = ast.literal_eval(self.args['ImageSize'])
        self.dataset = list(Path(self.dataset_path).glob('*'))
        self.batch = int(self.args['BatchSize'])
        self.gg = Path(self.dataset_path).glob('*')
        self.max = len(self.dataset)
        self.transformer = TVMTransformer(self.dict_for_transformer())

    def dict_for_transformer(self):
        dictionary = {
            'channel_swap': self.channel_swap,
            'mean': self.mean,
            'std': self.std,
            'norm': self.norm,
            'layout': self.layout,
        }
        return dictionary

    def _preprocess_image(self, image_path):
        image = cv2.imread(image_path)
        image_resize = cv2.resize(image, self.image_size)
        return image_resize

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.max:
            res = []
            for _ in range(self.batch):
                self.n += 1
                image = self._preprocess_image(str(next(self.gg).absolute()))
                res.append(image)
            res = np.array(res)
            result = self.transformer.transform_images(res, None, np.float32, 'data')
            return result
        else:
            raise StopIteration


class NNCFQuantParamReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self.model_type = self.args['ModelType']
        self.preset = self.args['Preset']
        self.subset_size = ast.literal_eval(self.args['SubsetSize'])
        self.output_dir = self.args['OutputDirectory']


class NNCFQuantizationProcess:
    def __init__(self, log, model_reader, dataset, quant_params):
        self.log = log
        self.quant_model = None
        self.model_reader = model_reader
        self.dataset = dataset
        self.quant_params = quant_params
    
    def transform_fn(self, data_item):
        images = data_item
        return {self.model_reader.model.graph.input[0].name: images}


    def quantization_nncf(self):
        calibration_dataset = nncf.Dataset(self.dataset, transform_func=self.transform_fn)
        self.quant_model = nncf.quantize(model=self.model_reader.model, calibration_dataset=calibration_dataset)
        print(self.quant_model)
