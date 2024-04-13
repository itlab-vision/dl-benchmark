from pathlib import Path

from tests.smoke_test.utils import execute_process
from tests.smoke_test.conftest import (SCRIPT_DIR, log)

QUANTIZATION_TFLITE = Path.joinpath(SCRIPT_DIR.parents[1], 'src/quantization/tflite/quantization_tflite.py')
QUANTIZATION_TVM = Path.joinpath(SCRIPT_DIR.parents[1], 'src/quantization/tvm/quantization_tvm.py')
QUANTIZATION_NNCF = Path.joinpath(SCRIPT_DIR.parents[1], 'src/quantization/nncf/quantization_nncf.py')

TVM_CONVERTER = Path.joinpath(SCRIPT_DIR.parents[1], 'src/model_converters/tvm_converter/tvm_converter.py')


def test_smoke_dl_models(test_configuration):
    if test_configuration.framework == 'NNCF':
        command_line = (f'python3 {QUANTIZATION_NNCF} -c {test_configuration.config_path}')
    elif test_configuration.framework == 'TFLITE':
        command_line = (f'python3 {QUANTIZATION_TFLITE} -c {test_configuration.config_path}')
    elif test_configuration.framework == 'TVM':
        command_line = (f'python3 {QUANTIZATION_TVM} -c {test_configuration.config_path}')
    else:
        raise Exception(f'Unsupported framework: {test_configuration.framework}')

    status, _ = execute_process(command_line=command_line, log=log)

    if status == 0:
        log.info(f'Success quantization test on config file : {test_configuration.config_name}')
    else:
        raise Exception(f'Quantization test on config file : {test_configuration.config_name} was ended with error')
