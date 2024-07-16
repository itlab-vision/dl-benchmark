import argparse
import sys
import traceback
from pathlib import Path
from model_readers import NNCFModelHandlerWrapper
from parameters import NNCFQuantParamReader, NNCFQuantizationProcess
sys.path.append(str(Path(__file__).resolve().parents[3]))
from src.utils.logger_conf import configure_logger  # noqa: E402
from src.quantization.utils import DatasetReader, ConfigParser, iter_log  # noqa: E402


log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='Path to xml config.',
                        type=str,
                        required=True,
                        dest='config')
    args = parser.parse_args()
    return args


def main():
    args = cli_argument_parser()
    try:
        parser = ConfigParser(args.config)
        data_reader = DatasetReader(log)
        quant_params = NNCFQuantParamReader(log)
        model_reader = NNCFModelHandlerWrapper(log)

        log.info('Parsing xml config')
        config = parser.parse()
        exit_code = 0
        for model_quant_config in config:
            try:
                model_reader.add_arguments(model_quant_config[0]['Model'])
                data_reader.add_arguments(model_quant_config[1]['Dataset'])
                quant_params.add_arguments(model_quant_config[2]['QuantizationParameters'])
                proc = NNCFQuantizationProcess(log, model_reader, data_reader, quant_params)
                iter_log(model_reader.dict_for_iter_log(),
                         data_reader.dict_for_iter_log(),
                         quant_params.dict_for_iter_log(),
                         log)
                proc.quantization_nncf()
                proc.save_quant_model()
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
