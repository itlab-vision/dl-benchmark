import sys
import argparse
import logging as log
from process import process
from utils import get_all_downloaded_public_models_in_dir

import traceback


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--batch_sizes',
        help='Batches to convert models',
        type=int, nargs='+', default = [1]
    )
    parser.add_argument(
        '-d', '--dir',
        help='Root directory where to store converter models ',
        type=str, default='./'
    )
    parser.add_argument(
        '-z', '--zoo_config_dir',
        help='Directory where public models config plased',
        default=''
    )
    config = parser.parse_args()
    return config


def model_conversion(params, log):
    models_list = get_all_downloaded_public_models_in_dir(params.dir)
    log.info(f'List of models to convert {models_list}')
    for model in models_list:
        log.info(f'Start conversion model {model}')
        for batch in params.batch_sizes:
            convert_process = process(model, batch, params, log)
            convert_process.execute()
        log.info(f'End conversion model {model}!')


def main():
    log.basicConfig(
        format='[ %(levelname)s][%(filename)s %(lineno)s] %(message)s',
        level=log.INFO,
        stream=sys.stdout
    )
    conversion_parameters = build_argparser()

    try:
        log.info('Start conversion on')
        model_conversion(conversion_parameters, log)
        log.info('End conversion!')
    except Exception as exp:
        log.error(str(exp))
        traceback.print_exc()


if __name__ == '__main__':
    sys.exit(main() or 0)
