from utils import get_param_from_data


class AllParameters:
    def __init__(self, data):
        GLOBAL_PARAMS_TAG = 'global_pot_parameters'
        PARAMETERS_TAG = 'parameters'

        self.global_pot_parameters = PotParameters(get_param_from_data(data, GLOBAL_PARAMS_TAG))
        self.models_list = [
            ModelParameters(m_params, self.global_pot_parameters)
            for m_params in get_param_from_data(data, PARAMETERS_TAG)
        ]


class ModelParameters:
    def __init__(self, data, g_pot_params):
        CONFIG_ID_TAG = 'config_id'
        POT_PARAMETERS_TAG = 'pot_parameters'
        CONFIG_PARAMETERS_TAG = 'config_parameters'

        self.__config_parameters = get_param_from_data(
            data,
            CONFIG_PARAMETERS_TAG
        )
        self.__config_id = get_param_from_data(data, CONFIG_ID_TAG)

        self.__pot_parameters = g_pot_params
        params = get_param_from_data(data, POT_PARAMETERS_TAG)
        if params is not None:
            self.__pot_parameters = PotParameters(params)

    def get_config_parameters(self):
        return self.__config_parameters

    def get_pot_parameters(self):
        return self.__pot_parameters

    def get_config_json_filename(self):
        return self.__config_id + '.json'


class PotParameters:
    def __init__(self, data):
        CONFIG_TAG = 'config'
        Q_METHOD_TAG = 'quantization_method'
        MODEL_TAG = 'model'
        WEIGHTS_TAG = 'weights'
        MODEL_NAME_TAG = 'model_name'
        PRESET_TAG = 'preset'
        AC_CONFIG_TAG = 'ac_config'
        MAX_DROP_TAG = 'max_drop'
        EVALUATION_TAG = 'evaluation'
        OUTPUT_DIR_TAG = 'output_dir'
        DIRECT_DUMP_TAG = 'direct_dump'
        LOG_LEVEL_TAG = 'log_level'
        PROGRESS_BAR_TAG = 'progress_bar'
        STREAM_OUTPUT = 'stream_output'
        KEEP_WEIGHTS = 'keep_uncompressed_weights'

        self.config = get_param_from_data(data, CONFIG_TAG)
        self.quantization_method = get_param_from_data(data, Q_METHOD_TAG)
        self.model = get_param_from_data(data, MODEL_TAG)
        self.weights = get_param_from_data(data, WEIGHTS_TAG)
        self.model_name = get_param_from_data(data, MODEL_NAME_TAG)
        self.preset = get_param_from_data(data, PRESET_TAG)
        self.ac_config = get_param_from_data(data, AC_CONFIG_TAG)
        self.max_drop = get_param_from_data(data, MAX_DROP_TAG)
        self.evaluation = get_param_from_data(data, EVALUATION_TAG)
        self.output_dir = get_param_from_data(data, OUTPUT_DIR_TAG)
        self.direct_dump = get_param_from_data(data, DIRECT_DUMP_TAG)
        self.log_level = get_param_from_data(data, LOG_LEVEL_TAG)
        self.progress_bar = get_param_from_data(data, PROGRESS_BAR_TAG)
        self.stream_output = get_param_from_data(data, STREAM_OUTPUT)
        self.keep_uncompressed_weights = get_param_from_data(
            data,
            KEEP_WEIGHTS
        )

    def rewrite_config_path(self, new_path):
        self.config = new_path
