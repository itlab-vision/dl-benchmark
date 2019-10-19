import os
import platform
from subprocess import Popen, PIPE


def get_path_to_sync_scrypts():
    inference_folder = os.path.abspath('../inference')
    path_to_sync_scrypt = os.path.join(inference_folder, 'inference_sync_mode.py')
    return path_to_sync_scrypt


def get_path_to_async_scrypts():
    inference_folder = os.path.abspath('../inference')
    path_to_async_scrypt = os.path.join(inference_folder, 'inference_async_mode.py')
    return path_to_async_scrypt


def get_cmd_python_version():
    cmd_python_version = ''
    os_type = platform.system()
    if os_type == 'Linux':
        cmd_python_version = 'python3'
    else:
        cmd_python_version = 'python'
    return cmd_python_version


def add_extension_for_cmd_line(command_line, extension):
    return '{0} -l {1}'.format(command_line, extension)


def add_nthreads_for_cmd_line(command_line, nthreads):
    return '{0} -nthreads {1}'.format(command_line, nthreads)


def add_nstreams_for_cmd_line(command_line, nstreams):
    return '{0} -nstreams {1}'.format(command_line, nstreams)


def add_requests_for_cmd_line(command_line, requests):
    return '{0} -nstreams {1}'.format(command_line, requests)


def create_cmd_line_for_sync_test(model_xml, model_bin, dataset, batch, device,
                                extension, iteration, nthreads, min_inference_time):
    scrypt = get_path_to_sync_scrypts()
    python = get_cmd_python_version()
    command_line = '{0} {1} -m {2} -w {3} -i {4} -b {5} -d {6} -ni {7} -mi {8} \
        --raw_output true'.format(python, scrypt, model_xml, model_bin, dataset,
                                    batch, device, iteration, min_inference_time)
    if extension:
        command_line = add_extension_for_cmd_line(command_line, extension)
    if nthreads:
        command_line = add_nthreads_for_cmd_line(command_line, nthreads)
    return command_line



def create_cmd_line_for_async_test(model_xml, model_bin, dataset, batch, device,
                                extension, iteration, nthreads, nstreams, requests):
    scrypt = get_path_to_async_scrypts()
    python = get_cmd_python_version()
    command_line = '{0} {1} -m {2} -w {3} -i {4} -b {5} -d {6} -ni {7} \
        --raw_output true'.format(python, scrypt, model_xml, model_bin, dataset,
                                    batch, device, iteration)
    if extension:
        command_line = add_extension_for_cmd_line(command_line, extension)
    if nthreads:
        command_line = add_nthreads_for_cmd_line(command_line, nthreads)
    if nstreams:
        command_line = add_nstreams_for_cmd_line(command_line, nstreams)
    if requests:
        command_line = add_requests_for_cmd_line(command_line, requests)
    return command_line


def run_test(command_line, environment):
    test = Popen(command_line, env = environment, shell = True,
        stdout = PIPE, universal_newlines = True)
    return_code = test.wait()
    out, _ = test.communicate()
    out = out.split('\n')[:-1]
    return return_code, out


def print_error(out):
    iserror = False
    for line in out:
        if line.rfind('ERROR! :') != -1:
            iserror = True
            print('    {0}'.format(line[8:]))
            continue
        if iserror:
            print('    {0}'.format(line))


def parse_model_blob(out):
    return out[-1]


def parse_sync_output(out):
    result = out[-2].split(',')
    average_time = float(result[0])
    fps = float(result[1])
    latency = float(result[2])
    return average_time, fps, latency


def parse_async_output(out):
    result = out[-2].split(',')
    average_time = float(result[0])
    fps = float(result[1])
    return average_time, fps