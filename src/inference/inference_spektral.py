import argparse
import json
import logging as log
import sys
from pathlib import Path

import pandas as pd
import spektral
from spektral.data import SingleLoader, BatchLoader, Dataset
from spektral.utils.io import load_binary
import tensorflow as tf

import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from reporter.report_writer import ReportWriter


TUDATASETS = ['tudataset_' + dst for dst in [
              'AIDS', 'alchemy_full', 'aspirin', 'benzene', 'BZR',
              'BZR_MD', 'COX2', 'COX2_MD', 'DHFR', 'DHFR_MD', 'ER_MD', 'ethanol', 'FRANKENSTEIN',
              'malonaldehyde', 'MCF-7', 'MCF-7H', 'MOLT-4', 'MOLT-4H', 'Mutagenicity', 'MUTAG',
              'naphthalene', 'NCI1', 'NCI109', 'NCI-H23', 'NCI-H23H', 'OVCAR-8', 'OVCAR-8H',
              'P388', 'P388H', 'PC-3', 'PC-3H', 'PTC_FM', 'PTC_FR', 'PTC_MM', 'PTC_MR', 'QM9',
              'salicylic_acid', 'SF-295', 'SF-295H', 'SN12C', 'SN12CH', 'SW-620', 'SW-620H',
              'toluene', 'Tox21_AhR_training', 'Tox21_AhR_testing', 'Tox21_AhR_evaluation',
              'Tox21_AR_training', 'Tox21_AR_testing', 'Tox21_AR_evaluation', 'Tox21_AR-LBD_training',
              'Tox21_AR-LBD_testing', 'Tox21_AR-LBD_evaluation', 'Tox21_ARE_training', 'Tox21_ARE_testing',
              'Tox21_ARE_evaluation', 'Tox21_aromatase_training', 'Tox21_aromatase_testing',
              'Tox21_aromatase_evaluation', 'Tox21_ATAD5_training', 'Tox21_ATAD5_testing',
              'Tox21_ATAD5_evaluation', 'Tox21_ER_training', 'Tox21_ER_testing', 'Tox21_ER_evaluation',
              'Tox21_ER-LBD_training', 'Tox21_ER-LBD_testing', 'Tox21_ER-LBD_evaluation',
              'Tox21_HSE_training', 'Tox21_HSE_testing', 'Tox21_HSE_evaluation', 'Tox21_MMP_training',
              'Tox21_MMP_testing', 'Tox21_MMP_evaluation', 'Tox21_p53_training', 'Tox21_p53_testing',
              'Tox21_p53_evaluation', 'Tox21_PPAR-gamma_training', 'Tox21_PPAR-gamma_testing',
              'Tox21_PPAR-gamma_evaluation', 'UACC257', 'UACC257H', 'uracil', 'Yeast', 'YeastH', 'ZINC_full',
              'ZINC_test', 'ZINC_train', 'ZINC_val', 'DD', 'ENZYMES', 'KKI', 'OHSU', 'Peking_1', 'PROTEINS',
              'PROTEINS_full', 'COIL-DEL', 'COIL-RAG', 'Cuneiform', 'Fingerprint', 'FIRSTMM_DB', 'Letter-high',
              'Letter-low', 'Letter-med', 'MSRC_9', 'MSRC_21', 'MSRC_21C', 'COLLAB', 'dblp_ct1', 'dblp_ct2',
              'DBLP_v1', 'deezer_ego_nets', 'facebook_ct1', 'facebook_ct2', 'github_stargazers',
              'highschool_ct1', 'highschool_ct2', 'IMDB-BINARY', 'IMDB-MULTI', 'infectious_ct1',
              'infectious_ct2', 'mit_ct1', 'mit_ct2', 'REDDIT-BINARY', 'REDDIT-MULTI-5K', 'REDDIT-MULTI-12K',
              'reddit_threads', 'tumblr_ct1', 'tumblr_ct2', 'twitch_egos', 'TWITTER-Real-Graph-Partial',
              'COLORS-3', 'SYNTHETIC', 'SYNTHETICnew', 'Synthie', 'TRIANGLES']]


