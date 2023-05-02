import abc
import logging
import tkinter
import tkinter.font

from iteration_utilities import deepflatten


class XlsxTable(metaclass=abc.ABCMeta):
    def __init__(self, paths_table_csv, path_table_xlsx, sheet_name):
        logging.info('START: __init__(). Input: {0}, {1}'.format(
            paths_table_csv, path_table_xlsx))

        self._paths_table_csv = paths_table_csv
        self._path_table_xlsx = path_table_xlsx
        self._sheet_name = sheet_name

        logging.info('FINISH: __init__()')

    @staticmethod
    def _get_column_width(values, format_):
        root = tkinter.Tk()
        max_cell_width = 0
        used_font = tkinter.font.Font(family=format_.font_name,
                                      size=format_.font_size,
                                      weight=('bold' if format_.bold else 'normal'),
                                      slant=('italic' if format_.italic else 'roman'),
                                      underline=format_.underline,
                                      overstrike=format_.font_strikeout)
        reference_font = tkinter.font.Font(family='Calibri', size=11)
        for _, value in values.items():
            if str(value).lower() == 'nan':
                continue
            if '\n' in value:
                pixelwidths = [used_font.measure(part) for part in value.split('\n')]
                cell_width = (max(pixelwidths) + used_font.measure(' ')) / reference_font.measure('0')
            else:
                cell_width = used_font.measure(value + ' ') / reference_font.measure('0')
            max_cell_width = max(max_cell_width, cell_width)
        root.update_idletasks()
        root.destroy()
        return max_cell_width

    def _get_infrastructure(self):
        logging.info('START: _get_infrastructure()')

        self._infrastructure = list(set(self._data_dictionary[self._KEY_INFRASTRUCTURE].values()))

        logging.info(f'FINISH: _get_infrastructure(). {self._infrastructure}')

    def _get_inference_frameworks(self):
        logging.info('START: _get_inference_frameworks()')

        self._inference_frameworks = []
        for machine in self._infrastructure:
            machine_inference_frameworks = []
            for key, value in self._data_dictionary[self._KEY_INFERENCE_FRAMEWORK].items():
                if (self._data_dictionary[self._KEY_INFRASTRUCTURE][key] == machine
                        and value not in machine_inference_frameworks):
                    machine_inference_frameworks.append(value)
            self._inference_frameworks.append(machine_inference_frameworks)

        logging.info(f'FINISH: _get_inference_frameworks(). {self._inference_frameworks}')

    @abc.abstractmethod
    def _get_devices(self):
        pass

    @abc.abstractmethod
    def _get_precisions(self):
        pass

    @abc.abstractmethod
    def _init_xlsx_parameters(self):
        pass

    def _create_row_record_by_key(self, records_group, key):
        record = {}
        # fill existingvalues
        for value in records_group:
            col_idx = self._find_column_idx(value)
            record.update({col_idx: value[key]})
        # fill undefined values
        available_col_indeces = list(deepflatten(self._col_indeces))  # flatten
        keys = list(record.keys())  # existing indeces
        undefined_col_indeces = [idx for idx in available_col_indeces if idx not in keys]
        for idx in undefined_col_indeces:
            record.update({idx: 'Undefined'})
        return record

    def _find_idx(self, element, available_elements, exception_str):
        try:
            return available_elements.index(element)
        except ValueError:
            raise ValueError(exception_str)

    def _find_infrastructure_idx(self, infrastructure_name,
                                 available_infrastructure):
        return self._find_idx(infrastructure_name, available_infrastructure,
                              'Unknown infrastructure')

    def _find_inference_framework_idx(self, framework_name,
                                      available_inference_frameworks):
        return self._find_idx(framework_name, available_inference_frameworks,
                              'Unknown inference framework')

    def _find_device_idx(self, device_name, available_devices):
        return self._find_idx(device_name, available_devices,
                              'Unknown device name')

    def _find_precision_idx(self, precision, available_precisions):
        return self._find_idx(precision, available_precisions,
                              'Unknown precision')

    def _find_execution_mode_idx(self, execution_mode,
                                 available_execution_modes):
        return self._find_idx(execution_mode, available_execution_modes,
                              'Unknown execution mode')

    def _find_execparams_idx(self, parameters, available_parameters):
        return self._find_idx(parameters, available_parameters,
                              'Unknown param')

    @abc.abstractmethod
    def _find_column_idx(self, value):
        pass

    def _draw_bold_bolder(self, rel_row_idx, rel_col_idx, num_rows, num_cols):
        if (num_cols > 2):
            # top
            self._sheet.conditional_format(rel_row_idx, rel_col_idx + 1,
                                           rel_row_idx, rel_col_idx + num_cols - 2,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 5,
                                                                             'bottom': 1,
                                                                             'left': 1,
                                                                             'right': 1})})
            # bottom
            self._sheet.conditional_format(rel_row_idx + num_rows - 1, rel_col_idx + 1,
                                           rel_row_idx + num_rows - 1, rel_col_idx + num_cols - 2,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 1,
                                                                             'bottom': 5,
                                                                             'left': 1,
                                                                             'right': 1})})
        if (num_rows > 2):
            # right
            self._sheet.conditional_format(rel_row_idx + 1, rel_col_idx + num_cols - 1,
                                           rel_row_idx + num_rows - 2, rel_col_idx + num_cols - 1,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 1,
                                                                             'bottom': 1,
                                                                             'left': 1,
                                                                             'right': 5})})
            # left
            self._sheet.conditional_format(rel_row_idx + 1, rel_col_idx,
                                           rel_row_idx + num_rows - 2, rel_col_idx,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 1,
                                                                             'bottom': 1,
                                                                             'left': 5,
                                                                             'right': 1})})
        if num_cols == 1:
            self._sheet.conditional_format(rel_row_idx, rel_col_idx,
                                           rel_row_idx, rel_col_idx,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 5,
                                                                             'bottom': 1,
                                                                             'left': 5,
                                                                             'right': 5})})
            self._sheet.conditional_format(rel_row_idx + num_rows - 1, rel_col_idx,
                                           rel_row_idx + num_rows - 1, rel_col_idx,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 1,
                                                                             'bottom': 5,
                                                                             'left': 5,
                                                                             'right': 5})})
        if num_rows == 1:
            self._sheet.conditional_format(rel_row_idx, rel_col_idx,
                                           rel_row_idx, rel_col_idx,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 5,
                                                                             'bottom': 5,
                                                                             'left': 5,
                                                                             'right': 1})})
            self._sheet.conditional_format(rel_row_idx, rel_col_idx + num_cols - 1,
                                           rel_row_idx, rel_col_idx + num_cols - 1,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 5,
                                                                             'bottom': 5,
                                                                             'left': 1,
                                                                             'right': 5})})
        if num_rows > 1 and num_cols > 1:
            # top left corner
            self._sheet.conditional_format(rel_row_idx, rel_col_idx,
                                           rel_row_idx, rel_col_idx,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 5,
                                                                             'bottom': 1,
                                                                             'left': 5,
                                                                             'right': 1})})
            # bottom left corner
            self._sheet.conditional_format(rel_row_idx + num_rows - 1, rel_col_idx,
                                           rel_row_idx + num_rows - 1, rel_col_idx,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 1,
                                                                             'bottom': 5,
                                                                             'left': 5,
                                                                             'right': 1})})
            # top right corner
            self._sheet.conditional_format(rel_row_idx, rel_col_idx + num_cols - 1,
                                           rel_row_idx, rel_col_idx + num_cols - 1,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 5,
                                                                             'bottom': 1,
                                                                             'left': 1,
                                                                             'right': 5})})
            # bottom right corner
            self._sheet.conditional_format(rel_row_idx + num_rows - 1, rel_col_idx + num_cols - 1,
                                           rel_row_idx + num_rows - 1, rel_col_idx + num_cols - 1,
                                           {'type': 'no_blanks',
                                            'format': self._book.add_format({'top': 1,
                                                                             'bottom': 5,
                                                                             'left': 1,
                                                                             'right': 5})})

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
