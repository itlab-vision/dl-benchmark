import sys
import argparse
import os
import subprocess


class TVMBuilder:
    def __init__(self, branch):
        self.branch = branch

    def _run(self, cmd):
        return subprocess.run(cmd, shell=True)

    def build_tvm(self):
        self._run(f'git clone --recursive https://github.com/apache/tvm -b {self.branch}')
        self._run(f'cd tvm && mkdir build && cd build && cmake -DUSE_LLVM=ON ../ && make -j2 && cd ../python && $CONDA_ROOT/envs/tvm_main/bin/python setup.py install --user')


def cli_arguments_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--branch',
                        help='Branch to build tvm.',
                        dest='branch',
                        required=True,
                        type=str)

    return parser.parse_args()

def main():
    args = cli_arguments_parse()
    cr = TVMBuilder(args.branch)
    cr.build_tvm()


if __name__ == '__main__':
    sys.exit(main() or 0)