class CustomDataset(Dataset):
    def __init__(self, gpath, **kwargs):
        self.graph_path = gpath

        super().__init__(**kwargs)

    def download(self):
        pass

    def read(self):
        output = []
        output.append(load_binary(self.graph_path))
        return output


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to a .keras file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-i', '--input',
                        help='Dataset or .bin file to import',
                        required=True,
                        type=str,
                        dest='input')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'sp_inference_report.json',
                        dest='report_path')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on '
                             '(Modern Tensorflow doesnt support anything but CPU)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--time',
                        help='Time in seconds to execute topology.',
                        required=False,
                        default=0,
                        type=int,
                        dest='time')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: turn to Node-Feature table',
                        choices=['node-classification', 'graph-classification'],
                        default='node-classification',
                        type=str,
                        dest='task')
    args = parser.parse_args()

    return args


def prepare_input_loader(input_, batch_size):
    file_type = str(input_).split('.')[-1]
    if file_type != 'bin':
        if input_ in ['cora', 'citeseer', 'pubmed']:
            dataset = spektral.datasets.citation.Citation(input_)
        elif input_ in ['ppi', 'reddit']:
            dataset = spektral.datasets.graphsage.GraphSage(input_)
        elif input_ == 'dblp':
            dataset = spektral.datasets.dblp.DBLP()
        elif input_ == 'flickr':
            dataset = spektral.datasets.flickr.Flickr()
        elif input_ == 'qm7':
            dataset = spektral.datasets.qm7.QM7()
        elif input_ == 'qm9':
            dataset = spektral.datasets.qm9.QM9()
        elif input_ == 'mnist':
            dataset = spektral.datasets.mnist.MNIST()
        elif input_ in ['modelnet10', 'modelnet40']:
            dataset = spektral.datasets.modelnet.ModelNet(input_[8:])
        elif input_ in TUDATASETS:
            dataset = spektral.datasets.TUDataset(input_[10:])
        else:
            raise ValueError('Attemting to import unsopported dataset.')
    else:
        dataset = CustomDataset(input_)

    if batch_size == 1:
        input_loader = SingleLoader(dataset)
    else:
        input_loader = BatchLoader(dataset, batch_size=batch_size)

    return input_loader


def process_output(result, task):
    if task == 'node-classification':
        _result = result.numpy()
        __result = {'Node': []}

        for i in range(1, len(_result[0]) + 1):
            __result['Feature ' + str(i)] = []

        for i in range(len(_result)):
            __result['Node'].append(i)
            for j in range(len(_result[0])):
                __result['Feature ' + str(j + 1)].append(_result[i][j])

        pd_result = pd.DataFrame(__result)
        pd.set_option('display.max_rows', 20)

        return pd_result


def model_load(model_path):
    log.info(f'Loading network files:\n\t {model_path}')
    file_type = str(model_path).split('.')[-1]
    if file_type != 'keras':
        raise ValueError('Only .keras model save file type is supported.')
    compiled_model = tf.keras.saving.load_model(model_path, compile=True)

    return compiled_model


def inference_spektral(model, number_iter, input_loader, test_duration):
    result = None
    time_infer = []
    log.info(f'Starting inference ({number_iter} iterations)')

    if number_iter == 1:
        slice_input, _ = input_loader.__next__()
        result, exec_time = infer_slice(model, slice_input)
        time_infer.append(exec_time)
    else:
        time_infer = loop_inference(number_iter, test_duration)(inference_iteration)(input_loader, model)
    log.info('Inference completed')

    return result, time_infer


def inference_iteration(input_loader, model):
    slice_input, _ = input_loader.__next__()
    _, exec_time = infer_slice(model, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(model, slice_input):
    res = model(slice_input, training=False)
    return res


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = cli_argument_parser()

    if args.device != 'CPU':
        log.warning('Modern Tensorflow required for Spektral supports only CPU. Device will be switched.')
        args.device = 'CPU'

    report_writer = ReportWriter()
    report_writer.update_framework_info(name='Spektral', version=spektral.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)

    input_loader = prepare_input_loader(args.input, args.batch_size)

    model = model_load(Path(args.model_path))

    result, inference_time = inference_spektral(model, args.number_iter, input_loader, args.time)
    log.info('Computing performance metrics')
    inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)

    report_writer.update_execution_results(**inference_result)
    log.info(f'Wrote report to {args.report_path}')
    report_writer.write_report(args.report_path)

    if not args.raw_output:
        if args.number_iter == 1:
            result = process_output(result, args.task)
            log.info(f'Inference results:\n{result}')

    log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')


if __name__ == '__main__':
    sys.exit(main() or 0)
