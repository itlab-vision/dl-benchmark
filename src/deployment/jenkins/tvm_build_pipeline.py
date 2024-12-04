import sys
import argparse
import os
import subprocess


class TVMBuilder:
    def __init__(self, branch, conda):
        self.branch = branch
        self.conda = conda

    def _run(self, cmd):
        return subprocess.run(cmd, shell=True)

    def build_tvm(self):
        self._run(f'git clone --recursive https://github.com/apache/tvm -b {self.branch}')
        self._run(f'cd tvm && mkdir -p build && cd build && cmake -DUSE_LLVM=ON ../ && make -j$(nproc --all) && cd ../python && {self.conda}/envs/tvm_main/bin/python setup.py install --user')


def cli_arguments_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--branch',
                        help='Branch to build tvm.',
                        dest='branch',
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
    cr = TVMBuilder(args.branch, args.conda)
    cr.build_tvm()


if __name__ == '__main__':
    sys.exit(main() or 0)
