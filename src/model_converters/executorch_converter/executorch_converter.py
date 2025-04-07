import sys
import argparse
import traceback
import os
import torch
from pathlib import Path
from torchvision.models import get_model, list_models
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner
from executorch.backends.vulkan.partitioner.vulkan_partitioner import VulkanPartitioner
from executorch.exir import to_edge_transform_and_lower

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from utils.logger_conf import configure_logger  # noqa: E402

log = configure_logger()

PARTITIONER = {
    'xnnpack': XnnpackPartitioner(),
    'vulkan': VulkanPartitioner(),
    'None': None,
}


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-mn', '--model_name',
                        help='Model name from the module.',
                        required=True,
                        type=str,
                        dest='model_name')
    parser.add_argument('-w', '--weights',
                        help='Name of weights to use from module.',
                        type=str,
                        default='DEFAULT',
                        dest='weights')
    parser.add_argument('-is', '--input_shapes',
                        help='Input tensor shapes.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shapes')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-p', '--partitioner',
                        help='Partitioner to export model.',
                        default='None',
                        choices=['xnnpack', 'vulkan', 'arm', None],
                        type=str,
                        dest='partitioner')
    parser.add_argument('--print_list_of_models',
                        help='Flag to print all available models.',
                        action='store_true',
                        dest='model_print')
    parser.add_argument('-o', '--output_dir',
                        help='Directory to save converted model.',
                        type=str,
                        default='',
                        dest='output_dir')
    args = parser.parse_args()

    return args


def export_to_executorch(model_name, weights, batch,
                         input_shape, partitioner, output_path):
    log.info(f'Getting the model {model_name} from torchvision.')
    model = get_model(model_name, weights=weights)
    model = model.eval()
    sample_inputs = (torch.randn(list(input_shape)), )

    log.info('Export model to ExecuTorch format.')
    et_program = to_edge_transform_and_lower(
        torch.export.export(model, sample_inputs),
        partitioner=PARTITIONER[partitioner],
    ).to_executorch()

    if output_path == '':
        output_path = os.getcwd()
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    save_name = f'{model_name}_{partitioner}_batch_{batch}.pte'
    log.info(f'Save model as {save_name} into {output_path}.')
    with open(f'{output_path}/{save_name}', 'wb') as file:
        et_program.write_to_file(file)


def main():
    try:
        log.info('Parsing command line arguments.')
        args = cli_argument_parser()
        if args.model_print:
            log.info(f'Available models: {list_models()}')
        export_to_executorch(args.model_name, args.weights, args.batch_size,
                             args.input_shapes, args.partitioner, args.output_dir)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
