import tvm
import abc
import ast
import os
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


class TVMDatasetReader(TVMReader):
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


class TVMModelReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self.model_name = self.args['ModelName']
        self.model_path = self.args['ModelJson']
        self.model_params = self.args['WeightsParams']
        self._read_model()

    def _read_model(self):
        with open(self.model_params, 'rb') as fo:
            params = tvm.relay.load_param_dict(fo.read())

        with open(self.model_path, 'r') as fo:
            mod = fo.read()

        self.mod = tvm.ir.load_json(mod)
        self.params = params


class TVMQuantParamReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self.calib_mode = self.args['CalibMode']
        self.calib_samples = (int(self.args['CalibSamples'])
                              if self.args['CalibSamples'] is not None else None)
        self.weights_scale = self.args['WeightsScale']
        self.dtype_input = self.args['dtype_input']
        self.dtype_weight = self.args['dtype_weight']
        self.dtype_activation = self.args['dtype_activation']
        self.partition_conversions = self.args['partition_conversions']
        self.global_scale = (float(self.args['GlobalScale'])
                             if self.args['GlobalScale'] is not None else None)
        self.output_dir = self.args['OutputDirectory']


class TVMQuantizationProcess:
    def __init__(self, log, model, dataset, quant_params):
        self.log = log
        self.quant_model = None
        self.model = model
        self.dataset = dataset
        self.quant_params = quant_params

    def calibrate_dataset(self):
        for i, data in enumerate(self.dataset):
            if i * self.dataset.batch >= self.quant_params.calib_samples:
                break
            yield {'data': data}

    def quantization_tvm(self):
        self.log.info(f'Starting quantization with calibration mode {self.quant_params.calib_mode}')
        if self.quant_params.calib_mode.lower() == 'kl_divergence':
            with tvm.relay.quantize.qconfig(calibrate_mode=self.quant_params.calib_mode.lower(),
                                            weight_scale=self.quant_params.weights_scale.lower(),
                                            dtype_input=self.quant_params.dtype_input,
                                            dtype_weight=self.quant_params.dtype_weight,
                                            dtype_activation=self.quant_params.dtype_activation,
                                            partition_conversions=self.quant_params.partition_conversions):

                self.quant_model = tvm.relay.quantize.quantize(self.model.mod,
                                                               self.model.params,
                                                               dataset=self.calibrate_dataset())

        elif self.quant_params.calib_mode.lower() == 'global_scale':
            with tvm.relay.quantize.qconfig(calibrate_mode=self.quant_params.calib_mode.lower(),
                                            global_scale=self.quant_params.global_scale,
                                            weight_scale=self.quant_params.weights_scale.lower(),
                                            dtype_input=self.quant_params.dtype_input,
                                            dtype_weight=self.quant_params.dtype_weight,
                                            dtype_activation=self.quant_params.dtype_activation,
                                            partition_conversions=self.quant_params.partition_conversions):

                self.quant_model = tvm.relay.quantize.quantize(self.model.mod,
                                                               self.model.params)

        else:
            raise ValueError('Wrong calibration mode parameter.'
                             'Supported modes: kl_divergence, global_scale')

    def save_quant_model(self):
        self.output_dir = self.quant_params.output_dir
        if self.output_dir is None:
            self.output_dir = os.getcwd()

        self.log.info(f'Saving quantized model \"{self.model.model_name}\" to \"{self.output_dir}\"')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.log.info(f'Saving weights of the quantized model {self.model.model_name}')
        with open(f'{self.output_dir}/{self.model.model_name}.params', 'wb') as fo:
            fo.write(tvm.relay.save_param_dict(self.model.params))

        self.log.info(f'Saving quantized model {self.model.model_name}')
        with open(f'{self.output_dir}/{self.model.model_name}.json', 'w') as fo:
            fo.write(tvm.ir.save_json(self.quant_model))
