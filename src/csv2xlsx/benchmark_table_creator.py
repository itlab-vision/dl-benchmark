import abc
import xlsxwriter
import pandas
import re
from collections import defaultdict
from iteration_utilities import deepflatten


class XlsxBenchmarkTable(metaclass=abc.ABCMeta):
    def __init__(self, path_table_csv, path_table_xlsx):
        self._path_table_csv = path_table_csv
        self._path_table_xlsx = path_table_xlsx
    
    def _init_xlsx_parameters(self):
        self._sheet_name = 'Performance'
        
        self._book = xlsxwriter.Workbook(self._path_table_xlsx)
        self._sheet = self._book.add_worksheet(self._sheet_name)
        
        # For the title
        self._cell_format = self._book.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': 1, \
             'bold': True, 'text_wrap': True, 'font_size': 9})
        self._cell_format_title2 = self._book.add_format(
            {'align': 'center', 'valign': 'vcenter', \
             'border': 1, 'bold': True, 'font_size': 9})
        self._cell_format_task_type = self._book.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': 1, \
             'bold': True, 'rotation': 90, 'font_size': 9})
        # For FPS
        self._cell_format_fps = self._book.add_format(
            {'valign': 'vcenter', 'border': 1, 'font_size': 9})
        self._cell_format_nan_fps = self._book.add_format(
            {'align': 'right', 'valign': 'vcenter', 'border': 1, \
             'font_size': 9, 'bg_color': '#E28E7D'})
        self._cell_format_undefined_fps = self._book.add_format(
            {'align': 'right', 'valign': 'vcenter', 'border': 1, \
             'font_size': 9, 'bg_color': '#F0EE8A'})
    
    def _init_table_keys(self):
        keys = list(self._data_dictionary.keys())
        
        self._KEY_STATUS = keys[0]
        self._KEY_TASK_TYPE = keys[1]
        self._KEY_TOPOLOGY_NAME = keys[2]
        self._KEY_DATASET = keys[3]
        self._KEY_TRAIN_FRAMEWORK = keys[4]
        self._KEY_INFERENCE_FRAMEWORK = keys[5]
        self._KEY_BLOB_SIZE = keys[6]
        self._KEY_PRECISION = keys[7]
        self._KEY_BATCH_SIZE = keys[8]
        self._KEY_EXECUTION_MODE = keys[9]
        self._KEY_PARAMETERS = keys[10]
        self._KEY_INFRASTRUCTURE = keys[11]
        self._KEY_AVGTIME = keys[12]
        self._KEY_LATENCY = keys[13]
        self._KEY_FPS = keys[14]
    
    def read_csv_table(self):
        self._data = pandas.read_csv(self._path_table_csv, sep = ';', \
                                     encoding='latin-1')
        self._data_dictionary = self._data.to_dict()
        self._init_table_keys()
        
    
    def _get_infrastructure(self):
        self._infrastructure = list(
            set(list(self._data_dictionary[self._KEY_INFRASTRUCTURE].values())))
    
    def _get_inference_frameworks(self):
        self._inference_frameworks = []
        for machine in self._infrastructure:
            machine_inference_frameworks = []
            for key, value in self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK].items():
                if self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine and \
                    (value in machine_inference_frameworks) == False:
                    machine_inference_frameworks.append(value)
            self._inference_frameworks.append(machine_inference_frameworks)
    
    def _get_devices(self):
        self._devices = []
        for idx in range(len(self._infrastructure)):
            machine = self._infrastructure[idx]
            machine_inference_frameworks = self._inference_frameworks[idx]
            machine_framework_devices = []
            for inference_framework in machine_inference_frameworks:
                framework_devices = []
                for key, value in self._data_dictionary[self._KEY_PARAMETERS].items():
                    pattern = re.compile(r'[.]*Device:[ ]*(?P<device_name>[\W\w]+)[,]+[.]*')
                    matcher = re.match(pattern, value)
                    device_name = matcher.group('device_name')
                    if self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine and \
                        self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK][key] == inference_framework and \
                            (device_name in framework_devices) == False:
                        framework_devices.append(device_name)
                machine_framework_devices.append(framework_devices)
            self._devices.append(machine_framework_devices)
    
    def _get_precisions(self):
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
                    for key, value in self._data_dictionary[self._KEY_PARAMETERS].items():
                        pattern = re.compile(r'[.]*Device:[ ]*(?P<device_name>[\W\w]+)[,]+[.]*')
                        matcher = re.match(pattern, value)
                        device_name = matcher.group('device_name')
                        if self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine and \
                           self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK][key] == inference_framework and \
                           device_name == device and \
                           (self._data_dictionary[self._KEY_PRECISION][key] in device_precisions) == False:
                            device_precisions.append(self._data_dictionary[self._KEY_PRECISION][key])
                    framework_precisions.append(device_precisions)
                machine_precisions.append(framework_precisions)
            self._precisions.append(machine_precisions)
    
    def _get_execution_modes(self):
        self._execution_modes = []
        for idx in range(len(self._infrastructure)):
            machine = self._infrastructure[idx]
            machine_inference_frameworks = self._inference_frameworks[idx]
            machine_modes = []
            for idx2 in range(len(machine_inference_frameworks)):
                inference_framework = machine_inference_frameworks[idx2]
                framework_devices = self._devices[idx][idx2]
                framework_modes = []
                for idx3 in range(len(framework_devices)):
                    device = framework_devices[idx3]
                    device_precisions = self._precisions[idx][idx2][idx3]
                    framework_device_modes = []
                    for precision in device_precisions:
                        device_precision_modes = []
                        for key, value in self._data_dictionary[self._KEY_PARAMETERS].items():
                            pattern = re.compile(r'[.]*Device:[ ]*(?P<device_name>[\W\w]+)[,]+[.]*')
                            matcher = re.match(pattern, value)
                            device_name = matcher.group('device_name')
                            if self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine and \
                               self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK][key] == inference_framework and \
                               device_name == device and \
                               self._data_dictionary[self._KEY_PRECISION][key] == precision and \
                               (self._data_dictionary[self._KEY_EXECUTION_MODE][key] in device_precision_modes) == False:
                                device_precision_modes.append(self._data_dictionary[self._KEY_EXECUTION_MODE][key])
                        framework_device_modes.append(device_precision_modes)
                    framework_modes.append(framework_device_modes)
                machine_modes.append(framework_modes)
            self._execution_modes.append(machine_modes)
    
    def _get_column_indeces(self):
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
                    num_cols1 = 0
                    col_indeces4 = []
                    for idx4 in range(len(framework_device_precisions)):
                        framework_device_precision = framework_device_precisions[idx4]
                        framework_device_precision_modes = self._execution_modes[idx][idx2][idx3][idx4]
                        col_indeces5 = []
                        for idx5 in range(len(framework_device_precision_modes)):
                            framework_device_precision_mode = framework_device_precision_modes[idx5]
                            self._sheet.write(row_idx, col_idx + idx5, framework_device_precision_mode, self._cell_format)
                            col_indeces5.append(col_idx + idx5)
                        self._sheet.merge_range(row_idx - 1, col_idx1, \
                                          row_idx - 1, col_idx1 + len(framework_device_precision_modes) - 1, \
                                          framework_device_precision, self._cell_format)
                        col_idx += len(framework_device_precision_modes)
                        col_idx1 += len(framework_device_precision_modes)
                        num_cols1 += len(framework_device_precision_modes)
                        num_cols2 += len(framework_device_precision_modes)
                        num_cols += len(framework_device_precision_modes)
                        col_indeces4.append(col_indeces5)
                    self._sheet.merge_range(row_idx - 2, col_idx2, \
                                      row_idx - 2, col_idx2 + num_cols1 - 1, \
                                      machine_framework_device, self._cell_format)
                    col_idx2 += num_cols1
                    col_indeces3.append(col_indeces4)
                self._sheet.merge_range(row_idx - 3, col_idx3, \
                                  row_idx - 3, col_idx3 + num_cols2 - 1, \
                                  machine_framework, self._cell_format)
                col_idx3 += num_cols2
                col_indeces2.append(col_indeces3)
            self._sheet.merge_range(row_idx - 4, rel_col_idx, \
                              row_idx - 4, rel_col_idx + num_cols - 1, \
                              machine, self._cell_format)
            rel_col_idx += num_cols
            self._col_indeces.append(col_indeces2)
    
    def create_table_header(self):
        self._init_xlsx_parameters()
        
        # Freeze title panes
        self._sheet.freeze_panes(5, 5)
        
        self._sheet.merge_range('A1:A5', self._KEY_TASK_TYPE, self._cell_format)
        self._sheet.merge_range('B1:B5', self._KEY_TOPOLOGY_NAME, self._cell_format)
        self._sheet.merge_range('C1:C5', self._KEY_TRAIN_FRAMEWORK, self._cell_format)
        self._sheet.merge_range('D1:D5', self._KEY_BLOB_SIZE, self._cell_format)
        self._sheet.merge_range('E1:E5', self._KEY_BATCH_SIZE, self._cell_format)
        
        self._get_infrastructure()
        self._get_inference_frameworks()
        self._get_devices()
        self._get_precisions()
        self._get_execution_modes()        
        self._get_column_indeces() # TODO: split function
    
    def _find_idx(self, element, available_elements, exception_str):
        try:
            return available_elements.index(element)
        except:
            raise exception_str
    
    def _find_infrastructure_idx(self, infrastructure_name, available_infrastructure):
        return self._find_idx(infrastructure_name, available_infrastructure, \
                        'Unknown infrastructure')
    
    def _find_inference_framework_idx(self, framework_name, available_inference_frameworks):
        return self._find_idx(framework_name, available_inference_frameworks, \
                        'Unknown inference framework')
    
    def _find_device_idx(self, device_name, available_devices):
        return self._find_idx(device_name, available_devices, 'Unknown device name')
    
    def _find_precision_idx(self, precision, available_precisions):
        return self._find_idx(precision, available_precisions, 'Unknown precision')
    
    def _find_execution_mode_idx(self, execution_mode, available_execution_modes):
        return self._find_idx(execution_mode, available_execution_modes, \
                        'Unknown execution mode')
    
    def _find_column_idx(self, value, infrastructure, inference_frameworks, devices, \
                        precisions, execution_modes, col_indeces):
        idx1 = self._find_infrastructure_idx(value[self._KEY_INFRASTRUCTURE], \
                                             self._infrastructure)    
        idx2 = self._find_inference_framework_idx(value[self._KEY_INFERENCE_FRAMEWORK], \
                                                  self._inference_frameworks[idx1])
        pattern = re.compile(r'[.]*Device:[ ]*(?P<device_name>[\W\w]+)[,]+[.]*')
        matcher = re.match(pattern, value[self._KEY_PARAMETERS])
        device_name = matcher.group('device_name')
        idx3 = self._find_device_idx(device_name, self._devices[idx1][idx2])
        idx4 = self._find_precision_idx(value[self._KEY_PRECISION], \
                                        self._precisions[idx1][idx2][idx3])
        idx5 = self._find_execution_mode_idx(value[self._KEY_EXECUTION_MODE], \
                                             self._execution_modes[idx1][idx2][idx3][idx4])
        return self._col_indeces[idx1][idx2][idx3][idx4][idx5]
    
    def _find_row_records(self, task_type, topology_name, train_framework, \
                         blob_size, batch_size, experiments, processed_records_keys):
        records_group = []
        for key, value in experiments.items():
            if key not in processed_records_keys and \
               value[self._KEY_TASK_TYPE] == task_type and \
               value[self._KEY_TOPOLOGY_NAME] == topology_name and \
               value[self._KEY_TRAIN_FRAMEWORK] == train_framework and \
               value[self._KEY_BLOB_SIZE] == blob_size and \
               value[self._KEY_BATCH_SIZE] == batch_size:
                records_group.append(value)
                processed_records_keys.append(key)
        return records_group
    
    def _create_row_record(self, records_group, infrastructure, inference_frameworks, devices, \
                          precisions, execution_modes, col_indeces):
        fps_record = {}
        # fill existing FPS values
        for value in records_group:
            col_idx = self._find_column_idx(value, infrastructure, inference_frameworks, \
                devices, precisions, execution_modes, col_indeces)
            fps_record.update( {col_idx : value[self._KEY_FPS]} )
        # fill underfined FPS values
        available_col_indeces = list(deepflatten(col_indeces)) # flatten
        fps_keys = list(fps_record.keys()) # existing indeces
        undefined_col_indeces = [idx for idx in available_col_indeces if idx not in fps_keys]
        for idx in undefined_col_indeces:
            fps_record.update( {idx : 'Undefined'} )
        return fps_record
    
    def _remove_unused_metrics(self, data):
        # remove unused keys from DataFrame
        for key, value in self._data.copy().items():
            if key == self._KEY_AVGTIME or key == self._KEY_LATENCY:
                del self._data[key]
        return self._data
    
    def create_table_rows(self):
        self._data = self._remove_unused_metrics(self._data)
        # transpose 2d dictionary
        experiments = self._data.to_dict('index')

        processed_records_keys = []
        self._table_records = defaultdict(list)
        for key, value in experiments.items():
            if key in processed_records_keys:
                continue
            records_group = self._find_row_records(value[self._KEY_TASK_TYPE], \
                                                   value[self._KEY_TOPOLOGY_NAME], \
                value[self._KEY_TRAIN_FRAMEWORK], value[self._KEY_BLOB_SIZE], \
                    value[self._KEY_BATCH_SIZE], experiments, processed_records_keys)
            fps_record = self._create_row_record(records_group, self._infrastructure, \
                self._inference_frameworks, self._devices, self._precisions, \
                self._execution_modes, self._col_indeces)
            record = { self._KEY_TASK_TYPE : value[self._KEY_TASK_TYPE], \
                       self._KEY_TOPOLOGY_NAME : value[self._KEY_TOPOLOGY_NAME], \
                       self._KEY_TRAIN_FRAMEWORK : value[self._KEY_TRAIN_FRAMEWORK], \
                       self._KEY_BLOB_SIZE : value[self._KEY_BLOB_SIZE], \
                       self._KEY_BATCH_SIZE : value[self._KEY_BATCH_SIZE], \
                       self._KEY_FPS : fps_record }
            self._table_records[value[self._KEY_TASK_TYPE]].append(record)
    
    def _get_records_group(self, task_records, topology_name, train_framework, \
                      blob_size, processed_records_idxs):
        records_group = []
        for idx in range(len(task_records)):
            record = task_records[idx]
            if idx not in processed_records_idxs and \
               record[self._KEY_TOPOLOGY_NAME] == topology_name and \
               record[self._KEY_TRAIN_FRAMEWORK] == train_framework and \
               record[self._KEY_BLOB_SIZE] == blob_size:
                processed_records_idxs.append(idx)
                records_group.append(record)
        return records_group
    
    def write_test_results(self):
        row_idx = 5
        for task_type, task_records in self._table_records.items(): # loop by tasks
            if len(task_records) <= 0:
                continue
            elif len(task_records) > 1: # print task type
                self._sheet.merge_range(row_idx, 0, row_idx + len(task_records) - 1, 0, \
                                  task_type, self._cell_format_task_type)
            else:
                self._sheet.write(row_idx, 0, task_type, self._cell_format_task_type)
            
            processed_records_idxs = []
            for record in task_records: # loop by table records and searching for records for the same topologies
                topology_name = record[self._KEY_TOPOLOGY_NAME]
                train_framework = record[self._KEY_TRAIN_FRAMEWORK]
                blob_size = record[self._KEY_BLOB_SIZE]
                records_group = self._get_records_group(task_records, topology_name, \
                                                  train_framework, blob_size, \
                                                  processed_records_idxs)
                topology_num_records = len(records_group)
                blob_size = blob_size.replace(',', ',\n')
                if topology_num_records == 0:
                    continue
                elif topology_num_records > 1:
                    self._sheet.merge_range(row_idx, 1, row_idx + topology_num_records - 1, 1, \
                                      topology_name, self._cell_format_title2)
                    self._sheet.merge_range(row_idx, 2, row_idx + topology_num_records - 1, 2, \
                                      train_framework, self._cell_format_title2)
                    self._sheet.merge_range(row_idx, 3, row_idx + topology_num_records - 1, 3, \
                                      blob_size, self._cell_format_title2)
                else:
                    self._sheet.write(row_idx, 1, topology_name, self._cell_format_title2)
                    self._sheet.write(row_idx, 2, train_framework, self._cell_format_title2)
                    self._sheet.write(row_idx, 3, blob_size, self._cell_format_title2)
                for topology_record in records_group:
                    self._sheet.write(row_idx, 4, topology_record[self._KEY_BATCH_SIZE], \
                                      self._cell_format_title2)
                    for key, value in topology_record[self._KEY_FPS].items():
                        formatting = self._cell_format_fps
                        if value == 'None':
                            value = 'NaN'
                            formatting = self._cell_format_nan_fps
                        elif value == 'Undefined':
                            formatting = self._cell_format_undefined_fps
                        else:
                            value = float(value)
                        self._sheet.write(row_idx, key, value, formatting)
                    row_idx += 1

    def close_table(self):
        self._book.close()