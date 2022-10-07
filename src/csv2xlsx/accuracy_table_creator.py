import logging

from table_creator import XlsxTable

import pandas
import xlsxwriter

class XlsxAccuracyTable(XlsxTable):
    def __init__(self, paths_table_csv, path_table_xlsx):
        logging.info('START: __init__(). Input: {0}, {1}'.format(
            paths_table_csv, path_table_xlsx))
        
        super().__init__(paths_table_csv, path_table_xlsx, 'Accuracy')

        logging.info('FINISH: __init__()')

    def _init_xlsx_parameters(self):
        logging.info('START: _init_xlsx_parameters()')

        self._book = xlsxwriter.Workbook(self._path_table_xlsx)
        self._sheet = self._book.add_worksheet(self._sheet_name)

        # For the title
        self._cell_format = self._book.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': 1,
             'bold': True, 'text_wrap': True, 'font_size': 9})
        # For accuracy values
        self._cell_format_acc = self._book.add_format(
            {'valign': 'vcenter', 'border': 1, 'font_size': 9})  # float
        self._cell_format_nan_acc = self._book.add_format(
            {'align': 'right', 'valign': 'vcenter', 'border': 1,
             'font_size': 9, 'bg_color': '#F08080'})  # Nan
        self._cell_format_undefined_acc = self._book.add_format(
            {'align': 'right', 'valign': 'vcenter', 'border': 1,
             'font_size': 9, 'bg_color': '#FFFF00'})  # Undefined

        logging.info('FINISH: _init_xlsx_parameters()')

    def _init_table_keys(self):
        logging.info('START: _init_table_keys()')

        keys = list(self._data_dictionary.keys())
        self._KEY_STATUS = keys[0]
        self._KEY_TASK_TYPE = keys[1]
        self._KEY_TOPOLOGY_NAME = keys[2]
        self._KEY_FRAMEWORK = keys[3]
        self._KEY_INFERENCE_FRAMEWORK = keys[4]
        self._KEY_DEVICE = keys[5]
        self._KEY_INFRASTRUCTURE = keys[6]
        self._KEY_DATASET = keys[7]
        self._KEY_ACCURACY_TYPE = keys[8]
        self._KEY_PRECISION = keys[9]
        self._KEY_ACCURACY = keys[10]        
        
        logging.info(f'FINISH: _init_table_keys(). {keys}')

    def read_csv_table(self):
        logging.info('START: read_csv_table()')

        self._data = pandas.DataFrame()
        for path_table_csv in self._paths_table_csv:
            new_table = pandas.read_csv(path_table_csv, sep=';',
                                        encoding='latin-1')  # for title
            self._data = pandas.concat([self._data, new_table])
        self._data.reset_index(drop=True, inplace=True)
        self._data_dictionary = self._data.to_dict()  # for table rows
        self._init_table_keys()

        logging.info('FINISH: read_csv_table()')
    
    def create_table_header(self):
        raise ValueError('Method is not implemented')

    def create_table_rows(self):
        raise ValueError('Method is not implemented')

    def write_test_results(self):
        raise ValueError('Method is not implemented')

    def beautify_table(self):
        raise ValueError('Method is not implemented')

    def close_table(self):
        raise ValueError('Method is not implemented')