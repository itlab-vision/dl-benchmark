import platform
import subprocess
from collections import OrderedDict
from openvino.inference_engine import IECore  # pylint: disable=E0401


def get_cpu_name():
    ie = IECore()
    try:
        cpuname = ie.get_metric('CPU', 'FULL_DEVICE_NAME')
    except TypeError:
        cpuname = 'Undefined'
    del ie
    return cpuname


def get_gpu_name():
    ie = IECore()
    try:
        gpuname = ie.get_metric('GPU', 'FULL_DEVICE_NAME')
    except TypeError:
        gpuname = 'Undefined'
    del ie
    return gpuname


def get_ram_size(ostype):
    ramsize = 'Undefined'
    if (ostype == 'Windows'):
        command = ['wmic', 'OS', 'get', 'TotalVisibleMemorySize', '/Value']
        p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = p.stdout.read()
        p.wait()
        text = text.split('=')
        ramsize = text[1].strip() + ' KB'
    elif (ostype == 'Linux'):
        command = ['cat', '/proc/meminfo']
        all_info = subprocess.check_output(command).strip().decode()
        for line in all_info.split('\n'):
            if 'MemTotal' in line:
                return line.split(':')[1].strip()
    return ramsize


def get_system_characteristics():
    ostype = platform.system()
    characteristics = OrderedDict()
    characteristics.update({'CPU': get_cpu_name()})
    characteristics.update({'CPU family': platform.processor()})
    characteristics.update({'GPU': get_gpu_name()})
    characteristics.update({'RAM size': get_ram_size(ostype)})
    characteristics.update({'OS family': platform.system()})
    characteristics.update({'OS version': platform.platform()})
    characteristics.update({'Python version': platform.python_version()})
    return characteristics


if __name__ == '__main__':
    hardware_dict = get_system_characteristics()
    for key in hardware_dict:
        print('{}: {}'.format(key, hardware_dict[key]))
