import spektral

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
