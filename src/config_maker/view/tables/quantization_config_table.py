from .table import Table  # pylint: disable=E0402
# pylint: disable-next=E0401
from tags import HEADER_ALL_PARAMS_TAGS, HEADER_INDEPENDENT_PARAMS_TAGS, \
    HEADER_DQ_PARAMS_TAGS, HEADER_AAQ_PARAMS_TAGS


class QuantizationConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__headers = HEADER_ALL_PARAMS_TAGS
        self.__independent_params_count = len(HEADER_INDEPENDENT_PARAMS_TAGS)
        self._count_col = len(self.__headers)
        self._count_row = 100
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)  # pylint: disable=E1120

    def update(self, q_models):
        self.clear()
        for i, q_model in enumerate(q_models):
            independent_params, dependent_params = q_model.get_params()
            quantization_method = q_model.get_quantization_method()
            for j, param_value in enumerate(independent_params):
                self.setItem(i, j, self._create_cell(param_value))
            self.__update_dependent_parameters(dependent_params, quantization_method, i)

    def __update_dependent_parameters(self, parameters, quantization_method, i):
        start_idx = self.__calculate_start_index(quantization_method)
        for j, param_value in enumerate(parameters):
            self.setItem(i, start_idx + j, self._create_cell(param_value))

    def __calculate_start_index(self, quantization_method):
        start_idx = self.__independent_params_count

        methods = {
            'DefaultQuantization': len(HEADER_DQ_PARAMS_TAGS),
            'AccuracyAwareQuantization': len(HEADER_AAQ_PARAMS_TAGS)
        }

        for method_name in methods.keys():
            if quantization_method == method_name:
                return start_idx
            start_idx += methods[method_name]
