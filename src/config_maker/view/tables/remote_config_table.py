from .table import Table  # pylint: disable=E0402
# pylint: disable-next=E0401
from tags import CONFIG_IP_TAG, CONFIG_LOGIN_TAG, CONFIG_PASSWORD_TAG, CONFIG_OS_TAG, CONFIG_FTP_CLIENT_PATH_TAG, \
    CONFIG_CONFIG_TAG, CONFIG_EXECUTOR_TAG, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG, CONFIG_AC_DATASET_PATH_TAG, \
    CONFIG_DEFINITION_PATH, CONFIG_BENCHMARK_TAG, CONFIG_ACCURACY_CHECKER_TAG


class RemoteConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        benchmark_headers = [CONFIG_CONFIG_TAG, CONFIG_EXECUTOR_TAG, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG]
        accuracy_checker_headers = [CONFIG_CONFIG_TAG, CONFIG_EXECUTOR_TAG, CONFIG_AC_DATASET_PATH_TAG,
                                    CONFIG_DEFINITION_PATH, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG]
        self.__headers = [CONFIG_IP_TAG, CONFIG_LOGIN_TAG, CONFIG_PASSWORD_TAG, CONFIG_OS_TAG,
                          CONFIG_FTP_CLIENT_PATH_TAG]
        self.__headers.extend(CONFIG_BENCHMARK_TAG + tag for tag in benchmark_headers)
        self.__headers.extend(CONFIG_ACCURACY_CHECKER_TAG + tag for tag in accuracy_checker_headers)
        self._count_col = len(self.__headers)
        self._count_row = 100
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)

    def update(self, computers):
        self.clear()
        count = 0
        for i in range(len(computers)):
            self.setItem(i, 0, self._create_cell(computers[i].ip))
            self.setItem(i, 1, self._create_cell(computers[i].login))
            self.setItem(i, 2, self._create_cell(computers[i].password))
            self.setItem(i, 3, self._create_cell(computers[i].os))
            self.setItem(i, 4, self._create_cell(computers[i].path_to_ftp_client))
            self.setItem(i, 5, self._create_cell(computers[i].benchmark.parameters[CONFIG_CONFIG_TAG]))
            self.setItem(i, 6, self._create_cell(computers[i].benchmark.parameters[CONFIG_EXECUTOR_TAG]))
            self.setItem(i, 7, self._create_cell(computers[i].benchmark.parameters[CONFIG_LOG_FILE_TAG]))
            self.setItem(i, 8, self._create_cell(computers[i].benchmark.parameters[CONFIG_RESULT_FILE_TAG]))
            self.setItem(i, 9, self._create_cell(computers[i].accuracy_checker.parameters[CONFIG_CONFIG_TAG]))
            self.setItem(i, 10, self._create_cell(computers[i].accuracy_checker.parameters[CONFIG_EXECUTOR_TAG]))
            self.setItem(i, 11, self._create_cell(computers[i].accuracy_checker.parameters[CONFIG_AC_DATASET_PATH_TAG]))
            self.setItem(i, 12, self._create_cell(computers[i].accuracy_checker.parameters[CONFIG_DEFINITION_PATH]))
            self.setItem(i, 13, self._create_cell(computers[i].accuracy_checker.parameters[CONFIG_LOG_FILE_TAG]))
            self.setItem(i, 14, self._create_cell(computers[i].accuracy_checker.parameters[CONFIG_RESULT_FILE_TAG]))
            count += 1
