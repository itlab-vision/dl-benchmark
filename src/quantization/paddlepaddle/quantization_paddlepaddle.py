import argparse
import sys
import traceback
from pathlib import Path
from ...utils.logger_conf import configure_logger  # noqa: E402
from ...quantization.utils import ConfigParser  # noqa: E402
from paddleslim.quant import quant_post_static
import paddle
from paddle.io import DataLoader
from parameters import PaddleModelReader, ImageNetDataset
import ast

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
        for model_quant_config in config:
            try:
                paddle.enable_static()
                place = paddle.CPUPlace()
                exe = paddle.static.Executor(place)
                val_dataset = (
                    ImageNetDataset(mode='test',
                                    crop_size=ast.literal_eval(model_quant_config[1]['Dataset']['CropResolution']),
                                    resize_size=ast.literal_eval(model_quant_config[1]['Dataset']['ImageResolution']),
                                    data_dir=model_quant_config[1]['Dataset']['Path']))

                image_shape = ast.literal_eval(model_quant_config[2]['Parameters']['InputShape'])
                image = paddle.static.data(
                    name=model_quant_config[2]['Parameters']['InputName'], shape=[None] + image_shape, dtype='float32')

                data_loader = DataLoader(
                    val_dataset,
                    places=place,
                    feed_list=[image],
                    drop_last=False,
                    return_list=False,
                    batch_size=32,
                    shuffle=False)

                quant_post_static(
                    executor=exe,
                    model_dir=model_quant_config[0]['Model']['ModelDir'],
                    quantize_model_path=model_quant_config[2]['Parameters']['SaveDir'],
                    data_loader=data_loader,
                    model_filename=model_quant_config[0]['Model']['ModelFileName'],
                    params_filename=model_quant_config[0]['Model']['ParamsFileName'],
                    batch_size=int(model_quant_config[1]['DataSet']['BatchSize']),
                    batch_nums=10,
                    algo='avg',
                    round_type='round',
                    hist_percent=0.9999,
                    is_full_quantize=False,
                    bias_correction=False,
                    onnx_format=False)

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
