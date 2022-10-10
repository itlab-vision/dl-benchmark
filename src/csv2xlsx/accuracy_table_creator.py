import logging
from collections import defaultdict

from table_creator import XlsxTable

import pandas
import xlsxwriter
from iteration_utilities import deepflatten


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
        self._KEY_TRAIN_FRAMEWORK = keys[3]
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

        logging.info('FINISH: _fill_horizontal_title()')

    def create_table_header(self):
        logging.info('START: create_table_header()')

        self._init_xlsx_parameters()

        # Freeze title panes
        self._sheet.freeze_panes(4, 5)

        # Write horizontal title (first cells before infrastructure)
        self._sheet.merge_range('A1:A4', self._KEY_TASK_TYPE, self._cell_format_title)
        self._sheet.merge_range('B1:B4', self._KEY_TOPOLOGY_NAME, self._cell_format_title)
        self._sheet.merge_range('C1:C4', self._KEY_TRAIN_FRAMEWORK, self._cell_format_title)
        self._sheet.merge_range('D1:D4', self._KEY_DATASET, self._cell_format_title)
        self._sheet.merge_range('E1:E4', self._KEY_ACCURACY_TYPE, self._cell_format_title)

        self._get_infrastructure()
        self._get_inference_frameworks()
        self._get_devices()
        self._get_precisions()

        # Write horizontal title (cells corresponding infrastructure)
        self._fill_horizontal_title()

        logging.info('FINISH: create_table_header()')

    def _find_row_records(self, task_type, topology_name, train_framework,
                          dataset, accuracy_type, experiments,
                          processed_records_keys):
        records_group = []
        for key, value in experiments.items():
            if (key not in processed_records_keys
                    and value[self._KEY_TASK_TYPE] == task_type
                    and value[self._KEY_TOPOLOGY_NAME] == topology_name
                    and value[self._KEY_TRAIN_FRAMEWORK] == train_framework
                    and value[self._KEY_DATASET] == dataset
                    and value[self._KEY_ACCURACY_TYPE] == accuracy_type):
                records_group.append(value)
                processed_records_keys.append(key)
        return records_group

    def _create_row_record(self, records_group):
        return self._create_row_record_by_key(records_group, self._KEY_ACCURACY)

    def _find_column_idx(self, value):
        idx1 = self._find_infrastructure_idx(value[self._KEY_INFRASTRUCTURE],
                                             self._infrastructure)
        idx2 = self._find_inference_framework_idx(value[self._KEY_INFERENCE_FRAMEWORK],
                                                  self._inference_frameworks[idx1])
        idx3 = self._find_device_idx(value[self._KEY_DEVICE], self._devices[idx1][idx2])
        idx4 = self._find_precision_idx(value[self._KEY_PRECISION],
                                        self._precisions[idx1][idx2][idx3])
        return self._col_indeces[idx1][idx2][idx3][idx4]

    def create_table_rows(self):
        logging.info('START: create_table_rows()')

        # transpose 2d dictionary
        experiments = self._data.to_dict('index')

        processed_records_keys = []
        self._table_records = defaultdict(list)
        for key, value in experiments.items():
            if key in processed_records_keys:
                continue
            records_group = self._find_row_records(value[self._KEY_TASK_TYPE],
                                                   value[self._KEY_TOPOLOGY_NAME],
                                                   value[self._KEY_TRAIN_FRAMEWORK],
                                                   value[self._KEY_DATASET],
                                                   value[self._KEY_ACCURACY_TYPE],
                                                   experiments,
                                                   processed_records_keys)
            if (len(records_group) == 0):
                continue
            accuracy_record = self._create_row_record(records_group)
            record = {self._KEY_TASK_TYPE: value[self._KEY_TASK_TYPE],
                      self._KEY_TOPOLOGY_NAME: value[self._KEY_TOPOLOGY_NAME],
                      self._KEY_TRAIN_FRAMEWORK: value[self._KEY_TRAIN_FRAMEWORK],
                      self._KEY_DATASET: value[self._KEY_DATASET],
                      self._KEY_ACCURACY_TYPE: value[self._KEY_ACCURACY_TYPE],
                      self._KEY_ACCURACY: accuracy_record}
            self._table_records[value[self._KEY_TASK_TYPE]].append(record)

        logging.info('FINISH: create_table_rows()')

    def _get_records_group(self, task_records, topology_name, train_framework,
                           dataset, processed_records_idxs):
        records_group = []
        for idx in range(len(task_records)):
            record = task_records[idx]
            if (idx not in processed_records_idxs
                    and record[self._KEY_TOPOLOGY_NAME] == topology_name
                    and record[self._KEY_TRAIN_FRAMEWORK] == train_framework
                    and record[self._KEY_DATASET] == dataset):
                processed_records_idxs.append(idx)
                records_group.append(record)
        return records_group

    def write_test_results(self):
        logging.info('START: write_test_results()')

        row_idx = 4
        for task_type, task_records in self._table_records.items():  # loop by tasks
            if len(task_records) <= 0:
                continue
            if len(task_records) > 1:  # print task type
                self._sheet.merge_range(row_idx, 0, row_idx + len(task_records) - 1, 0,
                                        task_type, self._cell_format_title)
            else:
                self._sheet.write(row_idx, 0, task_type, self._cell_format_title)

            processed_records_idxs = []
            for record in task_records:  # searching for records for the same topologies
                topology_name = record[self._KEY_TOPOLOGY_NAME]
                train_framework = record[self._KEY_TRAIN_FRAMEWORK]
                dataset = record[self._KEY_DATASET]
                records_group = self._get_records_group(task_records,
                                                        topology_name,
                                                        train_framework,
                                                        dataset,
                                                        processed_records_idxs)
                topology_num_records = len(records_group)
                if topology_num_records == 0:
                    continue
                if topology_num_records > 1:
                    self._sheet.merge_range(row_idx, 1,
                                            row_idx + topology_num_records - 1,
                                            1, topology_name,
                                            self._cell_format_title)
                    self._sheet.merge_range(row_idx, 2,
                                            row_idx + topology_num_records - 1,
                                            2, train_framework,
                                            self._cell_format_title)
                    self._sheet.merge_range(row_idx, 3,
                                            row_idx + topology_num_records - 1,
                                            3, dataset,
                                            self._cell_format_title)
                else:
                    self._sheet.write(row_idx, 1, topology_name, self._cell_format_title)
                    self._sheet.write(row_idx, 2, train_framework, self._cell_format_title)
                    self._sheet.write(row_idx, 3, dataset, self._cell_format_title)
                for topology_record in records_group:
                    self._sheet.write(row_idx, 4, topology_record[self._KEY_ACCURACY_TYPE],
                                      self._cell_format_title)
                    for key, value in topology_record[self._KEY_ACCURACY].items():
                        formatting = self._cell_format_acc
                        if value == 'None':
                            value = 'NaN'
                            formatting = self._cell_format_nan_acc
                        elif value == 'Undefined':
                            formatting = self._cell_format_undefined_acc
                        self._sheet.write(row_idx, key, value, formatting)
                    row_idx += 1

        self._full_num_rows = row_idx

        logging.info('FINISH: write_test_results()')

    def beautify_table(self):
        logging.info('START: beautify_table()')

        rel_col_idx = 5  # task type, topology, framework, dataset, accuracy type
        rel_row_idx = 0
        num_header_rows = 4  # infrastructure, framework, device, precision
        col_depth = 2
        self._draw_bold_bolder(0, 0, num_header_rows, rel_col_idx)
        self._draw_bold_bolder(num_header_rows - 1, 0,
                               self._full_num_rows - num_header_rows + 1,
                               rel_col_idx)
        for idx in range(len(self._infrastructure)):
            precisions = list(deepflatten(self._precisions[idx], depth=col_depth))
            num_cols = len(precisions)
            self._draw_bold_bolder(rel_row_idx, rel_col_idx, num_header_rows, num_cols)
            self._draw_bold_bolder(rel_row_idx + num_header_rows - 1, rel_col_idx,
                                   self._full_num_rows - num_header_rows + 1, num_cols)
            rel_col_idx += num_cols

        logging.info('FINISH: beautify_table()')

    def close_table(self):
        logging.info('START: close_table()')

        self._book.close()

        logging.info('FINISH: close_table()')
