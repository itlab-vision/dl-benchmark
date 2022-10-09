import logging
import pandas
import xlsxwriter

from table_creator import XlsxTable


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
        self._cell_format_title = self._book.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': 1,
             'bold': True, 'text_wrap': True, 'font_size': 9})
        # For cells
        self._cell_format = self._book.add_format(
            {'align': 'left', 'valign': 'vcenter', 'border': 1,
             'bold': True, 'text_wrap': False, 'font_size': 9})
        # For accuracy values
        self._cell_format_acc = self._book.add_format(
            {'valign': 'right', 'border': 1, 'font_size': 9})  # float
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

    def _get_devices(self):
        logging.info('START: _get_devices()')

        self._devices = []
        for idx in range(len(self._infrastructure)):
            machine = self._infrastructure[idx]
            machine_inference_frameworks = self._inference_frameworks[idx]
            machine_framework_devices = []
            for inference_framework in machine_inference_frameworks:
                framework_devices = []
                for key, value in self._data_dictionary[self._KEY_DEVICE].items():
                    if (self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine
                        and self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK][key] == inference_framework
                        and value not in framework_devices):
                        framework_devices.append(value)
                machine_framework_devices.append(framework_devices)
            self._devices.append(machine_framework_devices)

        logging.info(f'FINISH: _get_devices(). {self._devices}')

    def _get_precisions(self):
        logging.info('START: _get_precisions()')

        self._precisions = []
        for idx in range(len(self._infrastructure)):
            machine = self._infrastructure[idx]
            machine_inference_frameworks = self._inference_frameworks[idx]
            machine_precisions = []
            for idx2 in range(len(machine_inference_frameworks)):
                inference_framework = machine_inference_frameworks[idx2]
                framework_devices = self._devices[idx][idx2]
                framework_precisions = []
                for device in framework_devices:
                    device_precisions = []
                    for key, value in self._data_dictionary[self._KEY_DEVICE].items():
                        if (self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine
                            and self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK][key] == inference_framework
                            and value == device
                            and self._data_dictionary[self._KEY_PRECISION][key] not in device_precisions):
                            device_precisions.append(self._data_dictionary[self._KEY_PRECISION][key])
                    framework_precisions.append(device_precisions)
                machine_precisions.append(framework_precisions)
            self._precisions.append(machine_precisions)

        logging.info(f'FINISH: _get_precisions(). {self._precisions}')

    def _fill_horizontal_title(self):
        logging.info('START: _fill_horizontal_title()')

        rel_row_idx = 4
        rel_col_idx = 5

        self._col_indeces = []
        for idx in range(len(self._infrastructure)):
            row_idx = rel_row_idx
            col_idx = rel_col_idx
            num_cols = 0
            machine = self._infrastructure[idx]
            machine_inference_frameworks = self._inference_frameworks[idx]
            col_idx3 = col_idx
            col_indeces2 = []
            for idx2 in range(len(machine_inference_frameworks)):
                machine_framework = machine_inference_frameworks[idx2]
                machine_framework_devices = self._devices[idx][idx2]
                col_idx2 = col_idx
                num_cols2 = 0
                col_indeces3 = []
                for idx3 in range(len(machine_framework_devices)):
                    machine_framework_device = machine_framework_devices[idx3]
                    framework_device_precisions = self._precisions[idx][idx2][idx3]
                    col_idx1 = col_idx
                    col_indeces4 = []
                    for idx4 in range(len(framework_device_precisions)):
                        framework_device_precision = framework_device_precisions[idx4]
                        self._sheet.write(row_idx - 1, col_idx1 + idx4,
                                          framework_device_precision,
                                          self._cell_format_title)
                        col_indeces4.append(col_idx1 + idx4)
                    k = len(framework_device_precisions)
                    if k == 1:
                        self._sheet.write(row_idx - 2, col_idx2,
                                          machine_framework_device,
                                          self._cell_format_title)
                    elif k > 1:
                        self._sheet.merge_range(row_idx - 2, col_idx2,
                                                row_idx - 2, col_idx2 + k - 1,
                                                machine_framework_device,
                                                self._cell_format_title)
                    else:
                        msg = 'Incorrect number of device precision modes'
                        logging.error(msg)
                        raise ValueError(msg)
                    num_cols2 += k
                    num_cols += k
                    col_idx += k
                    col_idx2 += k
                    col_indeces3.append(col_indeces4)
                if num_cols2 > 1:
                    self._sheet.merge_range(row_idx - 3, col_idx3,
                                            row_idx - 3, col_idx3 + num_cols2 - 1,
                                            machine_framework, self._cell_format_title)
                elif num_cols2 == 1:
                    self._sheet.write(row_idx - 3, col_idx3,
                                      machine_framework, self._cell_format_title)
                else:
                    msg = 'Incorrect number of frameworks'
                    logging.error(msg)
                    raise ValueError(msg)
                col_idx3 += num_cols2
                col_indeces2.append(col_indeces3)
            if num_cols > 1:
                self._sheet.merge_range(row_idx - 4, rel_col_idx,
                                        row_idx - 4, rel_col_idx + num_cols - 1,
                                        machine, self._cell_format_title)
            elif num_cols == 1:
                self._sheet.write(row_idx - 4, rel_col_idx,
                                  machine, self._cell_format_title)
            else:
                msg = 'Incorrect number of machines'
                logging.error(msg)
                raise ValueError(msg)
            rel_col_idx += num_cols
            self._col_indeces.append(col_indeces2)

        logging.info(f'FINISH: _fill_horizontal_title(). {self._col_indeces}')


    def create_table_header(self):
        logging.info('START: create_table_header()')

        self._init_xlsx_parameters()

        # Freeze title panes
        self._sheet.freeze_panes(4, 5)

        # Write horizontal title (first cells before infrastructure)
        self._sheet.merge_range('A1:A4', self._KEY_TASK_TYPE, self._cell_format_title)
        self._sheet.merge_range('B1:B4', self._KEY_TOPOLOGY_NAME, self._cell_format_title)
        self._sheet.merge_range('C1:C4', self._KEY_FRAMEWORK, self._cell_format_title)
        self._sheet.merge_range('D1:D4', self._KEY_DATASET, self._cell_format_title)
        self._sheet.merge_range('E1:E4', self._KEY_ACCURACY_TYPE, self._cell_format_title)

        self._get_infrastructure()
        self._get_inference_frameworks()
        self._get_devices()
        self._get_precisions()

        # Write horizontal title (cells corresponding infrastructure)
        self._fill_horizontal_title()

        logging.info('FINISH: create_table_header()')

    def create_table_rows(self):
        raise ValueError('Method is not implemented')

    def write_test_results(self):
        raise ValueError('Method is not implemented')

    def beautify_table(self):
        raise ValueError('Method is not implemented')

    def close_table(self):
        logging.info('START: close_table()')

        self._book.close()

        logging.info('FINISH: close_table()')