from .models.models import Models
from .data.data import Data
from .benchmark_config.benchmark_config import BenchmarkConfig
from .remote_config.remote_config import RemoteConfig
from .deploy_config.deploy_config import DeployConfig


class DataBase:
    def __init__(self):
        self.models = Models()
        self.data = Data()
        self.benchmark_config = BenchmarkConfig()
        self.remote_config = RemoteConfig()
        self.deploy_config = DeployConfig()
