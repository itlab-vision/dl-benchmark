import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


class prepend_to_path:
    def __init__(self, paths):
        self._preprended_paths = paths
        self._original_path = None

    def __enter__(self):
        self._original_path = deepcopy(sys.path)
        if self._preprended_paths is not None:
            sys.path = self._preprended_paths + sys.path

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._original_path is not None:
            sys.path = self._original_path


def to_camel_case(text: str):
    s = text.replace('-', ' ').replace('_', ' ')
    s = s.split()
    if len(text) == 0:
        return text

    return s[0].capitalize() + ''.join(i.capitalize() for i in s[1:])


def create_folder(folder_path: Path, log=None):
    """
    Creates empty folder under provided path.
    @param folder_path: pathlib. Path folder path
    @param log
    """
    if not folder_path.exists():
        if log:
            log.info(f'Creating {folder_path} folder')
        folder_path.mkdir(parents=True)


def github_clone(repo_name: str, dist: str):
    repo_name = f'https://github.com/{repo_name}.git'
    subprocess.run(['git', 'clone', '--progress', repo_name, dist])


def regex_replace_in_file(file: Path, regex: str, replacement: str, log=None):
    with open(file, 'r+') as f:
        content = f.read()
        pattern = re.compile(re.escape(regex))
        file_content = pattern.sub(replacement, content)
        f.seek(0)
        f.truncate()
        f.write(file_content)
    if log:
        log.info(f'File content was modified: {file}')
