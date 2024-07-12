import abc
import sys
import importlib
import ast
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import ArgumentsParser  # noqa: E402


class ModelHandlerFactory:
    @staticmethod
    def get_source_framework_handler(args, log):
        framework = args['Framework']
        if framework.lower() == 'tensorflow':
            return NNCFModelHandlerTensorFlowFormat(log, args)
        elif framework.lower() == 'onnx':
            return NNCFModelHandlerONNXFormat(log, args)
        elif framework.lower() == 'openvino':
            return NNCFModelHandlerOpenVINOFormat(log, args)
        else:
            raise Exception(f'Unsupported framework: {framework}.')


class NNCFModelHandlerWrapper(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def dict_for_iter_log(self):
        return {
            'Name': self.handler.model_name,
            'Path to model': self.handler.model_path,
            'Path to weights': self.handler.model_params,
        }

    def _get_arguments(self):
        self.handler = ModelHandlerFactory.get_source_framework_handler(self.args,
                                                                        self._log)
        self.model = self.handler.read_model_from_source_framework()


class Handler:
    def __init__(self, log, args):
        self.log = log
        self.log.info('Parsing model arguments.')
        self.model_name = args['Name']
        self.model_path = args['Path']
        self.model_params = args['WeightsPath']
        self.input_name = args['InputName']
        self.output_name = args['OutputName']
        self.input_shape = ast.literal_eval(args['InputShape'])
        self.device = args['Device']
        self.framework = args['Framework']

    @abc.abstractmethod
    def read_model_from_source_framework(self):
        pass

    def save_model(self, quant_model, output_directory):
        if output_directory is None:
            output_directory = os.getcwd()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self.log.info(f'Saving model to {output_directory}')
        self._save_model_to_source_framework(quant_model,
                                             output_directory)

    @abc.abstractmethod
    def _save_model_to_source_framework(self,
                                        quant_model,
                                        output_directory):
        pass


class NNCFModelHandlerTensorFlowFormat(Handler):
    def __init__(self, log, reader):
        super().__init__(log, reader)
        self.tf = importlib.import_module('tensorflow')

    def read_model_from_source_framework(self):
        return self.tf.keras.models.load_model(Path(self.model_path))

    def _save_model_to_source_framework(self,
                                        quant_model,
                                        output_directory):
        self.tf.keras.saving.save_model(quant_model,
                                        f'{output_directory}/{self.model_name}',
                                        save_format='tf')


class NNCFModelHandlerONNXFormat(Handler):
    def __init__(self, log, reader):
        super().__init__(log, reader)
        self.onnx = importlib.import_module('onnx')

    def read_model_from_source_framework(self):
        return self.onnx.load(self.model_path)

    def _save_model_to_source_framework(self,
                                        quant_model,
                                        output_directory):
        self.onnx.save(quant_model, f'{output_directory}/{self.model_name}.onnx')


class NNCFModelHandlerOpenVINOFormat(Handler):
    def __init__(self, log, reader):
        super().__init__(log, reader)
        self.ov = importlib.import_module('openvino')

    def read_model_from_source_framework(self):
        core = self.ov.Core()
        return core.read_model(self.model_path)

    def _save_model_to_source_framework(self,
                                        quant_model,
                                        output_directory):
        self.ov.runtime.save_model(quant_model, f'{output_directory}/{self.model_name}.xml')
