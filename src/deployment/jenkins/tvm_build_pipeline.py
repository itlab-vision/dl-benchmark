import sys
import argparse
import subprocess


class TVMBuilder:
    def __init__(self, branch, conda, py):
        self.branch = branch
        self.conda = conda
        self.py_version = py

    def _run(self, cmd):
        return subprocess.run(cmd, shell=True)

    def build_tvm(self):
        self._run(f'{self.conda}/bin/conda create -y -n tvm_main_{self.branch} python=={self.py_version}')
        self._run(f'{self.conda}/bin/conda install -n tvm_main_{self.branch} -c conda-forge -y gcc=12.1.0')
        self._run(f'{self.conda}/bin/conda install -n tvm_main_{self.branch} -c conda-forge -y gxx_linux-64')
        self._run(f'{self.conda}/envs/tvm_main_{self.branch}/bin/pip3 install -r requirements.txt')
        self._run(f'git clone --recursive https://github.com/apache/tvm -b {self.branch}')
        command1 = 'cd tvm && mkdir -p build && cd build && cmake -DUSE_LLVM=ON -DUSE_BLAS=openblas ../ && '
        command2 = 'make -j$(nproc --all) && cd ../python && '
        command3 = f'{self.conda}/envs/tvm_main_{self.branch}/bin/python setup.py install --user' 
        self._run(command1 + command2 + command3)


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
