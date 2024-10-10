import pytest

from collections import namedtuple
from pathlib import Path

from tests.smoke_test.utils import execute_process
from tests.smoke_test.conftest import (SCRIPT_DIR, OUTPUT_DIR, log,
                                       download_models, convert_models)

QUANTIZATION_CONFIG_DIR_PATH = Path(SCRIPT_DIR, 'configs', 'quantization_models')
TVM_CONVERTER = Path.joinpath(SCRIPT_DIR.parents[1], 'src/model_converters/tvm_converter/tvm_converter.py')

DL_MODELS = ['resnet-50-pytorch', 'densenet-121-tf']


def pytest_addoption(parser):
    parser.addoption('--models',
                     nargs='+',
                     default=None,
                     required=False,
                     help='Space-separated list of models to launch benchmark on them')
    parser.addoption('--res_dir',
                     type=Path,
                     default=Path(SCRIPT_DIR, 'res_dir'),
                     required=False,
                     help='Path to dir to save results (*.csv)')
    parser.addoption('--config_dir',
                     type=Path,
                     default=None,
                     required=False,
                     help='Path to models config dir')


@pytest.fixture(scope='session')
def overrided_models(pytestconfig):
    """Fixture function for command-line option."""
    return pytestconfig.getoption('models')


@pytest.fixture(scope='session', autouse=True)
def prepare_dl_models(request, overrided_models):

    models_per_mark = DL_MODELS
    enabled_models = overrided_models if overrided_models else models_per_mark

    download_models(models_list=enabled_models)
    convert_models(models_list=enabled_models)
    convert_models_to_tvm()


@pytest.fixture(scope='session')
def res_dir(pytestconfig):
    """Fixture function for command-line option."""
    return pytestconfig.getoption('res_dir')


def convert_models_to_tvm():
    onnx_to_tvm = (f'cd {OUTPUT_DIR} && python3 {TVM_CONVERTER} -mn resnet50 '
                   f'-m {OUTPUT_DIR}/public/resnet-50-pytorch/resnet-v1-50.onnx '
                   f'-op {OUTPUT_DIR}/public/resnet-50-pytorch/ -is 1 3 224 224 '
                   f'-f onnx')
    try:
        import tvm  # noqa: F401
        execute_process(command_line=onnx_to_tvm, log=log)
    except ImportError:
        log.info('No tvm module found, skip tvm converter.')


def pytest_generate_tests(metafunc):
    param_list = []
    id_list = []

    smoke_test_params = namedtuple('SmokeDLTestParams', 'config_path, config_name, model_name, framework')

    overrided_config_dir = metafunc.config.getoption('config_dir')
    overrided_models = metafunc.config.getoption('models')
    smoke_configs_dir = overrided_config_dir if overrided_config_dir else QUANTIZATION_CONFIG_DIR_PATH

    for config_file in smoke_configs_dir.iterdir():
        config_name = config_file.stem
        config_naming_list = config_name.split('_')
        model_name = config_naming_list[0]
        framework = config_naming_list[1]

        params = {'config_path': config_file, 'config_name': config_name, 'model_name': model_name,
                  'framework': framework}

        if overrided_models and model_name not in overrided_models:
            continue

        param_list.append(smoke_test_params(**params))
        id_list.append(config_file.stem)

    metafunc.parametrize('test_configuration', param_list, ids=id_list)
