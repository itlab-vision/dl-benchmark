from pathlib import Path

from tests.smoke_test.conftest import SCRIPT_DIR, log
from tests.smoke_test.ac_smoke.conftest import AC_SMOKE_FOLDER
from tests.smoke_test.utils import execute_process

AC_CHECKER = Path(SCRIPT_DIR, '../../src/accuracy_checker/accuracy_checker.py')


def test_smoke_ac_models(test_configuration, res_dir):
    result_file = Path(res_dir, f'{test_configuration.config_name}.csv')
    _, omz_root = execute_process(command_line='python3 -c "import openvino.model_zoo as omz; print(omz.__path__[0])"',
                                  log=log)
    dataset_definitions = Path(omz_root[0].strip()).joinpath('data', 'dataset_definitions.yml')
    command_line = (f'python {AC_CHECKER} -r {result_file} -s {AC_SMOKE_FOLDER / "datasets_smoke"} '
                    f'-c {test_configuration.config_path} -d {dataset_definitions}')

    status, _ = execute_process(command_line=command_line, log=log)

    if status == 0:
        log.info(f'Success accuracy test on config file : {test_configuration.config_name}')
    else:
        raise Exception(f'Accuracy test on config file : {test_configuration.config_name} was ended with error')
