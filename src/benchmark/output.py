import os
import sys
sys.path.append(os.path.abspath('../auxiliary'))
import node_info as info
from collections import OrderedDict


def create_table(tablename):
    file = open(tablename, 'w')
    head = 'Status;Task type;Topology name;Framework;Input blob sizes;Weight type;Batch size;Mode;Parameters;Infrastructure;Average time of single pass (s);Latency;FPS;'
    file.write(head + '\n')
    file.close()


def add_row_to_table(tablename, row):
    file = open(tablename, 'a')
    file.write(row + '\n')
    file.close()


def create_table_row(status, model, dataset, param, blob_size, average_time, latency, fps):
    hardware = info.get_system_characteristics()
    hardware_info = ''
    for key in hardware:
        hardware_info += '{}: {}, '.format(key, hardware[key])
    hardware_info = hardware_info[:-2]
    parameters = OrderedDict()
    parameters.update({'Device' : param.device})
    parameters.update({'Async request count' : param.async_request})
    parameters.update({'Iteration count' : param.iteration})
    parameters.update({'Thread count' : param.nthreads})
    parameters.update({'Stream count' : param.nstreams})
    parameters.update({'Min inference time(s)' : param.min_inference_time})
    other_param = ''
    for key in parameters:
        if key == 'Min inference time(s)' and parameters[key] == 0.0:
            continue
        if parameters[key] != None:
            other_param += '{}: {}, '.format(key, parameters[key])
    other_param = other_param[:-2]
    if status == 'Failed':
        average_time = '-'
        latency = '-'
        fps = '-'
    table_row = '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};'.format(
        status, model.task, model.name, dataset.name, blob_size, model.datatype,
        param.batch_size, param.mode, other_param, hardware_info, average_time,
        latency, fps)
    return table_row