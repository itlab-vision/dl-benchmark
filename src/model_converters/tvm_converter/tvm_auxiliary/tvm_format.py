import importlib
from pathlib import Path

Converter = importlib.import_module('src.model_converters.tvm_converter.tvm_auxiliary.converter').Converter


class TVMConverter(Converter):
    def __init__(self, args):
        super().__init__(args)
        self.framework = 'TVM'

    def _get_deserialized_tvm_model(self):
        model_path = self.args['model_path']
        model_params = self.args['model_params']
        with open(model_params, 'rb') as fo:
            params = self.tvm.relay.load_param_dict(fo.read())

        with open(model_path, 'r') as fo:
            mod = fo.read()

        self.mod = self.tvm.ir.load_json(mod)
        self.params = params
        return self.mod, self.params

    def _get_lib_format_tvm_model(self):
        lib = self.tvm.runtime.load_module(self.args['model_path'])
        return lib

    def _get_vm_format_tvm_model(self):
        lib = self.tvm.runtime.load_module(self.args['model_path'])
        code = bytearray(open(self.args['model_params'], 'rb').read())
        return lib, code

    def _convert_model_from_framework(self):
        model_name = self.args['model_path']
        params = self.args['model_params']

        self.mod_type = Path(model_name).suffix[1:]

        if params is not None and params != '':
            self.params_type = Path(params).suffix[1:]
        else:
            self.params_type = None

        if self.mod_type == 'json' and self.params_type == 'params':
            return self._get_deserialized_tvm_model()
        elif ((self.mod_type == 'so' or self.mod_type == 'tar')
              and self.params_type is None):
            return [self._get_lib_format_tvm_model()]
        elif self.mod_type == 'so' and self.params_type == 'ro':
            return self._get_vm_format_tvm_model()
        else:
            raise ValueError('Wrong arguments.')
