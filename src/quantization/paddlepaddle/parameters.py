import sys
from pathlib import Path
import random
import numpy as np
import paddle
from paddle.io import Dataset
import ast
from paddle.io import DataLoader
from paddleslim.quant import quant_post_static
import cv2
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import ArgumentsParser  # noqa: E402


class PaddleDatasetReader(Dataset):
    def __init__(self, args, log):
        super(PaddleDatasetReader, self).__init__()
        self.log = log
        self.log.info('Parsing dataset arguments.')
        self.data_dir = args['Path']

        self.resize_size = ast.literal_eval(args['ResizeResolution'])
        self.mean = np.array((np.asarray(ast.literal_eval(args['Mean']), dtype=np.float32)
                              if args['Mean'] is not None else [0., 0., 0.])).reshape((3, 1, 1))
        self.std = np.array((np.asarray(ast.literal_eval(args['Std']), dtype=np.float32)
                             if args['Std'] is not None else [1., 1., 1.])).reshape((3, 1, 1))
        self.channel_swap = ast.literal_eval(args['ChannelSwap']) if args['ChannelSwap'] is not None else [2, 0, 1]
        self.batch_size = int(args['BatchSize'])
        self.batch_num = int(args['BatchNum'])
        self.dataset = list(Path(self.data_dir).glob('*.JPEG'))
        random.shuffle(self.dataset)
        self.dataset_iter = iter(self.dataset)

    def __getitem__(self, index):
        image_path = str(self.dataset[index].absolute())
        data = self.process_image(image_path)
        return data

    def __len__(self):
        return len(self.dataset)

    def process_image(self, image_path):

        img = cv2.imread(image_path)
        if img.size == 0:
            self.log.info('failed to read:', image_path)
            return None
        img = cv2.resize(img, self.resize_size)

        img = img.astype('float32').transpose(tuple(self.channel_swap)) / 255
        img -= self.mean
        img /= self.std

        return img


class PaddleQuantizationProcess:
    def __init__(self, log, model_reader, dataset, quant_params):
        self.log = log
        self.model_reader = model_reader
        self.dataset = dataset
        self.quant_params = quant_params

    def transform_fn(self):
        for data in self.dataset:
            yield [data.astype(np.float32)]

    def quantization_paddle(self):
        place = paddle.CPUPlace()
        exe = paddle.static.Executor(place)
        data_loader = DataLoader(
            self.dataset,
            places=place,
            feed_list=[self.quant_params.image],
            drop_last=False,
            return_list=False,
            batch_size=self.dataset.batch_size,
            shuffle=False)

        quant_post_static(
            executor=exe,
            model_dir=self.model_reader.model_dir,
            quantize_model_path=self.quant_params.save_dir,
            data_loader=data_loader,
            model_filename=self.model_reader.model_filename,
            params_filename=self.model_reader.params_filename,
            batch_size=self.dataset.batch_size,
            batch_nums=self.dataset.batch_num,
            algo=self.quant_params.algo,
            round_type='round',
            hist_percent=0.9999,
            is_full_quantize=True,
            bias_correction=False,
            onnx_format=False)


class PaddleModelReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self._log.info('Parsing model arguments.')
        self.model_name = self.args['Name']
        self.path_prefix = self.args['PathPrefix']
        self.model_dir = self.args['ModelDir']
        self.model_filename = self.args['ModelFileName']
        self.params_filename = self.args['ParamsFileName']

    def dict_for_iter_log(self):
        return {
            'Name': self.model_name,
            'Model path prefix': self.path_prefix,
        }


class PaddleQuantParamReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def dict_for_iter_log(self):
        return {
            'InputShape': self.input_shape,
            'InputName': self.input_name,
            'SaveDir': self.save_dir,
            'Algorithm': self.algo,
        }

    def _get_arguments(self):
        self.input_shape = ast.literal_eval(self.args['InputShape'])
        self.image = paddle.static.data(name=self.args['InputName'], shape=[None] + self.input_shape, dtype='float32')
        self.input_name = self.args['InputName']
        self.save_dir = self.args['SaveDir']
        self.algo = self.args['Algorithm']
