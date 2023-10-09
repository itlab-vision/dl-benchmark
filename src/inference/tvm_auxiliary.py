import tvm
import logging as log
from scipy.special import softmax


class TVMConverter:
    def __init__(self, args):
        self.args = args
        self.net = None
    
    def convert_model_from_framework(self):
        if self.args['framework'] == 'mxnet':
            import mxnet, gluoncv
            if self.args['device'] == 'CPU':
                context = mxnet.cpu()
                target = 'llvm'
                dev = tvm.device(target, 0)
            model_name = self.args['model_name']
            log.info(f'Loading network \"{model_name}\" from GluonCV model zoo')
            net = gluoncv.model_zoo.get_model(model_name, pretrained=True, ctx=context)
            shape_dict = {self.args['input_name']: self.args['input_shape']}
            model, params = tvm.relay.frontend.from_mxnet(net, shape_dict)
            with tvm.transform.PassContext(opt_level=3):
                lib = tvm.relay.build(model, target=target, params=params)
            module = tvm.contrib.graph_executor.GraphModule(lib["default"](dev))
            return module


def create_dict_for_converter(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'framework': args.framework,
        'device': args.device,
    }
    return dictionary


def prepare_output(result, task, output_names):
    if task == 'classification':
        return {output_names[0]: softmax(result.numpy())}
    


        