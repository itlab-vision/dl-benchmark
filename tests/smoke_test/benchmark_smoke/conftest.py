import pytest

from collections import namedtuple
from pathlib import Path

from tests.smoke_test.utils import execute_process
from tests.smoke_test.conftest import (SCRIPT_DIR, OUTPUT_DIR, log,
                                       check_used_mark, download_models, download_file, convert_models)

SMOKE_CONFIGS_DIR_PATH = Path(SCRIPT_DIR, 'configs', 'dl_models')

TVM_CONVERTER = Path.joinpath(SCRIPT_DIR.parents[1], 'src/model_converters/tvm_converter/tvm_converter.py')

TVM_COMPILER = Path.joinpath(SCRIPT_DIR.parents[1], 'src/model_converters/tvm_converter/tvm_compiler.py')

DL_MODELS = ['resnet-50-pytorch', 'mobilenet-v1-1.0-224-tf', 'mobilenet-v2-1.4-224', 'efficientnet-b0-pytorch',
             'deeplabv3', 'road-segmentation-adas-0001', 'semantic-segmentation-adas-0001', 'efficientdet-d0-tf',
             'face-detection-0206', 'person-detection-asl-0001', 'person-detection-action-recognition-0005',
             'person-detection-action-recognition-0006', 'person-detection-raisinghand-recognition-0001',
             'person-detection-action-recognition-teacher-0002', 'yolo-v2-ava-0001', 'yolo-v2-tiny-ava-0001',
             'yolo-v2-tf', 'yolo-v3-tf']
DL_CAFFE_MODELS = ['googlenet-v1']


def pytest_addoption(parser):
    parser.addoption('--models',
                     nargs='+',
                     default=None,
                     required=False,
                     help='Space-separated list of models to launch benchmark on them')
    parser.addoption('--config_dir',
                     type=Path,
                     default=None,
                     required=False,
                     help='Path to models config dir')
    parser.addoption('--res_dir',
                     type=Path,
                     default=Path(SCRIPT_DIR, 'res_dir'),
                     required=False,
                     help='Path to dir to save results (*.csv)')
    parser.addoption('--openvino_cpp_benchmark_dir',
                     type=Path,
                     default=None,
                     required=False,
                     help='Path to the folder with pre-built OpenVINO C++ Benchmark App')
    parser.addoption('--cpp_benchmarks_dir',
                     type=Path,
                     dest='cpp_benchmarks_dir',
                     default=None,
                     required=False,
                     help='Path to the folder with pre-built C++ Benchmark apps')


@pytest.fixture(scope='session')
def openvino_cpp_benchmark_dir(pytestconfig):
    """Fixture function for command-line option."""
    return pytestconfig.getoption('openvino_cpp_benchmark_dir')


@pytest.fixture(scope='session')
def cpp_benchmarks_dir(pytestconfig):
    """Fixture function for command-line option."""
    return pytestconfig.getoption('cpp_benchmarks_dir')


@pytest.fixture(scope='session')
def res_dir(pytestconfig):
    """Fixture function for command-line option."""
    return pytestconfig.getoption('res_dir')


@pytest.fixture(scope='session')
def overrided_models(pytestconfig):
    """Fixture function for command-line option."""
    return pytestconfig.getoption('models')


def download_dgl_models(output_dir: Path = OUTPUT_DIR):
    dgl_dir = Path(output_dir, 'dgl')
    dgl_pt_link = ('https://raw.githubusercontent.com/itlab-vision/'
                   'itlab-vision-dl-benchmark-models/main/dgl/models/'
                   'classification/GCN/gcn_model.pt')
    download_file(dgl_pt_link, dgl_dir, 'gcn_model.pt')

    dgl_py_link = ('https://raw.githubusercontent.com/itlab-vision/'
                   'itlab-vision-dl-benchmark-models/main/dgl/models/'
                   'classification/GCN/GCN.py')
    download_file(dgl_py_link, dgl_dir, 'GCN.py')


def download_citation_gcn(output_dir: Path = OUTPUT_DIR):
    cit_gcn_dir = Path(output_dir, 'citation-gcn')
    cit_gcn_link = ('https://raw.githubusercontent.com/itlab-vision/itlab-vision-dl-benchmark-models/main/'
                    'spektral/models/classification/citation-gcn/citation-gcn.keras')
    download_file(cit_gcn_link, cit_gcn_dir, 'citation-gcn.keras')


def download_resnet50(output_dir: Path = OUTPUT_DIR):
    resnet_dir = Path(output_dir, 'resnet50')
    resnet_so_link = ('https://raw.githubusercontent.com/itlab-vision/itlab-vision-dl-benchmark-models/main/'
                      'tvm/models/classification/resnet50-tvm-optimized/resnet50.so')
    download_file(resnet_so_link, resnet_dir, 'resnet50.so')


def download_old_instance_segmentation(output_dir: Path = OUTPUT_DIR):
    instance_seg_dir = Path(output_dir, 'instance-segmentation-security-0083')
    instance_seg_link = ('https://storage.openvinotoolkit.org/repositories/open_model_zoo/2021.2/'
                         'models_bin/2/instance-segmentation-security-0083/FP32/')
    model_link = instance_seg_link + 'instance-segmentation-security-0083.xml'
    weights_link = instance_seg_link + 'instance-segmentation-security-0083.bin'

    download_file(model_link, instance_seg_dir, 'instance-segmentation-security-0083.xml')
    download_file(weights_link, instance_seg_dir, 'instance-segmentation-security-0083.bin')


