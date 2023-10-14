import tvm
import logging as log
from scipy.special import softmax


class TVMConverter:
    def __init__(self, args):
        self.args = args
        self.net = None
    
    def _get_target_device(self):
        if self.args['device'] == 'CPU':
            target = tvm.target.Target('llvm')
            dev = tvm.cpu(0)
        return target, dev

    def convert_model_from_framework(self, framework):
        
        target, dev = self._get_target_device()

        if framework == 'mxnet':
            import mxnet, gluoncv
            if self.args['device'] == 'CPU':
                context = mxnet.cpu()
            model_name = self.args['model_name']
            log.info(f'Loading network \"{model_name}\" from GluonCV model zoo')
            net = gluoncv.model_zoo.get_model(model_name, pretrained=True, ctx=context)
            shape_dict = {self.args['input_name']: self.args['input_shape']}
            model, params = tvm.relay.frontend.from_mxnet(net, shape_dict)
            with tvm.transform.PassContext(opt_level=3):
                lib = tvm.relay.build(model, target=target, params=params)
            module = tvm.contrib.graph_executor.GraphModule(lib["default"](dev))
            return module
        
        elif framework == 'pytorch':
            import torch, torchvision
            model_name = self.args['model_name']
            pt_model = getattr(torchvision.models, model_name)(pretrained=True)
            pt_model = pt_model.eval()
            input_shape = self.args['input_shape']
            input_data = torch.randn(input_shape)
            scripted_model = torch.jit.trace(pt_model, input_data).eval()
            input_name = self.args['input_name']
            shape_list = [(input_name, input_shape)]
            model, params = tvm.relay.frontend.from_pytorch(scripted_model, shape_list)
            with tvm.transform.PassContext(opt_level=3):
                lib = tvm.relay.build(model, target=target, params=params)
            module = tvm.contrib.graph_executor.GraphModule(lib["default"](dev))
            return module
        
        elif framework == 'onnx':
            import onnx
            model_path = self.args['model_name']
            model_onnx = onnx.load(model_path)
            shape_dict = {self.args['input_name']: self.args['input_shape']}
            model, params = tvm.relay.frontend.from_onnx(model_onnx, shape_dict)
            with tvm.transform.PassContext(opt_level=3):
                lib = tvm.relay.build(model, target=target, params=params)
            module = tvm.contrib.graph_executor.GraphModule(lib["default"](dev))
            return module






def create_dict_for_converter_mxnet(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'device': args.device,
    }
    return dictionary


def create_dict_for_transformer(args):
    dictionary = {
        'channel_swap': args.channel_swap,
        'mean': args.mean,
        'std': args.std,
        'norm': args.norm,
        'input_shape': args.input_shape,
        'batch_size': args.batch_size,
    }
    return dictionary


def create_dict_for_modelwrapper(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
    }
    return dictionary


def prepare_output(result, task, output_names):
    if task == 'feedforward':
        return {}
    if task == 'classification':
        return {output_names[0]: softmax(result.asnumpy())}
    


        