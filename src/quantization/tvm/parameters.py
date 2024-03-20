import tvm
import os
import sys
import numpy as np
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import Reader  # noqa: E402


class TVMModelReader(Reader):
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


class TVMQuantParamReader(Reader):
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
