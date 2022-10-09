import abc
import logging
import tkinter
import tkinter.font


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
