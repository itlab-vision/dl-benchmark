import pytest

import logging as log

from collections import namedtuple
from pathlib import Path

from utils import execute_process, create_empty_folder

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = Path(SCRIPT_DIR, 'models_dir')
CACHE_DIR = Path(SCRIPT_DIR, 'cache_dir')
RES_DIR = Path(SCRIPT_DIR, 'res_dir')

SMOKE_CONFIGS_DIR_PATH = Path(SCRIPT_DIR, 'configs', 'dl_models')

TORCH_TVM_CONVERTER = Path.joinpath(SCRIPT_DIR.parents[1],
                                    'src/model_converters/tvm_converter/pytorch_to_tvm_converter.py')
MXNET_TVM_CONVERTER = Path.joinpath(SCRIPT_DIR.parents[1],
                                    'src/model_converters/tvm_converter/mxnet_to_tvm_converter.py')
CAFFE_TVM_CONVERTER = Path.joinpath(SCRIPT_DIR.parents[1],
                                    'src/model_converters/tvm_converter/caffe_to_tvm_converter.py')

DL_MODELS = ['resnet-50-pytorch', 'mobilenet-v1-1.0-224-tf', 'efficientnet-b0-pytorch', 'googlenet-v1']

log.basicConfig(level='INFO', format=' %(levelname)-8s - %(message)s')


def download_dl_models(models_list: list = DL_MODELS, output_dir: Path = OUTPUT_DIR, cache_dir: Path = CACHE_DIR):
    for model_name in models_list:
        command_line = f'omz_downloader --output_dir {output_dir} --cache_dir {cache_dir} --name={model_name}'
        execute_process(command_line=command_line, log=log)

    def download_resnet50():
        resnet_dir = Path(output_dir, 'resnet50')
        resnet_so_link = ('https://raw.githubusercontent.com/itlab-vision/itlab-vision-dl-benchmark-models/main/'
                          'models/classification/resnet50-tvm-optimized/resnet50.so')
        command_line_resnet_download = f'mkdir -p {resnet_dir} && '
        command_line_resnet_download += f'curl -o {resnet_dir}/resnet50.so {resnet_so_link}'
        execute_process(command_line=command_line_resnet_download, log=log)

    download_resnet50()


def convert_dl_models(models_list: list = DL_MODELS, output_dir: Path = OUTPUT_DIR):
    for model_name in models_list:
        command_line = (f'omz_converter --output_dir {output_dir} --download_dir {output_dir} '
                        f'--name={model_name} --precisions FP32')
        execute_process(command_line=command_line, log=log)


def convert_tvm_models(use_caffe: bool = False):
    pytorch_to_tvm_converter = (f'cd {OUTPUT_DIR} && python3 {TORCH_TVM_CONVERTER} -mn efficientnet_b0 '
                                f'-w {OUTPUT_DIR}/public/efficientnet-b0-pytorch/efficientnet-b0.pth '
                                '-is 1 3 224 224')
    mxnet_to_tvm_converter = (f'cd {OUTPUT_DIR} && python3 {MXNET_TVM_CONVERTER} -mn alexnet -is 1 3 224 224')
    caffe_to_tvm_converter = (f'cd {OUTPUT_DIR} && python3 {CAFFE_TVM_CONVERTER} -mn googlenet-v1 -is 1 3 224 224 '
                              f'-m {OUTPUT_DIR}/public/googlenet-v1/googlenet-v1.prototxt '
                              f'-w {OUTPUT_DIR}/public/googlenet-v1/googlenet-v1.caffemodel')

    execute_process(command_line=pytorch_to_tvm_converter, log=log)
    execute_process(command_line=mxnet_to_tvm_converter, log=log)

    if use_caffe:
        execute_process(command_line=caffe_to_tvm_converter, log=log)


def check_used_mark(request, mark_name: str):
    used_marks = []
    used_marks.extend([instance.own_markers[0] for instance in request.node.items if instance.own_markers])

    if used_marks:
        return all(mark.name == mark_name for mark in used_marks)

    return False


@pytest.fixture(scope='session', autouse=True)
def prepare_dl_models(request):
    if not OUTPUT_DIR.exists():
        download_dl_models()
        convert_dl_models()
        convert_tvm_models(use_caffe=check_used_mark(request, 'caffe'))


@pytest.fixture(scope='session', autouse=True)
def prepare_folders():
    """ Setup fixture """
    create_empty_folder(RES_DIR, log=log)


def pytest_generate_tests(metafunc):
    param_list = []
    id_list = []

    smoke_test_params = namedtuple('SmokeDLTestParams', 'config_path, config_name, model_name, classification_check')

    for config_file in SMOKE_CONFIGS_DIR_PATH.iterdir():
        config_name = config_file.stem
        config_naming_list = config_name.split('_')

        params = {'config_path': config_file, 'config_name': config_name, 'model_name': config_naming_list[0],
                  'classification_check': False}
        if 'classification' in config_naming_list:
            params.update({'classification_check': True})

        param_list.append(smoke_test_params(**params))
        id_list.append(config_file.stem)

    # Mark Caffe tests
    for i, test_param in enumerate(param_list):
        if test_param.config_name in ['googlenet-v1_Caffe', 'googlenet-v1_TVM_Caffe', 'googlenet-v1_TVM_TVM']:
            param_list[i] = pytest.param(test_param, marks=pytest.mark.caffe)

    metafunc.parametrize('test_configuration', param_list, ids=id_list)
