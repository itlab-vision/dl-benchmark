import shutil
import sys

from pathlib import Path

# to be able to access src package
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.utils.cmd_handler import CMDHandler  # noqa: E402, PLC0411


def execute_process(command_line: str, log):
    cmd_handler = CMDHandler(command_line=command_line, log=log)
    cmd_handler.run(None)

    return cmd_handler.return_code, cmd_handler.output


def create_empty_folder(folder_path: Path, log):
    if not folder_path.exists():
        log.info(f'Folder {folder_path} missing, creating')
        folder_path.mkdir(parents=True)
    else:
        log.warning(f'Folder {folder_path} exists, re-creating')
        shutil.rmtree(folder_path.absolute())
        folder_path.mkdir(parents=True, exist_ok=True)
