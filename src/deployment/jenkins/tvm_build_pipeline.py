import sys
import argparse
import os
import subprocess


class TVMBuilder:
    def __init__(self, branch, conda, py):
        self.branch = branch
        self.conda = conda
        self.py_version = py

    def _run(self, cmd):
        return subprocess.run(cmd, shell=True)

    def build_tvm(self):
        self._run(f'{self.conda}/bin/conda create -y -n tvm_main python=={self.py_version}')
        self._run(f'{self.conda}/bin/conda install -n tvm_main -c conda-forge -y gcc=12.1.0')
        self._run(f'{self.conda}/bin/conda install -n tvm_main -c conda-forge -y gxx_linux-64')
        self._run(f'{self.conda}/envs/tvm_main/bin/pip3 install -r requirements.txt')
        self._run(f'git clone --recursive https://github.com/apache/tvm -b {self.branch}')
        self._run(f'cd tvm && mkdir -p build && cd build && cmake -DUSE_LLVM=ON ../ && make -j$(nproc --all) && cd ../python && {self.conda}/envs/tvm_main/bin/python setup.py install --user')


def cli_arguments_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--branch',
                        help='Branch to build tvm.',
                        dest='branch',
                        required=True,
                        type=str)
    parser.add_argument('-p', '--python_version',
                        help='Python version to create conda env.',
                        dest='py',
                        required=True,
                        type=str)
    parser.add_argument('-cp', '--conda_prefix',
                        help='Path to miniconda3 directory.',
                        dest='conda',
                        required=True,
                        type=str)

    return parser.parse_args()


def main():
    args = cli_arguments_parse()
    cr = TVMBuilder(args.branch, args.conda, args.py)
    cr.build_tvm()


if __name__ == '__main__':
    sys.exit(main() or 0)
