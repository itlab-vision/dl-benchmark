import sys
import ast
import numpy as np
import os
import tensorflow as tf
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import ArgumentsParser  # noqa: E402


OPTIMIZATIONS = {
    'latency': tf.lite.Optimize.OPTIMIZE_FOR_LATENCY,
    'default': tf.lite.Optimize.DEFAULT,
    'size': tf.lite.Optimize.OPTIMIZE_FOR_SIZE,
}

SUPPORTED_OPS = {
    'int8': tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
    'int16': tf.lite.OpsSet.EXPERIMENTAL_TFLITE_BUILTINS_ACTIVATIONS_INT16_WEIGHTS_INT8,
}

SUPPORTED_TYPES = {
    'float16': tf.float16,
    'int8': tf.int8,
}


class TFLiteModelReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def _get_arguments(self):
        self._log.info('Parsing model arguments.')
        self.model_name = self.args['Name']
        self.model_path = self.args['Path']
        self._read_model()

    def dict_for_iter_log(self):
        return {
            'Name': self.model_name,
            'Path to model': self.model_path,
        }

    def _read_model(self):
        self.converter = tf.lite.TFLiteConverter.from_saved_model(self.model_path)


class TFLiteQuantParamReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def dict_for_iter_log(self):
        return {
            'Optimizations': self.optimizations,
            'Supported operations': self.supported_ops,
            'Supported types': self.supported_types,
        }

    def _get_arguments(self):
        self._log.info('Parsing parameters of quantization.')
        self.optimizations = (ast.literal_eval(self.args['Optimizations'])
                              if self.args['Optimizations'] is not None else [])
        self.supported_ops = (ast.literal_eval(self.args['SupportedOperations'])
                              if self.args['SupportedOperations'] is not None else [])
        self.supported_types = (ast.literal_eval(self.args['SupportedTypes'])
                                if self.args['SupportedTypes'] is not None else [])
        self.optimizations = self._convert_to_list_of_tf_objects(self.optimizations,
                                                                 OPTIMIZATIONS)
        self.supported_ops = self._convert_to_list_of_tf_objects(self.supported_ops,
                                                                 SUPPORTED_OPS)
        self.supported_types = self._convert_to_list_of_tf_objects(self.supported_types,
                                                                   SUPPORTED_TYPES)
        self.output_dir = self.args['OutputDirectory']

    def _convert_to_list_of_tf_objects(self, keys, dictionary):
        return [dictionary[key] for key in keys]


class TFLiteQuantizationProcess:
    def __init__(self, log, model_reader, dataset, quant_params):
        self.log = log
        self.quant_model = None
        self.model_reader = model_reader
        self.dataset = dataset
        self.quant_params = quant_params

    def transform_fn(self):
        for data in self.dataset:
            yield [data.astype(np.float32)]

    def quantization_tflite(self):
        converter = self.model_reader.converter
        converter.optimizations = self.quant_params.optimizations
        converter.representative_dataset = self.transform_fn
        converter.target_spec.supported_ops = self.quant_params.supported_ops
        converter.target_spec.supported_types = self.quant_params.supported_types
        self.quant_model = converter.convert()

    def save_quant_model(self):
        model_name = self.model_reader.model_name
        output_dir = self.quant_params.output_dir
        if output_dir is None:
            output_dir = os.getcwd()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.log.info(f'Saving model to {output_dir}')
        with open(f'{output_dir}/{model_name}.tflite', 'wb') as f:
            f.write(self.quant_model)
