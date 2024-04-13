import ast
import nncf
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import Reader  # noqa: E402

PRESET = {'performance': nncf.QuantizationPreset.PERFORMANCE,
          'mixed': nncf.QuantizationPreset.MIXED}

MODEL_TYPE = {'transformer': nncf.ModelType.TRANSFORMER}


class NNCFQuantParamReader(Reader):
    def __init__(self, log):
        super().__init__(log)

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
        self.model_reader = model_reader
        self.dataset = dataset
        self.quant_params = quant_params

    def transform_fn(self, data_item):
        images = data_item
        return {self.model_reader.model.graph.input[0].name: images}

    def quantization_nncf(self):
        self.log.info('Starting quantization process.')
        if self.model_reader.framework.lower() == 'onnx':
            calibration_dataset = nncf.Dataset(self.dataset, transform_func=self.transform_fn)
        else:
            calibration_dataset = nncf.Dataset(self.dataset)
        self.quant_model = nncf.quantize(model=self.model_reader.model, calibration_dataset=calibration_dataset,
                                         model_type=self.quant_params.model_type, preset=self.quant_params.preset,
                                         subset_size=self.quant_params.subset_size)

    def save_quant_model(self):
        self.log.info('Save quantized model.')
        self.model_reader.save_model(self.quant_model, self.quant_params.output_dir)
