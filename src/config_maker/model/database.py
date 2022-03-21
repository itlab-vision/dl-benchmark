from .models.models import Models  # pylint: disable=E0402
from .data.data import Data  # pylint: disable=E0402
from .benchmark_config.benchmark_config import BenchmarkConfig  # pylint: disable=E0402
from .accuracy_checker_config.accuracy_checker_config import AccuracyCheckerConfig  # pylint: disable=E0402
from .remote_config.remote_config import RemoteConfig  # pylint: disable=E0402
from .deploy_config.deploy_config import DeployConfig  # pylint: disable=E0402


class DataBase:
    def __init__(self):
        self.models = Models()
        self.data = Data()
        self.benchmark_config = BenchmarkConfig()
        self.accuracy_checker_config = AccuracyCheckerConfig()
        self.remote_config = RemoteConfig()
        self.deploy_config = DeployConfig()
