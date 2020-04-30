import os
import sys
sys.path.append(os.path.abspath('../auxiliary'))
import node_info as info
from collections import OrderedDict


def create_table(tablename):
    file = open(tablename, 'w')
    head = 'Status;Task type;Topology name;Dataset;Framework;Inference Framework;Input blob sizes;Weight type;Batch size;Mode;Parameters;Infrastructure;Average time of single pass (s);Latency;FPS'
    file.write(head + '\n')
    file.close()


def add_row_to_table(tablename, row):
    file = open(tablename, 'a')
    file.write(row + '\n')
    file.close()


def create_table_row(status, model, dataset, indep_param, dep_param, framework, input_shape, average_time, latency, fps):
    hardware = info.get_system_characteristics()
    hardware_info = ''
    for key in hardware:
        hardware_info += '{}: {}, '.format(key, hardware[key])
    hardware_info = hardware_info[:-2]
    parameters = OrderedDict()
    parameters.update({'Device' : indep_param.device})
    parameters.update({'Async request count' : dep_param.async_request})
    parameters.update({'Iteration count' : indep_param.iteration})
    parameters.update({'Thread count' : dep_param.nthreads})
    parameters.update({'Stream count' : dep_param.nstreams})
    parameters.update({'Min inference time(s)' : 0})
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
    table_row = '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14}'.format(
        status, model.task, model.name, dataset.name, framework, framework, input_shape,
        model.datatype, indep_param.batch_size, dep_param.mode, other_param, hardware_info,
        average_time, latency, fps)
    return table_row