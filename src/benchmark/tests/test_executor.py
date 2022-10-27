import sys
import re
import logging as log
import psutil
import pytest
from src.benchmark.executors import Executor, HostExecutor, DockerExecutor

log.basicConfig(
    format='[ %(levelname)s ] %(message)s',
    level=log.INFO,
    stream=sys.stdout,
)


class MockContainer:
    """A fake Docker API container object."""

    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.args = args
        self.kwargs = kwargs

    def exec_run(self, *args, **kwargs):    # noqa
        return 0, 'test: test\ntest: test\ntest: test'.encode('utf-8')


class MockContainersApi:
    """A fake Docker API with containers calls."""

    def __init__(self, containers_names=None):
        self.names = containers_names

    def run(self, *args, **kwargs):
        return MockContainer(*args, **kwargs)

    def list(self):     # noqa
        if self.names:
            return [MockContainer(name=name) for name in self.names]
        return []


class MockDockerApi:
    """A fake Docker API."""

    def __init__(self, containers_names=None):
        self.containers = MockContainersApi(containers_names)


def get_host_executor(mocker):
    return HostExecutor(log)


def get_docker_executor(mocker):
    mocker.patch('docker.from_env', return_value=MockDockerApi(['test_target_framework']))
    executor = DockerExecutor(log)
    executor.my_target_framework = 'test_target_framework'
    return executor


@pytest.mark.parametrize('executor_type', [['host_machine', HostExecutor], ['docker_container', DockerExecutor]])
def test_get_executor(executor_type, mocker):
    mocker.patch('docker.from_env', return_value=MockDockerApi())
    assert isinstance(Executor.get_executor(executor_type[0], log), executor_type[1])


@pytest.mark.parametrize('executor_type', ['test_str_1', 'test_str_2'])
def test_get_wrong_executor(executor_type, mocker):
    mocker.patch('docker.from_env', return_value=MockDockerApi())
    assert Executor.get_executor(executor_type, log) is None


@pytest.mark.parametrize('executor_instance', [get_host_executor, get_docker_executor])
def test_target_framework(executor_instance, mocker):
    ex = executor_instance(mocker)
    ex.set_target_framework('OpenVINO DLDT')
    assert ex.my_target_framework == 'OpenVINO_DLDT'


@pytest.mark.parametrize('executor_instance', [get_host_executor, get_docker_executor])
def test_infrastructure(executor_instance, mocker):
    ex = executor_instance(mocker)
    if isinstance(ex, HostExecutor):
        assert re.match(r'CPU: .* CPU family: .* GPU: .* RAM size: .* OS family: .* OS version: .* Python version: .*',
                        ex.get_infrastructure())
    else:
        assert ex.get_infrastructure() == 'test: test'


@pytest.mark.parametrize('executor_instance', [get_host_executor, get_docker_executor])
def test_execute_process(executor_instance, mocker):
    ex = executor_instance(mocker)
    if isinstance(ex, HostExecutor):
        assert ex.execute_process(command_line='echo -n test | md5sum',
                                  timeout=999)[1][0] == '098f6bcd4621d373cade4e832627b4f6  -\n'
    else:
        assert ex.execute_process(command_line='test docker', _=None) == (0, b'test: test\ntest: test\ntest: test')


@pytest.mark.parametrize('executor_instance', [get_host_executor, get_docker_executor])
def test_execute_process_timeout(executor_instance, mocker, caplog):
    ex = executor_instance(mocker)
    if isinstance(ex, HostExecutor):
        ex.execute_process(command_line='sleep 5', timeout=0.01)
        assert re.match(r'.*Timeout .* is reached, terminating.*', caplog.text)


def test_process_kill_fail(mocker):
    ex = get_host_executor(mocker)
    with pytest.raises(psutil.NoSuchProcess):
        ex.kill_process(99999)
