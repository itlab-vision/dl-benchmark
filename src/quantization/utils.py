import re
import abc
import ast
import sys
import numpy as np
import importlib
import random
from pathlib import Path
from xml.etree import ElementTree as ET


def iter_log(model_reader, data_reader, quant_params, log):
    log_string = 'Quantization config:\n\n\t'
    log_string += 'Model:'
    for name in model_reader:
        log_string += f'\n\t\t{name}: {model_reader[name]}'
    log_string += '\n\tDataset'
    for name in data_reader:
        log_string += f'\n\t\t{name}: {data_reader[name]}'
    log_string += '\n\tQuantization parameters:'
    for name in quant_params:
        log_string += f'\n\t\t{name}: {quant_params[name]}'
    log.info(log_string)


class ArgumentsParser(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self._log = log

    def add_arguments(self, args):
        self.args = args
        self._get_arguments()

    @abc.abstractmethod
    def _get_arguments(self):
        pass

    @abc.abstractmethod
    def dict_for_iter_log(self):
        pass


class DatasetReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)
        self.cv2 = importlib.import_module('cv2')

    def dict_for_iter_log(self):
        return {
            'Name': self.dataset_name,
            'Path to folder': self.dataset_path,
            'Number of images': self.max,
        }

    def _get_arguments(self):
        self._log.info('Parsing dataset arguments.')
        self.dataset_name = self.args['Name']
        self.dataset_path = self.args['Path']

        self.channel_swap = (np.asarray(ast.literal_eval(self.args['ChannelSwap']), dtype=np.float32)
                             if self.args['ChannelSwap'] is not None else [2, 1, 0])

        self.norm = (ast.literal_eval(self.args['Normalization'])
                     if self.args['Normalization'] is not None else False)

        self.layout = self.args['Layout']

        self.mean = (np.asarray(ast.literal_eval(self.args['Mean']), dtype=np.float32)
                     if self.args['Mean'] is not None else [0., 0., 0.])

        self.std = (np.asarray(ast.literal_eval(self.args['Std']), dtype=np.float32)
                    if self.args['Std'] is not None else [1., 1., 1.])

        self.image_size = ast.literal_eval(self.args['ImageResolution'])

        self.dataset = list(Path(self.dataset_path).glob('*'))
        random.shuffle(self.dataset)
        self.dataset_iter = iter(self.dataset)
        self.batch = int(self.args['BatchSize'])
        self.max = len(self.dataset)

        sys.path.append(str(Path(__file__).resolve().parents[2]))
        from src.inference.transformer import TVMTransformer
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
        image = self.cv2.imread(image_path)
        image_resize = self.cv2.resize(image, self.image_size)
        return image_resize

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.max:
            res = []
            for _ in range(self.batch):
                self.n += 1
                image = self._preprocess_image(str(next(self.dataset_iter).absolute()))
                res.append(image)
            res = np.array(res)
            result = self.transformer.transform_images(res, None, np.float32, 'data')
            return result
        else:
            raise StopIteration


class ConfigParser:
    def __init__(self, config_path):
        self.config_path = config_path

    def _parse_xml(self):
        return ET.parse(self.config_path).getroot()

    def _create_list_from_xml_nodes(self, nodes):
        ls = []
        for i, node in enumerate(nodes):
            ls.append({node.tag: {}})
            for subnode in node:
                ls[i][node.tag][subnode.tag] = subnode.text
        return ls

    def parse(self):
        res = []
        xml = self._parse_xml()
        for config in xml:
            model = config.find('Model')
            dataset = config.find('Dataset')
            quantparam = config.find('QuantizationParameters')
            res.append(self._create_list_from_xml_nodes([model, dataset, quantparam]))
        return res


def get_param_from_data(data, tag):
    if data is not None:
        return data.get(tag)
    else:
        return None


def get_correct_path(path):
    if path is not None and ' ' in path and '"' not in path:
        path = '"' + path + '"'
    return path


def camel_to_snake(string):
    groups = re.findall('([A-z][a-z0-9]*)', string)
    return '_'.join([i.lower() for i in groups])


def get_typed_from_str(text):
    if text == 'False':
        return False
    if text == 'True':
        return True
    if text.isdigit():
        return int(text)
    if is_number(text):
        return float(text)
    return text or ''


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