def download_yolov2_tiny_tf(output_dir: Path = OUTPUT_DIR):
    yolov2_tiny_tf_dir = Path(output_dir, 'yolo-v2-tiny-tf')
    model_link = ('https://storage.openvinotoolkit.org/repositories/open_model_zoo/public/2024.0/'
                  'yolo-v2-tiny-tf/yolo-v2-tiny.pb')
    download_file(model_link, yolov2_tiny_tf_dir, 'yolo-v2-tiny.pb')


def download_yolov7_onnx(output_dir: Path = OUTPUT_DIR):
    yolov7_onnx_dir = Path(output_dir, 'yolo-v7-onnx')
    model_link = 'https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-nms-640.onnx'
    download_file(model_link, yolov7_onnx_dir, 'yolo-v7.onnx')


def download_facedet_full(output_dir: Path = OUTPUT_DIR):
    facedet_full_dir = Path(output_dir, 'face-detection-fr')
    model_link = ('https://github.com/patlevin/face-detection-tflite/blob/main/fdlite/data/'
                  'face_detection_full_range.tflite')
    download_file(model_link, facedet_full_dir, 'face_detection_full_range.tflite')


def convert_models_to_tvm(use_caffe: bool = False):
    pytorch_to_tvm_converter = (f'cd {OUTPUT_DIR} && python3 {TVM_CONVERTER} -mn efficientnet_b0 '
                                f'-w {OUTPUT_DIR}/public/efficientnet-b0-pytorch/efficientnet-b0.pth '
                                f'-is 1 3 224 224 -f pytorch -op {OUTPUT_DIR}/public/efficientnet-b0-pytorch/')
    mxnet_to_tvm_converter = f'cd {OUTPUT_DIR} && python3 {TVM_CONVERTER} -mn alexnet -is 1 3 224 224 -f mxnet'
    caffe_to_tvm_converter = (f'cd {OUTPUT_DIR} && python3 {TVM_CONVERTER} -mn googlenet-v1 -is 1 3 224 224 '
                              f'-m {OUTPUT_DIR}/public/googlenet-v1/googlenet-v1.prototxt '
                              f'-w {OUTPUT_DIR}/public/googlenet-v1/googlenet-v1.caffemodel '
                              f'-op {OUTPUT_DIR}/public/googlenet-v1/ -f caffe')
    tvm_compiler = (f'cd {OUTPUT_DIR} && python3 {TVM_COMPILER} -m alexnet.json '
                    '-p alexnet.params -t llvm --lib_name alexnet_vm.so -vm')

    if use_caffe:
        execute_process(command_line=caffe_to_tvm_converter, log=log)
    else:
        try:
            import tvm  # noqa: F401
            execute_process(command_line=pytorch_to_tvm_converter, log=log)
            execute_process(command_line=mxnet_to_tvm_converter, log=log)
            execute_process(command_line=tvm_compiler, log=log)
        except ImportError:
            log.info('No tvm module found, skip tvm converters')


@pytest.fixture(scope='session', autouse=True)
def prepare_dl_models(request, overrided_models):
    use_caffe = check_used_mark(request, 'caffe')

    models_per_mark = DL_CAFFE_MODELS if use_caffe else DL_MODELS
    enabled_models = overrided_models if overrided_models else models_per_mark

    download_models(models_list=enabled_models)

    if not use_caffe:
        convert_models(models_list=enabled_models)

        download_dgl_models()
        download_resnet50()
        download_old_instance_segmentation()
        download_yolov2_tiny_tf()
        download_yolov7_onnx()
        download_facedet_full()
        download_citation_gcn()

    convert_models_to_tvm(use_caffe)


def pytest_generate_tests(metafunc):
    param_list = []
    id_list = []

    smoke_test_params = namedtuple('SmokeDLTestParams', 'config_path, config_name, model_name, classification_check')

    overrided_config_dir = metafunc.config.getoption('config_dir')
    overrided_models = metafunc.config.getoption('models')
    smoke_configs_dir = overrided_config_dir if overrided_config_dir else SMOKE_CONFIGS_DIR_PATH

    for config_file in smoke_configs_dir.iterdir():
        config_name = config_file.stem
        config_naming_list = config_name.split('_')
        model_name = config_naming_list[0]

        params = {'config_path': config_file, 'config_name': config_name, 'model_name': model_name,
                  'classification_check': False}
        if 'classification' in config_naming_list:
            params.update({'classification_check': True})

        if overrided_models and model_name not in overrided_models:
            continue

        param_list.append(smoke_test_params(**params))
        id_list.append(config_file.stem)

    # Mark Caffe tests
    for i, test_param in enumerate(param_list):
        if test_param.config_name in ['googlenet-v1_Caffe', 'googlenet-v1_TVM_Caffe', 'googlenet-v1_TVM']:
            param_list[i] = pytest.param(test_param, marks=pytest.mark.caffe)
        if test_param.config_name in ['dgl']:
            param_list[i] = pytest.param(test_param)

    metafunc.parametrize('test_configuration', param_list, ids=id_list)
