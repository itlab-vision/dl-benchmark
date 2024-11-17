import sys
import argparse
import os
import subprocess


class EnvCreator:
    def __init__(self, frameworks, py_version):
        self.frameworks = frameworks.split(',')
        self.py_version = py_version

    def _run(self, cmd):
        return subprocess.run(cmd, shell=True)

    def create_envs(self):
        self._run(f'conda create -y -n tvm_main python=={self.py_version}')
        self._run(f'$CONDA_ROOT/envs/tvm_main/bin/pip3 install -r requirements.txt')
        for framework in self.frameworks:
            self._run(f'conda create -y --name tvm_{framework} --clone tvm_main')
            self._run(f'$CONDA_ROOT/envs/tvm_{framework}/bin/pip3 install {framework}')


def cli_arguments_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--branch',
                        help='Branch to build tvm.',
                        dest='branch',
                        required=True,
                        type=str)
    parser.add_argument('-f', '--frameworks',
                        help='Frameworks to create pyenv.',
                        dest='frameworks',
                        required=True,
                        type=str)
    parser.add_argument('-p', '--python_version',
                        help='Python version to create pyenv.',
                        dest='py',
                        required=True,
                        type=str)

    return parser.parse_args()

def main():
    args = cli_arguments_parse()
    cr = EnvCreator(args.frameworks, args.py)
    cr.create_envs()


if __name__=='__main__':
    sys.exit(main() or 0)