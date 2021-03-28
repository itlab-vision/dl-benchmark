import abc
import yaml


class HTMLTable(metaclass=abc.ABCMeta):
    def __init__(self, table_csv, file):
        self._table_html = []
        self._table_csv = table_csv
        self._frameworks_list = yaml.safe_load(file)['frameworks']

    def add_styles_to_table(self, path_to_styles):
        styles = open(path_to_styles, 'r')
        for line in styles:
            self._table_html.append(line)

    def save_html_table(self, path_table_html):
        fileHTML = open(path_table_html, 'w')
        self._table_html.append('</table>')
        for line in self._table_html:
            fileHTML.write(line)

    def sort_all_tests(self):
        models_dict = self._get_model_dict()
        self._get_nested_parameters(models_dict)
        self._task_types_dict = self.__format_models_dict(models_dict)
        self._column_dict = self._get_column_dict()
        self._added_all_test(models_dict)

    @abc.abstractmethod
    def _get_model_dict(self):
        pass

    @abc.abstractmethod
    def _get_nested_parameters(self, models_dict):
        pass

    @abc.abstractmethod
    def _get_column_dict(self):
        pass

    @abc.abstractmethod
    def _added_all_test(self, models_dict):
        pass

    def __format_models_dict(self, models_dict):
        task_types_dict = dict()
        for model in models_dict:
            try:
                task_types_dict[models_dict[model]['type']][model] = models_dict[model]
            except KeyError:
                task_types_dict[models_dict[model]['type']] = {model: models_dict[model]}
        return task_types_dict
