import os
import argparse
import config_parser


def build_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mo', type = str,
        dest = 'mo', help = 'Path to model optimizer')
    parser.add_argument('-c', '--config', type = str,
        dest = 'config', help = 'Path to file with config')
    mo = parser.parse_args().mo
    config = parser.parse_args().config
    if (mo is None) or (not os.path.isfile(mo)):
        raise ValueError('Wrong path to model optimizer')
    if (config is None) or (not os.path.isfile(config)):
        raise ValueError('Wrong path to file with config')
    return mo, config


def converter(mo, conversion_list):
    i = 0
    while i < len(conversion_list):
        if conversion_list[i].additional_options is None:
            command = 'python {} --input_model {} --output_dir {}'.format(mo,
                conversion_list[i].modelfile, conversion_list[i].outdir)
        else:
            command = 'python {} --input_model {} --output_dir {} {}'.format(mo,
                conversion_list[i].modelfile, conversion_list[i].outdir,
                conversion_list[i].additional_options)
        os.system(command)
        i += 1


if __name__ == '__main__':
    try:
        mo, config = build_argparse()
        conversion_list = configparse.process_config(config)
        converter(mo, conversion_list)
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
