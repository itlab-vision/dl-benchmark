import ast
import nncf
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import ArgumentsParser  # noqa: E402

PRESET = {'performance': nncf.QuantizationPreset.PERFORMANCE,
          'mixed': nncf.QuantizationPreset.MIXED}

MODEL_TYPE = {'transformer': nncf.ModelType.TRANSFORMER}


class NNCFQuantParamReader(ArgumentsParser):
    def __init__(self, log):
        super().__init__(log)

    def dict_for_iter_log(self):
        return {
            'Model type': self.model_type,
            'Subset size': self.subset_size,
            'Preset': self.preset,
        }

    def _get_arguments(self):
        self._log.info('Parsing parameters of quantization.')
        self.model_type = (MODEL_TYPE[self.args['ModelType']]
                           if self.args['ModelType'] is not None
                           else None)
        self.preset = (PRESET[self.args['Preset']]
                       if self.args['Preset'] is not None
                       else None)
        self.subset_size = ast.literal_eval(self.args['SubsetSize'])
        self.output_dir = self.args['OutputDirectory']


class NNCFQuantizationProcess:
    def __init__(self, log, model_reader, dataset, quant_params):
        self.log = log
        self.quant_model = None
        self.handler = model_reader.handler
        self.model = model_reader.model
        self.dataset = dataset
        self.quant_params = quant_params

    def transform_fn(self, data_item):
        images = data_item
        return {self.model.graph.input[0].name: images}

    def quantization_nncf(self):
        self.log.info('Starting quantization process.')
        if self.handler.framework.lower() == 'onnx':
            calibration_dataset = nncf.Dataset(self.dataset, transform_func=self.transform_fn)
        else:
            calibration_dataset = nncf.Dataset(self.dataset)
        self.quant_model = nncf.quantize(model=self.model, calibration_dataset=calibration_dataset,
                                         model_type=self.quant_params.model_type, preset=self.quant_params.preset,
                                         subset_size=self.quant_params.subset_size)

    def save_quant_model(self):
        self.log.info('Save quantized model.')
        self.handler.save_model(self.quant_model, self.quant_params.output_dir)
