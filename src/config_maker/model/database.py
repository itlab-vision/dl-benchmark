from .accuracy_checker_config.accuracy_checker_config import AccuracyCheckerConfig
from .benchmark_config.benchmark_config import BenchmarkConfig
from .data.data import Data
from .deploy_config.deploy_config import DeployConfig
from .models.models import Models
from .remote_config.remote_config import RemoteConfig
from .quantization_config.quantization_config import QuantizationConfig


class DataBase:
    def __init__(self):
        self.models = Models()
        self.data = Data()
        self.benchmark_config = BenchmarkConfig()
        self.accuracy_checker_config = AccuracyCheckerConfig()
        self.remote_config = RemoteConfig()
        self.deploy_config = DeployConfig()
        self.quantization_config = QuantizationConfig()
