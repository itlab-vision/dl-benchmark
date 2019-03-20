import os
import platform
import subprocess


def get_cpu_name(ostype):
    cpuname = 'Underfined'
    if (ostype == 'Windows'):
        command = ['wmic', 'cpu', 'get', 'name', '/Value']
        p = subprocess.Popen(command, universal_newlines = True, shell = True,
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        text = p.stdout.read()
        p.wait()
        text = text.split('=')
        cpuname = text[1].strip()
    elif (ostype == 'Linux'):
        command = ['cat', '/proc/cpuinfo']
        cpu_info = subprocess.check_output(command).strip().decode()
        for line in cpu_info.split('\n'):
            if 'model name' in line:
                return line.split(':')[1].strip()
    elif (ostype == 'Darwin'):
        # TODO : write code for Mac OS
        #'sysctl -n machdep.cpu.brand_string'
        cpuname = 'Underfined Macintosh CPU'
    return cpuname


def get_gpu_name(ostype):
    gpuname = 'Underfined'
    if (ostype == 'Windows'):
        import wmi
        computer = wmi.WMI()
        gpu_info = computer.Win32_VideoController()
        for eachitem in gpu_info:
            if 'Graphics' in eachitem.Name:
                gpuname = eachitem.Name
    elif (ostype == 'Linux'):
        # TODO : write code for Linux
        command = 'hwinfo --short'
        gpu_info = subprocess.check_output(command).strip().decode()
        for line in cpu_info.split('\n'):
            if 'Graphics' in line:
                return line.strip()
    elif (ostype == 'Darwin'):
        # TODO : write code for Mac OS
        gpuname = 'Underfined GPU'
    return gpuname


def get_ram_size(ostype):
    ramsize = 'Underfined'
    if (ostype == 'Windows'):
        command = ['wmic', 'OS', 'get', 'TotalVisibleMemorySize', '/Value']
        p = subprocess.Popen(command, universal_newlines = True, shell = True, 
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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
    characteristics = {}
    ostype = platform.system()
    characteristics.update({'CPU' : get_cpu_name(ostype)})
    characteristics.update({'CPU family' : platform.processor()})
    characteristics.update({'GPU' : get_gpu_name(ostype)})
    characteristics.update({'RAM size' : get_ram_size(ostype)})
    characteristics.update({'OS family' : platform.system()})
    characteristics.update({'OS version' : platform.platform()})
    characteristics.update({'Python version' : platform.python_version()})
    return characteristics


if __name__ == '__main__':
    print(get_system_characteristics())