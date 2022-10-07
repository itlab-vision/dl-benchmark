import abc
import logging


class XlsxTable(metaclass=abc.ABCMeta):
    def __init__(self, paths_table_csv, path_table_xlsx, sheet_name):
        logging.info('START: __init__(). Input: {0}, {1}'.format(
            paths_table_csv, path_table_xlsx))

        self._paths_table_csv = paths_table_csv
        self._path_table_xlsx = path_table_xlsx
        self._sheet_name = sheet_name
                
        logging.info('FINISH: __init__()')
    
    @abc.abstractmethod
    def _init_xlsx_parameters(self):
        pass
    
    @abc.abstractmethod
    def read_csv_table(self):
        pass
    
    @abc.abstractmethod
    def create_table_header(self):
        pass

    @abc.abstractmethod
    def create_table_rows(self):
        pass

    @abc.abstractmethod
    def write_test_results(self):
        pass

    @abc.abstractmethod
    def beautify_table(self):
        pass

    @abc.abstractmethod
    def close_table(self):
        pass
