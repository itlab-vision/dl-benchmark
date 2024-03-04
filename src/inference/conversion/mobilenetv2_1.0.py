from mxnet.onnx import export_model
import logging

logging.basicConfig(level=logging.INFO)

path_prefix = './public/mobilenetv2_1.0/'
sym = path_prefix + 'mobilenetv2_1.0-symbol.json'
params = path_prefix + 'mobilenetv2_1.0-0000.params'
in_shape = (3, 3, 224, 224)
onnx_file_path = './results/mobilenetv2_1.0.onnx'

export_model(sym=sym, params=params, in_shapes=[in_shape], onnx_file_path=onnx_file_path)
