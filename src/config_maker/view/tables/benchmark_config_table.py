from .table import Table  # pylint: disable=E0402
# pylint: disable-next=E0401
from tags import CONFIG_MODEL_TAG, CONFIG_DATASET_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_BATCH_SIZE_TAG, CONFIG_DEVICE_TAG, \
    CONFIG_ITERATION_COUNT_TAG, CONFIG_TEST_TIME_LIMIT_TAG, CONFIG_FRAMEWORK_DEPENDENT_TAG, CONFIG_MODE_TAG, \
    CONFIG_EXTENSION_TAG, CONFIG_ASYNC_REQ_COUNT_TAG, CONFIG_THREAD_COUNT_TAG, CONFIG_STREAM_COUNT_TAG, \
    CONFIG_CHANNEL_SWAP_TAG, CONFIG_MEAN_TAG, CONFIG_INPUT_SCALE_TAG, CONFIG_INPUT_SHAPE_TAG, CONFIG_INPUT_NAME_TAG, \
    CONFIG_OUTPUT_NAMES_TAG, CONFIG_KMP_AFFINITY_TAG,  CONFIG_INTER_OP_THREADS_TAG, \
    CONFIG_INTRA_OP_THREADS_TAG


class BenchmarkConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.headers = [CONFIG_MODEL_TAG, CONFIG_DATASET_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_BATCH_SIZE_TAG,
                        CONFIG_DEVICE_TAG, CONFIG_ITERATION_COUNT_TAG, CONFIG_TEST_TIME_LIMIT_TAG, CONFIG_MODE_TAG,
                        CONFIG_EXTENSION_TAG, CONFIG_ASYNC_REQ_COUNT_TAG, CONFIG_THREAD_COUNT_TAG,
                        CONFIG_STREAM_COUNT_TAG, CONFIG_CHANNEL_SWAP_TAG, CONFIG_MEAN_TAG, CONFIG_INPUT_SCALE_TAG,
                        CONFIG_INPUT_SHAPE_TAG, CONFIG_INPUT_NAME_TAG, CONFIG_OUTPUT_NAMES_TAG, CONFIG_KMP_AFFINITY_TAG,
                        CONFIG_INTER_OP_THREADS_TAG, CONFIG_INTRA_OP_THREADS_TAG]
        self._count_col = len(self.headers)
        self._count_row = 350
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.headers)
        self._resize_columns()
        self.clear()

    def update(self, tests):
        self.clear()
        count = 0
        for i in range(len(tests)):
            test_dict = tests[i].get_values_dict()
            self.setItem(i, 0, self._create_cell(test_dict[CONFIG_MODEL_TAG].get_str()))
            self.setItem(i, 1, self._create_cell(test_dict[CONFIG_DATASET_TAG].get_str()))
            self.setItem(i, 2, self._create_cell(test_dict[CONFIG_FRAMEWORK_TAG]))
            self.setItem(i, 3, self._create_cell(test_dict[CONFIG_BATCH_SIZE_TAG]))
            self.setItem(i, 4, self._create_cell(test_dict[CONFIG_DEVICE_TAG]))
            self.setItem(i, 5, self._create_cell(test_dict[CONFIG_ITERATION_COUNT_TAG]))
            self.setItem(i, 6, self._create_cell(test_dict[CONFIG_TEST_TIME_LIMIT_TAG]))
            self.__update_framework_dependent_parameters(test_dict[CONFIG_FRAMEWORK_DEPENDENT_TAG], i)
            count += 1

    def __update_framework_dependent_parameters(self, parameters, i):
        values = parameters.get_parameter_dict()
        for key in values.keys():
            self.setItem(i, self.headers.index(key), self._create_cell(values[key]))
