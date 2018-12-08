import sys
import logging as log

sys.path.append('E:\ITlab\openvino-dl-benchmark\src\inference')

import inference_async_mode as as_mode
import inference_sync_mode as s_mode

def test_async(model, dataset, params):
    log.basicConfig(format = "[ %(levelname)s ] %(message)s",
        level = log.INFO, stream = sys.stdout)
    log.info("Start async inference test on model : {}".format(model.name))
    net, plugin, data = as_mode.prepare_model(log, model.model, model.weigh,
        None, params.plugin, None, dataset.path)
    net.batch_size = params.batchsize
    images = as_mode.prepare_data(net, data)
    log.info("Loading model to the plugin")
    exec_net = plugin.load(network = net, num_requests = params.asyncrequest)
    log.info("Starting inference ({} iterations)".format(params.iteration))
    _, time = as_mode.infer_async(images, exec_net, net, params.iteration)
    log.info("End async inference test on model : {}".format(model.name))
    return time

def test_sync(model, dataset, params):
    log.basicConfig(format = "[ %(levelname)s ] %(message)s",
        level = log.INFO, stream = sys.stdout)
    log.info("Start sync inference test on model : {}".format(model.name))
    net, plugin = s_mode.prepare_model(model.model, model.weigh,
        None, params.plugin, None, dataset.path, log)
    print('Ok')
    images = s_mode.convert_image(net, dataset.path, log)
    print('Ok')
    _, time = s_mode.infer_sync(net, plugin, images, params.iteration, log)
    log.info("End sync inference test on model : {}".format(model.name))
    return time