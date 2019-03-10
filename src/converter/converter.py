import os
import sys
import argparse
import config_parser
import subprocess
import platform
import logging as log

def build_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mo', type = str,
        required = True, help = 'Path to mo.py')
    parser.add_argument('-c', '--config', type = str,
        required = True, help = 'Path to xml file with config')
    mo = parser.parse_args().mo
    config = parser.parse_args().config
    if not os.path.isfile(mo):
        raise ValueError('Wrong path to model optimizer')
    if not os.path.isfile(config):
        raise ValueError('Wrong path to file with config')
    return mo, config


def converter(mo, conversion_list, log):
    python_type = ''
    os_type = platform.system()
    if os_type == 'Windows':
        python_type = 'python'
    elif os_type == 'Linux':
        python_type = 'python3'
    else:
        raise ValueError('OS type not supported')
    for i in range(len(conversion_list)):
        if conversion_list[i].additional_options == 'None':
            cmd = '{} {} --input_model {} --output_dir {}'.format(
                python_type, mo, conversion_list[i].modelfile,
                conversion_list[i].outdir)
        else:
            cmd = '{} {} --input_model {} --output_dir {} {}'.format(
                python_type, mo, conversion_list[i].modelfile,
                conversion_list[i].outdir,
                conversion_list[i].additional_options)
        log.info('Start converting the model with the command:\n    {}'.
            format(cmd))
        convert = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE,
            stderr = subprocess.PIPE, universal_newlines = True)
        convert.wait()
        if not convert.poll():
            log.info('Conversion successful')
        else:
            log.error('Conversion failed')
            log.error('Error logs:')
            for line in convert.stderr:
                print(line, end = '')

if __name__ == '__main__':
    try:
        log.basicConfig(format = '[ %(levelname)s ] %(message)s',
            level = log.INFO, stream = sys.stdout)
        mo, config = build_argparse()
        conversion_list = config_parser.process_config(config)
        log.info('Start converting {} models'.format(len(conversion_list)))
        converter(mo, conversion_list, log)
        log.info('End converting')
        log.info('Work is done!')
    except Exception as exp:
        log.warning(str(exp))