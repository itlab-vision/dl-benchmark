import sys
import pytest

import logging as log

from pathlib import Path

# to be able to access tests folder
sys.path.append(str(Path(__file__).resolve().parents[2]))
from tests.smoke_test.utils import create_empty_folder, execute_process  # noqa: E402, PLC0411

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = Path(SCRIPT_DIR, 'models_dir')
CACHE_DIR = Path(SCRIPT_DIR, 'cache_dir')

log.basicConfig(level='INFO', format=' %(levelname)-8s - %(message)s')


def download_models(models_list: list, output_dir: Path = OUTPUT_DIR, cache_dir: Path = CACHE_DIR,
                    precisions: str = 'FP32'):
    for model_name in models_list:
        command_line = (f'omz_downloader --output_dir {output_dir} --cache_dir {cache_dir} '
                        f'--name={model_name} --precisions {precisions}')
        execute_process(command_line=command_line, log=log)


def convert_models(models_list: list, output_dir: Path = OUTPUT_DIR, precisions: str = 'FP32'):
    for model_name in models_list:
        command_line = (f'omz_converter --output_dir {output_dir} --download_dir {output_dir} '
                        f'--name={model_name} --precisions {precisions}')
        execute_process(command_line=command_line, log=log)


def download_file(link, out_dir, filename):
    cmd = f'mkdir -p {out_dir} && curl -L -o {out_dir}/{filename} {link}'
    execute_process(command_line=cmd, log=log)


def check_used_mark(request, mark_name: str):
    used_marks = []
    used_marks.extend([instance.own_markers[0] for instance in request.node.items if instance.own_markers])

    if used_marks:
        return all(mark.name == mark_name for mark in used_marks)

    return False


@pytest.fixture(scope='session', autouse=True)
def prepare_folders(res_dir):
    """ Setup fixture """
    create_empty_folder(res_dir, log=log)
