from pathlib import Path

from tests.smoke_test.conftest import SCRIPT_DIR, log

from tests.smoke_test.utils import execute_process

INFERENCE_BENCHMARK = Path(SCRIPT_DIR, '../../src/benchmark/inference_benchmark.py')


def check_classification(output: list, model_name: str):
    classification_top_res = {'resnet-50-pytorch': 'baseball player',
                              'efficientnet-b0-pytorch': 'palace',
                              'mobilenet-v1-1.0-224-tf': 'window shade',
                              'mobilenet-v1-1.0-224-tflite': 'damselfly',
                              'squeezenet': 'ballplayer, baseball player'}
    start_search_index = output.index('[ INFO ] Result for image 1\n')
    search_area = output[start_search_index + 1:start_search_index + 5]

    pass_status = False
    for res in search_area:
        if classification_top_res[model_name] in res:
            pass_status = True

    if pass_status:
        log.info(f'Classification passed for model {model_name}')
    else:
        raise Exception(f'Classification failed. \nPredicted: {search_area}\n'
                        f'Actual: {classification_top_res[model_name]}')


def test_smoke_dl_models(test_configuration, res_dir, openvino_cpp_benchmark_dir, cpp_benchmarks_dir):
    result_file = Path(res_dir, f'{test_configuration.config_name}.csv')
    command_line = (f'python3 {INFERENCE_BENCHMARK} --result {result_file} --executor_type host_machine '
                    f'--config {test_configuration.config_path}')
    if openvino_cpp_benchmark_dir:
        command_line += f' --openvino_cpp_benchmark_dir {openvino_cpp_benchmark_dir}'
    if cpp_benchmarks_dir:
        command_line += f' --cpp_benchmarks_dir {cpp_benchmarks_dir}'

    status, output = execute_process(command_line=command_line, log=log)

    if test_configuration.classification_check:
        check_classification(output, test_configuration.model_name)

    if status == 0:
        log.info(f'Success inference test on config file : {test_configuration.config_name}')
    else:
        raise Exception(f'Inference test on config file : {test_configuration.config_name} was ended with error')
