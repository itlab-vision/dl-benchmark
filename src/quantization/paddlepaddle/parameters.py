import sys
import math
import random
import numpy as np
import paddle
from pathlib import Path
from PIL import Image, ImageEnhance
from paddle.io import Dataset
import ast
from paddle.io import DataLoader
from paddleslim.quant import quant_post_static
sys.path.append(str(Path(__file__).resolve().parents[3]))
from src.quantization.utils import ArgumentsParser


random.seed(0)
np.random.seed(0)

default_crop_scale = (0.08, 1.0)
default_crop_ratio = (3. / 4., 4. / 3.)


def resize_short(img, target_size):
    percent = float(target_size) / min(img.size[0], img.size[1])
    resized_width = int(round(img.size[0] * percent))
    resized_height = int(round(img.size[1] * percent))
    img = img.resize((resized_width, resized_height), Image.LANCZOS)
    return img


def crop_image(img, target_size, center):
    width, height = img.size
    size = target_size
    if center:
        w_start = (width - size) // 2
        h_start = (height - size) // 2
    else:
        w_start = np.random.randint(0, width - size + 1)
        h_start = np.random.randint(0, height - size + 1)
    w_end = w_start + size
    h_end = h_start + size
    img = img.crop((w_start, h_start, w_end, h_end))
    return img


def random_crop(img, size, scale=default_crop_scale, ratio=default_crop_ratio):
    aspect_ratio = math.sqrt(np.random.uniform(*ratio))
    w = 1. * aspect_ratio
    h = 1. / aspect_ratio

    bound = min((float(img.size[0]) / img.size[1]) / (w**2),
                (float(img.size[1]) / img.size[0]) / (h**2))
    scale_max = min(scale[1], bound)
    scale_min = min(scale[0], bound)

    target_area = img.size[0] * img.size[1] * np.random.uniform(scale_min,
                                                                scale_max)
    target_size = math.sqrt(target_area)
    w = int(target_size * w)
    h = int(target_size * h)

    i = np.random.randint(0, img.size[0] - w + 1)
    j = np.random.randint(0, img.size[1] - h + 1)

    img = img.crop((i, j, i + w, j + h))
    img = img.resize((size, size), Image.LANCZOS)
    return img


def rotate_image(img):
    angle = np.random.randint(-10, 11)
    img = img.rotate(angle)
    return img


def distort_color(img):
    def random_brightness(img, lower=0.5, upper=1.5):
        e = np.random.uniform(lower, upper)
        return ImageEnhance.Brightness(img).enhance(e)

    def random_contrast(img, lower=0.5, upper=1.5):
        e = np.random.uniform(lower, upper)
        return ImageEnhance.Contrast(img).enhance(e)

    def random_color(img, lower=0.5, upper=1.5):
        e = np.random.uniform(lower, upper)
        return ImageEnhance.Color(img).enhance(e)

    ops = [random_brightness, random_contrast, random_color]
    np.random.shuffle(ops)

    img = ops[0](img)
    img = ops[1](img)
    img = ops[2](img)

    return img


def process_image(sample,
                  mode,
                  color_jitter,
                  rotate,
                  crop_size,
                  resize_size,
                  img_mean, img_std):
    img_path = sample[0]

    try:
        img = Image.open(img_path)
    except Exception:
        print(img_path, 'does not exist!')
        return None
    if mode == 'train':
        if rotate:
            img = rotate_image(img)
        img = random_crop(img, crop_size)
    else:
        img = resize_short(img, target_size=resize_size)
        img = crop_image(img, target_size=crop_size, center=True)
    if mode == 'train':
        if color_jitter:
            img = distort_color(img)
        if np.random.randint(0, 2) == 1:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img = np.array(img).astype('float32').transpose((2, 0, 1)) / 255
    img -= img_mean
    img /= img_std

    if mode == 'train' or mode == 'val':
        return img, sample[1]
    elif mode == 'test':
        return [img]


class PaddleDatasetReader(Dataset):
    def __init__(self, args, mode='train'):
        super(PaddleDatasetReader, self).__init__()
        self.data_dir = args['Path']
        self.crop_size = ast.literal_eval(args['ResizeResolution'])
        self.resize_size = ast.literal_eval(args['ImageResolution'])
        self.mean = (np.asarray(ast.literal_eval(args['Mean']), dtype=np.float32)
                     if args['Mean'] is not None else [0., 0., 0.])

        self.std = (np.asarray(ast.literal_eval(args['Std']), dtype=np.float32)
                    if args['Std'] is not None else [1., 1., 1.])
        self.mode = mode
        self.batch_size = int(args['BatchSize'])
        self.dataset = list(Path(self.data_dir).glob('*'))
        random.shuffle(self.dataset)
        self.dataset_iter = iter(self.dataset)

    def __getitem__(self, index):
        sample = str(self.dataset[index].absolute())
        if self.mode == 'train':
            data, label = process_image(
                [sample, sample],
                mode='train',
                color_jitter=False,
                rotate=False,
                crop_size=self.crop_size,
                resize_size=self.resize_size,
                img_mean=self.mean,
                img_std=self.std)
            return data, np.array([label]).astype('int64')
        elif self.mode == 'val':
            data, label = process_image(
                [sample, sample],
                mode='val',
                color_jitter=False,
                rotate=False,
                crop_size=self.crop_size,
                resize_size=self.resize_size,
                img_mean=self.mean,
                img_std=self.std)
            return data, np.array([label]).astype('int64')
        elif self.mode == 'test':
            data = process_image(
                [sample, sample],
                mode='test',
                color_jitter=False,
                rotate=False,
                crop_size=self.crop_size,
                resize_size=self.resize_size,
                img_mean=self.mean,
                img_std=self.std)
            return data

    def __len__(self):
        return len(self.dataset)


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
            batch_nums=10,
            algo='avg',
            round_type='round',
            hist_percent=0.9999,
            is_full_quantize=False,
            bias_correction=False,
            onnx_format=False)


class PaddleModelReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self._log.info('Parsing model arguments.')
        self.path_prefix = self.args['PathPrefix']
        self.model_dir = self.args['ModelDir']
        self.model_filename = self.args['ModelFileName']
        self.params_filename = self.args['ParamsFileName']

    def dict_for_iter_log(self):
        return {
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
        }

    def _get_arguments(self):
        self.image_shape = ast.literal_eval(self.args['InputShape'])
        self.image = paddle.static.data(name=self.args['InputName'], shape=[None] + self.image_shape, dtype='float32')
        self.input_shape = self.args['InputShape']
        self.input_name = self.args['InputName']
        self.save_dir = self.args['SaveDir']

    def _convert_to_list_of_tf_objects(self, keys, dictionary):
        return [dictionary[key] for key in keys]
