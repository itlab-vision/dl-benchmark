import platform
import os
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
    
    ## Collect CPU information
    # CPU name
    characteristics.update({'CPU' : get_cpu_name(ostype)})
    # CPU family
    characteristics.update({'CPU_family' : platform.processor()})
    
    ## Collect RAM information
    # RAM size
    characteristics.update({'RAM_size' : get_ram_size(ostype)})
    
    ## Collect OS information 
    # OS family
    characteristics.update({'OS_family' : platform.system()})
    # OS platform
    characteristics.update({'OS_version' : platform.platform()})
    
    ## Collect Python information
    # Python version
    characteristics.update({'Python_version' : platform.python_version()})
    
    return characteristics


if __name__ == '__main__':
    print(get_system_characteristics())
