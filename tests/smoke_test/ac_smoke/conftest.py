import pytest

from collections import namedtuple
from pathlib import Path

from tests.smoke_test.utils import execute_process, create_empty_folder
from tests.smoke_test.conftest import (SCRIPT_DIR, log,
                                       download_models, convert_models)

AC_SMOKE_FOLDER = Path(SCRIPT_DIR, 'ac_smoke')
SMOKE_CONFIGS_DIR_PATH = Path.joinpath(SCRIPT_DIR, 'configs', 'ac_models')

AC_MODELS = ['Sphereface']


@pytest.fixture(scope='session', autouse=True)
def prepare_ac_models():
    download_models(models_list=AC_MODELS)
    convert_models(models_list=AC_MODELS)


@pytest.fixture(scope='session', autouse=True)
def prepare_dataset():
    lfw_source = Path(SCRIPT_DIR, 'lfw.pickle')
    if lfw_source.is_file():
        lfw_source.unlink()

    datasets_folder = Path.joinpath(AC_SMOKE_FOLDER, 'datasets_smoke', 'LFW')
    if not datasets_folder.exists():
        create_empty_folder(datasets_folder, log=log)
        execute_process(command_line='wget http://vis-www.cs.umass.edu/lfw/lfw-a.tgz '
                                     f'-O {datasets_folder}/lfw-a.tgz && '
                                     f'tar -xf {datasets_folder}/lfw-a.tgz -C {datasets_folder}',
                        log=log)

        annotation_folder = Path(datasets_folder, 'annotation')
        create_empty_folder(annotation_folder, log=log)
        execute_process(command_line='wget http://vis-www.cs.umass.edu/lfw/pairs.txt '
                                     f'-O {annotation_folder}/pairs.txt.bak && '
                                     "grep -E '^A[[:graph:]]+[[:space:]][[:digit:]]+[[:space:]][[:digit:]]+' "
                                     f'{annotation_folder}/pairs.txt.bak > {annotation_folder}/pairs.txt',
                        log=log)
        execute_process(
            command_line='wget '
                         'https://raw.githubusercontent.com/clcarwin/sphereface_pytorch/master/data/lfw_landmark.txt '
                         f'-O {annotation_folder}/lfw_landmark.txt.bak && '
                         f'grep ^A {annotation_folder}/lfw_landmark.txt.bak > {annotation_folder}/lfw_landmark.txt',
            log=log)


def pytest_generate_tests(metafunc):
    param_list = []
    id_list = []

    smoke_test_params = namedtuple('SmokeACTestParams', 'config_path, config_name, model_name')

    for config_file in SMOKE_CONFIGS_DIR_PATH.iterdir():
        if config_file.suffix == '.xml':
            config_name = config_file.stem
            config_naming_list = config_name.split('_')

            params = {'config_path': config_file, 'config_name': config_name, 'model_name': config_naming_list[0]}

            param_list.append(smoke_test_params(**params))
            id_list.append(config_file.stem)

    metafunc.parametrize('test_configuration', param_list, ids=id_list)
