from table_creator import HTMLTable


STATUS_POSITION_IN_TABLE = 0
TYPE_POSITION_IN_TABLE = 1
MODEL_POSITION_IN_TABLE = 2
FRAMEWORK_POSITION_IN_TABLE = 4
INFERENCE_POSITION_IN_TABLE = 5
SHAPE_POSITION_IN_TABLE = 6
WEIGHT_POSITION_IN_TABLE = 7
BATCH_POSITION_IN_TABLE = 8
MODE_POSITION_IN_TABLE = 9
PARAMS_POSITION_IN_TABLE = 10
INFR_POSITION_IN_TABLE = 11
FPS_POSITION_IN_TABLE = 14


class HTMLBenchmarkTable(HTMLTable):
    def __init__(self, _table_csv, _file):
        super().__init__(_table_csv, _file)

    @staticmethod
    def get_supported_mode(plugin):
        if plugin == 'CPU':
            return 'ALL'
        elif plugin == 'GPU':
            return 'SYNC'
        else:
            return 'ASYNC'

    def _get_model_dict(self):
        models_dict = {}
        for row_index in range(1, len(self._table_csv)):
            try:
                models_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]]
            except KeyError:
                models_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]] = {
                    'weight': set(),
                    'shape': self._table_csv[row_index][SHAPE_POSITION_IN_TABLE],
                    'batch': set(),
                    'type': self._table_csv[row_index][TYPE_POSITION_IN_TABLE],
                    'framework': self._table_csv[row_index][FRAMEWORK_POSITION_IN_TABLE]
                }
        return models_dict

    def _get_nested_parameters(self, models_dict):
        # Added to dict all weights and batch.
        for row_index in range(1, len(self._table_csv)):
            models_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]]['weight'].add(
                self._table_csv[row_index][WEIGHT_POSITION_IN_TABLE])
            models_dict[self._table_csv[row_index][MODEL_POSITION_IN_TABLE]]['batch'].add(
                self._table_csv[row_index][BATCH_POSITION_IN_TABLE])

        # Sort all batches, because they added in set randomly.
        for model in models_dict:
            models_dict[model]['batch'] =  \
                sorted(models_dict[model]['batch'], key=lambda val: int(val))

    def __find_plugin_in_infr(self, plugin, target_infr):
        for row_index in range(1, len(self._table_csv)):
            if plugin in self._table_csv[row_index][PARAMS_POSITION_IN_TABLE] and \
                    target_infr == self._table_csv[row_index][INFR_POSITION_IN_TABLE]:
                return True
        return False

    def _get_column_dict(self):
        infr_dict = {}
        for row_index in range(1, len(self._table_csv)):
            try:
                infr_dict[self._table_csv[row_index][INFR_POSITION_IN_TABLE]]
            except KeyError:
                # Added to each intr all frameworks with target plugins.
                infr_dict[self._table_csv[row_index][INFR_POSITION_IN_TABLE]] = {}
                for framework in self._frameworks_list:
                    infr_dict[self._table_csv[row_index][INFR_POSITION_IN_TABLE]][framework['name']] = {}
                    for plugin in framework:
                        if plugin == 'name':
                            continue
                        if self.__find_plugin_in_infr(plugin, self._table_csv[row_index][INFR_POSITION_IN_TABLE]):
                            infr_dict[self._table_csv[row_index][
                                INFR_POSITION_IN_TABLE]][framework['name']][plugin] = framework[
                                plugin].replace(' ', '').split(',')
        return infr_dict

    def __find_test_in_table(self, curr_infr, plugin, model_name, framework, batch, weight, mode):
        for row_index in range(1, len(self._table_csv)):
            if (self._table_csv[row_index][MODEL_POSITION_IN_TABLE] == model_name and
                    self._table_csv[row_index][INFR_POSITION_IN_TABLE] == curr_infr and
                    plugin in self._table_csv[row_index][PARAMS_POSITION_IN_TABLE] and
                    self._table_csv[row_index][BATCH_POSITION_IN_TABLE] == batch and
                    self._table_csv[row_index][WEIGHT_POSITION_IN_TABLE] == weight and
                    self._table_csv[row_index][MODE_POSITION_IN_TABLE] == mode and
                    self._table_csv[row_index][INFERENCE_POSITION_IN_TABLE] == framework):
                if self._table_csv[row_index][STATUS_POSITION_IN_TABLE] == 'Failed':
                    return '-'
                else:
                    return self._table_csv[row_index][FPS_POSITION_IN_TABLE]
        return 'N/A'

    def _added_all_test(self, models_dict):
        for infr in self._column_dict:
            for framework in self._column_dict[infr]:
                for plugin in self._column_dict[infr][framework]:
                    weights = self._column_dict[infr][framework][plugin]
                    self._column_dict[infr][framework][plugin] = {weight: {} for weight in weights}
                    for weight in weights:
                        for model in models_dict:
                            self._column_dict[infr][framework][plugin][weight][model] = {}
                            for batch in models_dict[model]['batch']:
                                self._column_dict[infr][framework][plugin][weight][model][batch] = {}
                                self._column_dict[infr][framework][plugin][weight][model][batch]['sync'] = \
                                    self.__find_test_in_table(infr, plugin, model, framework, batch, weight, 'Sync')
                                self._column_dict[infr][framework][plugin][weight][model][batch]['async'] = \
                                    self.__find_test_in_table(infr, plugin, model, framework, batch, weight, 'Async')

    def create_table_header(self):
        self._table_html.append('\n<table align="center" border="1" cellspacing="0" cellpadding="0" class="main">')
        self._table_html.append('\n<tr>\n<th>Task type</th>\n<th>Topology name</th>\n<th>Framework</th>\n<th>Input blob sizes</th>\n<th>Batch size</th>\n')  # pylint: disable=line-too-long  # noqa: E501
        for infrastr in self._column_dict:
            self._table_html.append('<th> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
            self._table_html.append('<tr>\n<th>{}</th>\n</tr>'.format(infrastr))
            self._table_html.append('\n<tr>\n<td> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n<tr>')  # pylint: disable=line-too-long  # noqa: E501
            for framework in self._column_dict[infrastr]:
                self._table_html.append('<th> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="{}">\n<tr>')  # pylint: disable=line-too-long  # noqa: E501
                self._table_html.append('\n<th>{}</th></tr><tr>'.format(framework))
                self._table_html.append('<td> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n<tr>')  # pylint: disable=line-too-long  # noqa: E501
                for plugin in self._column_dict[infrastr][framework]:
                    supported_mode = HTMLBenchmarkTable.get_supported_mode(plugin)
                    table_header_class = "standard_table" if (supported_mode == 'ALL' and len(
                        self._column_dict[infrastr][framework]) > 1) else "one_type_table"
                    self._table_html.append('<th> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="{}">\n<tr>'.format(table_header_class))  # pylint: disable=line-too-long  # noqa: E501
                    self._table_html.append('\n<th>{}</th>\n</tr>\n<tr>\n'.format(plugin))
                    self._table_html.append('<td> <table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="{}">\n<tr>'.format(table_header_class))  # pylint: disable=line-too-long  # noqa: E501
                    for weight in self._column_dict[infrastr][framework][plugin]:
                        table_class = "standard_table" if supported_mode == 'ALL' else "one_type_table"
                        self._table_html.append('<th><table align="center" width="100%" border="1" cellspacing="0" cellpadding="0" class="{}">\n'.format(table_class))  # pylint: disable=line-too-long  # noqa: E501
                        self._table_html.append('<tr><th colspan="2">{}</th>\n</tr>'.format(weight))
                        if supported_mode == 'ALL':
                            self._table_html.append('<tr><th class="double">Latency Mode</th>\n')
                            self._table_html.append('<th class="double">Throughput Mode</th></tr>\n</table></th>')
                        elif supported_mode == 'SYNC':
                            self._table_html.append('<tr>\n<th>Latency<br>Mode</th>\n</tr></table></th>\n')
                        elif supported_mode == 'ASYNC':
                            self._table_html.append('<tr><th>Throughput<br>Mode</th>\n</tr>\n</table></th>')
                    self._table_html.append('</tr></table></td></tr>\n</table>\n</th>')
                self._table_html.append('\n</tr></table></td></tr>\n</table>\n</th>\n')
            self._table_html.append('</tr>\n</table></td></tr>')
            # END of one ifr table
            self._table_html.append('\n</table>\n</th>\n')
        self._table_html.append('</tr>\n')

    def write_test_results(self):
        pass
        for task_type in self._task_types_dict:
            self._table_html.append('\n<tr>')
            self._table_html.append('<td>{}</td>'.format(task_type))

            # Print models
            self._table_html.append('<td> <table align="center" class="lock" height="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr><td>\n<table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
                self._table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(model))
            self._table_html.append('</table>\n</td>')

            # Print framework
            self._table_html.append('<td> <table align="center" class="lock" height="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr><td>\n<table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
                self._table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(
                    self._task_types_dict[task_type][model]['framework'])
                )
            self._table_html.append('</table>\n</td>')

            # Print shape
            self._table_html.append('<td> <table align="center" class="lock" height="100%" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr><td>\n<table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
                self._table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(
                    self._task_types_dict[task_type][model]['shape'])
                )
            self._table_html.append('</table>\n</td>')

            # Print batch
            self._table_html.append('<td > <table align="center" class="lock" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
            for model in self._task_types_dict[task_type]:
                self._table_html.append('<tr>\n <td> <table align="center" class="border_columns" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
                for batch in self._task_types_dict[task_type][model]['batch']:
                    self._table_html.append('<tr>\n<td align="right">{}</td>\n</tr>\n'.format(batch))
                self._table_html.append('</table>\n</td></tr>')
            self._table_html.append('</table>\n</td>')

            # Print result
            for infrastr in self._column_dict:
                self._table_html.append('<td> <table align="center" class="lock" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
                for model in self._task_types_dict[task_type]:
                    self._table_html.append('<tr>\n<td> <table align="center" class="lock" border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')  # pylint: disable=line-too-long  # noqa: E501
                    for framework in self._column_dict[infrastr]:
                        for plugin in self._column_dict[infrastr][framework]:
                            for weight in self._column_dict[infrastr][framework][plugin]:
                                self._table_html.append('<td height="120px"> <table align="center" class="result_column" border="1" cellspacing="0" cellpadding="0" class="standard_table">')  # pylint: disable=line-too-long  # noqa: E501
                                for batch in self._task_types_dict[task_type][model]['batch']:
                                    supported_mode = HTMLBenchmarkTable.get_supported_mode(plugin)
                                    table_class = "standard_table" if supported_mode == 'ALL' else "one_type_table"
                                    self._table_html.append('\n<tr><td> <table align="center" border="1" cellspacing="0" cellpadding="0" class="{}">\n'.format(table_class))  # pylint: disable=line-too-long  # noqa: E501
                                    if supported_mode == 'ALL':
                                        self._table_html.append(
                                            '<tr>\n<td class="double" align="right">{}</td>\n'.format(
                                                self._column_dict[infrastr][framework][plugin][weight][
                                                    model][batch]['sync']))
                                        self._table_html.append(
                                            '<td class="double" align="right">{}</td>\n</tr>'.format(
                                                self._column_dict[infrastr][framework][plugin][weight][
                                                    model][batch]['async']))
                                    elif supported_mode == 'SYNC':
                                        self._table_html.append(
                                            '<tr>\n<td class="double" align="right">{}</td>\n</tr>'.format(
                                                self._column_dict[infrastr][framework][plugin][weight][
                                                    model][batch]['sync']))
                                    elif supported_mode == 'ASYNC':
                                        self._table_html.append(
                                            '<tr><td class="double" align="right">{}</td>\n</tr>'.format(
                                                self._column_dict[infrastr][framework][plugin][weight][
                                                    model][batch]['async']))
                                    self._table_html.append('\n</table></td>\n</tr>')
                                self._table_html.append('</table>\n</td>')
                    self._table_html.append('</table>\n</td>\n</tr>')
                self._table_html.append('</table>\n</td>')
            self._table_html.append('\n</tr>')
