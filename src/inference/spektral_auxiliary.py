import os

import pandas as pd

import spektral
from io_adapter import IOAdapter

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


class CustomDataset(spektral.data.Dataset):
    def __init__(self, gpath, **kwargs):
        self.graph_path = gpath

        super().__init__(**kwargs)

    def download(self):
        pass

    def read(self):
        output = []
        output.append(spektral.utils.io.load_binary(self.graph_path))
        return output


class SpektralIO(IOAdapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)
        self._loader = None

    def get_io_adapter(args, io_model_wrapper, transformer):
        task = args.task
        if task == 'feedforward_spektral':
            return FeedForward_SpektralIO(args, io_model_wrapper, transformer)
        elif task == 'node-classification':
            return NodeClassification_SpektralIO(args, io_model_wrapper, transformer)

    def prepare_input(self, model, input_):
        self._input = input_
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
                raise ValueError('Attempt to import unsupported dataset.')
        else:
            dataset = CustomDataset(input_)

        if self._batch_size == 1:
            input_loader = spektral.data.SingleLoader(dataset)
        else:
            input_loader = spektral.data.BatchLoader(dataset, batch_size=self._batch_size)

        self._loader = input_loader

    def get_slice_input(self, *args, **kwargs):
        slice_input, _ = self._loader.__next__()
        return slice_input


class FeedForward_SpektralIO(SpektralIO):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        return


class NodeClassification_SpektralIO(SpektralIO):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        self.load_labels_map('cora.txt')

        _result = result.numpy()
        __result = {'Node': []}

        for i in range(len(self._labels_map)):
            __result[self._labels_map[i]] = []

        for i in range(len(_result)):
            __result['Node'].append(i)
            for j in range(len(self._labels_map)):
                __result[self._labels_map[j]].append(_result[i][j])

        pd_result = pd.DataFrame(__result)
        file_name = os.path.join(os.path.dirname(__file__), 'node_classification_out.csv')
        pd_result.to_csv(file_name, sep=' ', columns=list(__result.keys()), index=False)

        log.info(f'Result was saved to {file_name}')
