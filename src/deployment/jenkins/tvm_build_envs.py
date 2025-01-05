import sys
import argparse
import os
import subprocess


class EnvCreator:
    def __init__(self, frameworks, py_version, conda, branch):
        self.frameworks = frameworks.split(',')
        self.py_version = py_version
        self.conda_prefix = conda
        self.branch = branch

    def _run(self, cmd):
        return subprocess.run(cmd, shell=True)

    def create_envs(self):
        if len(self.frameworks) != 0:
            for framework in self.frameworks:
                self._run(f'{self.conda_prefix}/bin/conda create -y --name tvm_{framework} --clone tvm_main_{self.branch}')
                if framework != 'mxnet':
                    self._run(f'{self.conda_prefix}/envs/tvm_{framework}_{self.branch}/bin/pip3 install {framework}')
                else:
                    self._run(f'{self.conda_prefix}/envs/tvm_{framework}_{self.branch}/bin/pip3 install {framework}==1.9.1')
                    self._run(f'{self.conda_prefix}/envs/tvm_{framework}_{self.branch}/bin/pip3 install gluoncv[full]')
                    self._run(f'{self.conda_prefix}/envs/tvm_{framework}_{self.branch}/bin/pip3 uninstall -y numpy')
                    self._run(f'{self.conda_prefix}/envs/tvm_{framework}_{self.branch}/bin/pip3 install numpy==1.23.1')


def cli_arguments_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--branch',
                        help='Branch to build tvm.',
                        dest='branch',
                        required=True,
                        type=str)
    parser.add_argument('-f', '--frameworks',
                        help='Frameworks to create conda envs.',
                        dest='frameworks',
                        default='',
                        required=False,
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
    cr = EnvCreator(args.frameworks, args.py, args.conda, args.branch)
    cr.create_envs()


if __name__=='__main__':
    sys.exit(main() or 0)