from .table import Table  # pylint: disable=E0402
# pylint: disable-next=E0401
# from tags import CONFIG_CONFIG_TAG, CONFIG_QUANTIZATION_METHOD_TAG, CONFIG_NAME_TAG, \
#     CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_PRESET_TAG, CONFIG_AC_CONFIG_TAG, \
#     CONFIG_MAX_DROP_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG, \
#     CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG
from tags import DEPENDENT_PARAMETERS_TAG, HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS, HEADER_POT_PARAMS_TAGS, HEADER_MODEL_PARAMS_MODEL_TAGS, HEADER_MODEL_PARAMS_ENGINE_TAGS


class QuantizationConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        # pot_headers = [CONFIG_CONFIG_TAG, CONFIG_QUANTIZATION_METHOD_TAG, CONFIG_NAME_TAG,
        #     CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_PRESET_TAG, CONFIG_AC_CONFIG_TAG,
        #     CONFIG_MAX_DROP_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG,
        #     CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG,
        #     CONFIG_KEEP_WEIGHTS_TAG]
        # pot_headers = HEADER_POT_PARAMS_TAGS
        # self.__headers = []
        # self.__headers.extend(pot_headers)
        self.__headers = HEADER_POT_PARAMS_TAGS + HEADER_MODEL_PARAMS_MODEL_TAGS + \
            HEADER_MODEL_PARAMS_ENGINE_TAGS + HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS + []
        self._count_col = len(self.__headers)
        self._count_row = 100
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)

    def update(self, q_models):
        self.clear()
        for i, q_model in enumerate(q_models):
            for j, param_name in enumerate(self.__headers):
                self.setItem(i, j, self._create_cell(q_model.parameters[param_name]))
            self.__update_dependent_parameters(q_model.parameters[DEPENDENT_PARAMETERS_TAG], i)

    def __update_dependent_parameters(self, parameters, i):
        values = parameters.get_parameter_dict()
        for key in values.keys():
            self.setItem(i, self.__headers.index(key), self._create_cell(values[key]))
