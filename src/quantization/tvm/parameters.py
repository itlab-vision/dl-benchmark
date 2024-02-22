import tvm
import abc

class TVMReader(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self._log = log
    
    def add_arguments(self, args):
        self.args = args
        self._get_arguments()
    
    @abc.abstractmethod
    def _get_arguments(self):
        pass


class TVMDatasetReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)
    
    def _get_arguments(self):
        self.dataset_name = self.args['DatasetName']
        self.dataset_path = self.args['DatasetPath']
        self.mean = self.args['Mean']
        self.std = self.args['Std']
        self.image_size = self.args['ImageSize']
    

class TVMModelReader(TVMReader):
    def __init__(self, log):
        super().__init__(log)
    
    def _get_arguments(self):
        self.model_path = self.args['ModelJson']
        self.model_params = self.args['WeightsParams']
        self.batch = self.args['BatchSize']

    def _read_model(self):
        with open(self.model_params, 'rb') as fo:
            params = tvm.relay.load_param_dict(fo.read())

        with open(self.model_path, 'r') as fo:
            mod = fo.read()

        self.mod = self.tvm.ir.load_json(mod)
        self.params = params


class TVMQuantParamReader:
    def __init__(self, args):
        pass