import argparse
import sys
import traceback
from pathlib import Path
from ...utils.logger_conf import configure_logger  # noqa: E402
from ...quantization.utils import ConfigParser  # noqa: E402
from parameters import PaddleModelReader, PaddleDatasetReader, PaddleQuantizationProcess, PaddleQuantParamReader

sys.path.append(str(Path(__file__).resolve().parents[3]))

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='Path to the configuration file in the xml-format.',
                        type=str,
                        required=True,
                        dest='config')
    args = parser.parse_args()
    return args


def main():
    args = cli_argument_parser()
    try:
        log.info(f'Parsing the configuration file {args.config}')
        parser = ConfigParser(args.config)

        config = parser.parse()
        exit_code = 0
        quant_params = PaddleQuantParamReader(log)
        model_reader = PaddleModelReader(log)
        for model_quant_config in config:
            try:
                data_reader = PaddleDatasetReader(model_quant_config[1]['Dataset'])
                model_reader.add_arguments(model_quant_config[0]['Model'])
                quant_params.add_arguments(model_quant_config[2]['QuantizationParameters'])
                proc = PaddleQuantizationProcess(log, model_reader, data_reader, quant_params)
                proc.quantization_tflite()

            except Exception:
                log.error(traceback.format_exc())
                exit_code += 1
        if exit_code:
            sys.exit(1)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
