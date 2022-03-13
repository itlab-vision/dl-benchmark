from table_creator import HTMLTable


STATUS_POSITION_IN_TABLE = 0
TASK_TYPE_POSITION_IN_TABLE = 1
MODEL_POSITION_IN_TABLE = 2
FRAMEWORK_POSITION_IN_TABLE = 3
INFERENCE_FRAMEWORK_POSITION_IN_TABLE = 4
DEVICE_POSITION_IN_TABLE = 5
INFR_POSITION_IN_TABLE = 6
DATASET_POSITION_IN_TABLE = 7
ACCURACY_TYPE_POSITION_IN_TABLE = 8
PRECISION_POSITION_IN_TABLE = 9
ACCURACY_POSITION_IN_TABLE = 10


class HTMLAccuracyCheckerTable(HTMLTable):
    def __init__(self, _table_csv, _file):
        super().__init__(_table_csv, _file)

    def _get_model_dict(self):
        models_dict = dict()
        for row_index in range(1, len(self._table_csv)):
            try:
                models_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]]
            except KeyError:
                models_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]] = {
                    'type': self._table_csv[row_index][TASK_TYPE_POSITION_IN_TABLE],
                    'plugin': self._table_csv[row_index][DEVICE_POSITION_IN_TABLE],
                    'dataset': self._table_csv[row_index][DATASET_POSITION_IN_TABLE],
                    'framework': self._table_csv[row_index][FRAMEWORK_POSITION_IN_TABLE],
                    'accuracy_type': set()
                }
        return models_dict

    def _get_nested_parameters(self, model_dict):
        for row_index in range(1, len(self._table_csv)):
            model_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]]['accuracy_type'].add(
                self._table_csv[row_index][ACCURACY_TYPE_POSITION_IN_TABLE])

        for model in model_dict:
            model_dict[model]['accuracy_type'] =  \
                sorted(model_dict[model]['accuracy_type'])

    def __find_plugin_in_infr(self, plugin, framework, target_infr):
        for row_index in range(1, len(self._table_csv)):
            if (plugin in self._table_csv[row_index][DEVICE_POSITION_IN_TABLE] and
                    framework == self._table_csv[row_index][INFERENCE_FRAMEWORK_POSITION_IN_TABLE] and
                    target_infr == self._table_csv[row_index][INFR_POSITION_IN_TABLE]):
                return True
        return False

    def __find_framework_in_infr(self, framework, target_infr):
        for row_index in range(1, len(self._table_csv)):
            if (framework in self._table_csv[row_index][INFERENCE_FRAMEWORK_POSITION_IN_TABLE] and
                    target_infr == self._table_csv[row_index][INFR_POSITION_IN_TABLE]):
                return True
        return False

    def _get_column_dict(self):
        infr_dict = dict()
        for row_index in range(1, len(self._table_csv)):
            infrastructure = self._table_csv[row_index][INFR_POSITION_IN_TABLE]
            try:
                infr_dict[infrastructure]
            except KeyError:
                # Added to each intr all frameworks with target plugins.
                infr_dict[infrastructure] = {}
                for framework in self._frameworks_list:
                    if self.__find_framework_in_infr(framework['name'], infrastructure):
                        infr_dict[infrastructure][framework['name']] = {}
                        for plugin in framework:
                            if plugin == 'name':
                                continue
                            if self.__find_plugin_in_infr(plugin, framework['name'], infrastructure):
                                infr_dict[infrastructure][framework['name']][plugin] = \
                                    framework[plugin].replace(' ', '').split(',')
        return infr_dict

    def _added_all_test(self, models_dict):
        for infr in self._column_dict:
            for framework in self._column_dict[infr]:
                for plugin in self._column_dict[infr][framework]:
                    weights = self._column_dict[infr][framework][plugin]
                    self._column_dict[infr][framework][plugin] = {weight: {} for weight in weights}
                    for weight in weights:
                        for model in models_dict:
                            self._column_dict[infr][framework][plugin][weight][model] = {}
                            for type in models_dict[model]['accuracy_type']:
                                self._column_dict[infr][framework][plugin][weight][model][type] = \
                                    self.__find_test(model, framework, plugin, infr, type, weight)

    def __find_test(self, model, framework, plugin, infr, accuracy_type, precision):
        for row_index in range(1, len(self._table_csv)):
            if (self._table_csv[row_index][MODEL_POSITION_IN_TABLE] == model and
                    self._table_csv[row_index][INFERENCE_FRAMEWORK_POSITION_IN_TABLE] == framework and
                    self._table_csv[row_index][DEVICE_POSITION_IN_TABLE] == plugin and
                    self._table_csv[row_index][INFR_POSITION_IN_TABLE] == infr and
                    self._table_csv[row_index][ACCURACY_TYPE_POSITION_IN_TABLE] == accuracy_type and
                    (self._table_csv[row_index][PRECISION_POSITION_IN_TABLE] == precision or
                     self._table_csv[row_index][PRECISION_POSITION_IN_TABLE] == '')):
                if self._table_csv[row_index][STATUS_POSITION_IN_TABLE] == 'FAILED':
                    return '-'
                else:
                    return self._table_csv[row_index][ACCURACY_POSITION_IN_TABLE]
        return 'N/A'

    def create_table_header(self):
        self._table_html.append('\n<table align="center" border="1" cellspacing="0" cellpadding="0" class="main">')
        self._table_html.append('\n<tr>\n<th>Task type</th>\n<th>Topology name</th>\n<th>Framework</th>\n<th>Dataset</th>\n<th>Accuracy type</th>\n')
        for infr in self._column_dict:
            self._table_html.append(
                '<th> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            self._table_html.append('<tr>\n<th>{}</th>\n</tr>'.format(infr))
            self._table_html.append(
                '\n<tr>\n<td> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n<tr>')
            for framework in self._column_dict[infr]:
                self._table_html.append('<th> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="{}">\n')
                self._table_html.append('\n<th>{}</th></tr><tr>'.format(framework))
                self._table_html.append('<td> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="one_type_table">\n<tr>')
                for plugin in self._column_dict[infr][framework]:
                    self._table_html.append('<th><table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="one_type_table">\n<tr>')
                    self._table_html.append('\n<th>{}</th>\n</tr>'.format(plugin))
                    self._table_html.append('\n<tr>\n<td> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="one_type_table">\n<tr>')
                    for weights in self._column_dict[infr][framework][plugin]:
                        self._table_html.append('<th><table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="one_type_table">\n')
                        self._table_html.append('<tr><th >{}</th>\n</tr>'.format(weights))
                        self._table_html.append('\n</table></th>\n')
                    self._table_html.append('</tr>\n</table></td></tr>')
                    self._table_html.append('\n</table>\n</th>\n')
                self._table_html.append('</tr>\n</table></td></tr>')
                self._table_html.append('\n</table>\n</th>\n')
            self._table_html.append('</tr>\n</table></td></tr>')
            self._table_html.append('\n</table>\n</th>\n')
        self._table_html.append('</tr>\n')

    def write_test_results(self):
        for task_type in self._task_types_dict:
            self._table_html.append('\n<tr>')
            self._table_html.append('<td>{}</td>'.format(task_type))

            # Print models
            self._table_html.append('<td> <table align="center" class="lock" height="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr><td>\n<table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                self._table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(model))
            self._table_html.append('</table>\n</td>')

            # Print framework
            self._table_html.append('<td> <table align="center" class="lock" height="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr><td>\n<table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                self._table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(
                    self._task_types_dict[task_type][model]['framework'])
                )
            self._table_html.append('</table>\n</td>')

            # Print dataset
            self._table_html.append('<td> <table align="center" class="lock" height="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr><td>\n<table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                self._table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(
                    self._task_types_dict[task_type][model]['dataset'])
                )
            self._table_html.append('</table>\n</td>')

            # Print accuracy type
            self._table_html.append('<td > <table align="center" class="lock" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr>\n <td> <table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                for accuracy_type in self._task_types_dict[task_type][model]['accuracy_type']:
                    self._table_html.append('<tr>\n<td align="right">{}</td>\n</tr>\n'.format(accuracy_type))
                self._table_html.append('</table>\n</td></tr>')
            self._table_html.append('</table>\n</td>')

            # Print results
            for infr in self._column_dict:
                self._table_html.append('<td> <table align="center" class="lock" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                for model in self._task_types_dict[task_type]:
                    self._table_html.append('<tr>\n<td> <table align="center" class="lock" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                    for framework in self._column_dict[infr]:
                        for plugin in self._column_dict[infr][framework]:
                            for weight in self._column_dict[infr][framework][plugin]:
                                self._table_html.append(
                                    '<td height="120px"><table align="center" class="result_column" border="1" cellspacing="0" cellpadding="0" class="one_type_table">')
                                for accuracy_type in self._task_types_dict[task_type][model]['accuracy_type']:
                                    self._table_html.append(
                                        '\n<tr><td><table align="center" border="1" cellspacing="0" cellpadding="0" class="one_type_table">\n')
                                    self._table_html.append(
                                        '<tr><td class="double" align="right">{}</td>\n</tr>'.format(
                                            self._column_dict[infr][framework][plugin][weight][model][accuracy_type]))
                                    self._table_html.append('\n</table></td>\n</tr>')
                                self._table_html.append('</table>\n</td>')
                    self._table_html.append('</table>\n</td>\n</tr>')
                self._table_html.append('</table>\n</td>')

            self._table_html.append('\n</tr>')
