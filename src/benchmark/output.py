import os
import sys
sys.path.append('../auxiliary')
import node_info as info


def create_table(tablename):
    file = open(tablename, 'w')
    head = 'Model;Dataset;Batch size;Mode;Parameters;Infrastucture;Average time of single pass (s);Latency;FPS;'
    file.write(head + '\n')
    file.close()


def add_row_to_table(table, row):
    file = open(tablename, 'a')
    file.write(row + '\n')
    file.close()


def create_table_row(model, dataset, param, average_time, latency, fps):
    hardware = info.get_system_characteristics()
    hardware_info = ''
    for key in hardware:
        hardware_info += '{}: {}, '.format(key, hardware[key])
    hardware_info = hardware_info[:-2]
    other_param = 'Plugin: {}, Async request count: {}, Iteration count: {}, Min inference time: {}'.format(param.plugin,
        param.async_request, param.iteration, param.min_inference_time)
    table_row = '{};{};{};{};{};{};{};{};{};'.format(model.name, dataset.name,
        param.batch_size, param.mode, other_param, hardware_info, average_time,
        latency, fps)
    return table_row