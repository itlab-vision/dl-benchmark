import os
import sys

auxiliary_path = os.path.dirname(os.path.abspath(__file__))
auxiliary_path = auxiliary_path[0:-9]
auxiliary_path = os.path.join(auxiliary_path, 'auxiliary')
sys.path.append(auxiliary_path)

import node_info as info

def create_table_row(model, dataset, param, average_time, latency, fps):
    hardware = info.get_system_characteristics()
    hardware_info = ''
    for key in hardware:
        hardware_info += '{}: {}, '.format(key, hardware[key])
    hardware_info = hardware_info[:-2]
    other_param = 'Plugin: {}, Async request count: {}, Iteration count: {}, Min inference time: {}'.format(param.plugin,
        param.asyncrequest, param.iteration, param.mininferencetime)
    table_row = '{};{};{};{};{};{};{};{};{};'.format(model.name, dataset.name,
        param.batchsize, param.mode, other_param, hardware_info, average_time,
        latency, fps)
    return table_row

def save_table(table):
    file = open('results.csv', 'w')
    head = 'Model;Dataset;BatchSize;Mode;Parameters;Infrastucture;Average time of single pass (s);Latency;FPS'
    file.write(head + '\n')
    for line in range(len(table)):
        file.write(table[line] + '\n')
    file.close()