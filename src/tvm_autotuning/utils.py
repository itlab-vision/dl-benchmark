import tvm
from tvm import relay


def load_params(path):
    with open(path, "rb") as fo:
        params = relay.load_param_dict(fo.read())
    return params


def load_mod(path):
    with open(path, "r") as fo:
        mod = fo.read()

    return tvm.ir.load_json(mod)
