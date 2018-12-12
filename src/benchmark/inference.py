import os
import sys
import logging as log

infer_path = os.path.dirname(os.path.abspath(__file__))
infer_path = infer_path[0:-9]
infer_path = os.path.join(infer_path, 'inference')
sys.path.append(infer_path)

import inference_async_mode as as_mode
import inference_sync_mode as s_mode

def test_async(model, dataset, param):
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    log.info('Start async inference test on model : {}'.format(model.name))
    try:
        images = []
        images.append(dataset.path)
        net, plugin, data = as_mode.prepare_model(log, model.model,
            model.weight, None, param.plugin, None, images)
        net.batch_size = param.batch_size
        images = as_mode.prepare_data(net, data)
        log.info('Loading model to the plugin')
        exec_net = plugin.load(network = net,
            num_requests = param.async_request)
        log.info('Starting inference ({} iterations)'.format(param.iteration))
        _, time = as_mode.infer_async(images, exec_net, net, param.iteration)
        log.info('End async inference test on model : {}'.format(model.name))
        del net
        del exec_net
        del plugin
        return time
    except Exception as ex:
        log.warning('Async inference test was ended with error:')
        print('{}'.format(str(ex)))

def test_sync(model, dataset, param):
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    log.info('Start sync inference test on model : {}'.format(model.name))
    try:
        images = []
        images.append(dataset.path)
        net, plugin, data = s_mode.prepare_model(model.model, model.weight,
            None, param.plugin, None, images, log)
        net.batch_size = param.batch_size
        images = s_mode.convert_image(net, data, log)
        _, time = s_mode.infer_sync(net, plugin, images, param.iteration, log)
        log.info('End sync inference test on model : {}'.format(model.name))
        del net
        del plugin
        return time
    except Exception as ex:
        log.warning('Sync inference test was ended with error:')
        print('{}'.format(str(ex)))