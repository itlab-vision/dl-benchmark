from converter import TVMConverter


class TVMConverterTVMFormat(TVMConverter):
    def __init__(self, args):
        super().__init__(args)

    @property
    def source_framework(self):
        return super().source_framework

    def _get_deserialized_tvm_model(self):
        with open(self.model_params, 'rb') as fo:
            params = self.tvm.runtime.load_param_dict(fo.read())

        with open(self.model_path, 'r') as fo:
            mod = fo.read()

        self.mod = self.tvm.ir.load_json(mod)
        self.params = params
        return self.mod, self.params

    def _get_lib_format_tvm_model(self):
        lib = self.tvm.runtime.load_module(self.model_path)
        return lib

    def _get_vm_format_tvm_model(self):
        lib = self.tvm.runtime.load_module(self.model_path)
        code = bytearray(open(self.model_params, 'rb').read())
        return lib, code

    def _convert_model_from_framework(self):
        if self.mod_type == 'json' and self.params_type == 'params':
            return self._get_deserialized_tvm_model()
        elif ((self.mod_type == 'so' or self.mod_type == 'tar')
              and self.params_type is None):
            return [self._get_lib_format_tvm_model()]
        elif ((self.mod_type == 'so' or self.mod_type == 'tar')
              and self.params_type == 'ro'):
            return self._get_vm_format_tvm_model()
        else:
            raise ValueError('Wrong arguments.')
