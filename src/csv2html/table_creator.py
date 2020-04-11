from copy import deepcopy
import yaml

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

class HTMLTable:
    def __init__(self, _table_csv, _file):
        self.table_html = []
        self.table_csv = _table_csv
        self.frameworks_list = yaml.safe_load(_file)['frameworks']

    @staticmethod
    def get_supported_mode(plugin):
        if plugin == 'CPU':
            return 'ALL'
        elif plugin == 'GPU':
            return 'SYNC'
        else:
            return 'ASYNC'

    def add_styles_to_table(self, path_to_styles):
        styles = open(path_to_styles, 'r')
        for line in styles:
            self.table_html.append(line)

    def get_model_dict(self):
        models_dict = dict()
        for row_index in range(1, len(self.table_csv)):
            try:
                models_dict[self.table_csv[row_index][MODEL_POSITION_IN_TABLE]]
            except KeyError:
                models_dict[self.table_csv[row_index][MODEL_POSITION_IN_TABLE]] = {
                    'weight': set(),
                    'shape': self.table_csv[row_index][SHAPE_POSITION_IN_TABLE],
                    'batch': set(),
                    'type': self.table_csv[row_index][TYPE_POSITION_IN_TABLE],
                    'framework' : self.table_csv[row_index][FRAMEWORK_POSITION_IN_TABLE]
                }
        return models_dict

    def get_model_weights_and_batches(self, models_dict):
        #Added to dict all weights and batch.
        for row_index in range(1, len(self.table_csv)):
            models_dict[self.table_csv[row_index][MODEL_POSITION_IN_TABLE]]['weight'].add(
                self.table_csv[row_index][WEIGHT_POSITION_IN_TABLE])
            models_dict[self.table_csv[row_index][MODEL_POSITION_IN_TABLE]]['batch'].add(
                self.table_csv[row_index][BATCH_POSITION_IN_TABLE])

        #Sort all batches, because they added in set randomly.
        for model in models_dict:
            models_dict[model]['batch'] =  \
                sorted(models_dict[model]['batch'], key=lambda val: int(val))

    def format_models_dict(self, models_dict):
        task_types_dict = dict()
        for model in models_dict:
            try:
                task_types_dict[models_dict[model]['type']][model] = models_dict[model]
            except KeyError:
                task_types_dict[models_dict[model]['type']] = { model: models_dict[model] }

        return task_types_dict

    def find_plugin_in_infr(self, plugin, target_infr):
        for row_index in range(1, len(self.table_csv)):
            if (plugin in self.table_csv[row_index][PARAMS_POSITION_IN_TABLE] and
                target_infr == self.table_csv[row_index][INFR_POSITION_IN_TABLE]):
                return True
        return False

    def get_infr_dict(self):
        infr_dict = dict()
        for row_index in range(1, len(self.table_csv)):
            try:
                infr_dict[self.table_csv[row_index][INFR_POSITION_IN_TABLE]]
            except KeyError:
                #Added to each intr all frameworks with target plugins.
                infr_dict[self.table_csv[row_index][INFR_POSITION_IN_TABLE]] = {}
                for framework in self.frameworks_list:
                    infr_dict[self.table_csv[row_index][INFR_POSITION_IN_TABLE]][framework['name']] = {}
                    for plagin in framework:
                        if plagin == 'name':
                            continue
                        if self.find_plugin_in_infr(plagin, self.table_csv[row_index][INFR_POSITION_IN_TABLE]):
                            infr_dict[self.table_csv[row_index][INFR_POSITION_IN_TABLE]][framework['name']][plagin] = \
                                framework[plagin].replace(' ', '').split(',')

        return infr_dict

    def find_test_in_table(self, curr_infr, plagin, model_name, framework, batch, weight, mode):
        for row_index in range(1, len(self.table_csv)):
            if (self.table_csv[row_index][MODEL_POSITION_IN_TABLE] == model_name and
                self.table_csv[row_index][INFR_POSITION_IN_TABLE] == curr_infr and
                plagin in self.table_csv[row_index][PARAMS_POSITION_IN_TABLE] and
                self.table_csv[row_index][BATCH_POSITION_IN_TABLE] == batch and
                self.table_csv[row_index][WEIGHT_POSITION_IN_TABLE] == weight and
                self.table_csv[row_index][MODE_POSITION_IN_TABLE] == mode and
                self.table_csv[row_index][INFERENCE_POSITION_IN_TABLE] == framework):
                if self.table_csv[row_index][STATUS_POSITION_IN_TABLE] == 'Failed':
                    return '-'
                else:
                    return self.table_csv[row_index][FPS_POSITION_IN_TABLE]

        return 'N/A'

    def added_all_test(self, models_dict):
        for infr in self.infr_dict:
            for framework in self.infr_dict[infr]:
                for plagin in self.infr_dict[infr][framework]:
                    weights = self.infr_dict[infr][framework][plagin]
                    self.infr_dict[infr][framework][plagin] = {weight:{} for weight in weights}
                    for weight in weights:
                        for model in models_dict:
                            self.infr_dict[infr][framework][plagin][weight][model] = {}
                            for batch in models_dict[model]['batch']:
                                self.infr_dict[infr][framework][plagin][weight][model][batch] = {}
                                self.infr_dict[infr][framework][plagin][weight][model][batch]['sync'] = \
                                    self.find_test_in_table(infr, plagin, model, framework, batch, weight, 'Sync')
                                self.infr_dict[infr][framework][plagin][weight][model][batch]['async'] = \
                                    self.find_test_in_table(infr, plagin, model, framework, batch, weight, 'Async')

    def sort_all_tests(self):
        models_dict = self.get_model_dict()
        self.get_model_weights_and_batches(models_dict)
        self.task_types_dict = self.format_models_dict(models_dict)
        self.infr_dict = self.get_infr_dict()
        self.added_all_test(models_dict)

    def create_table_header(self):
        self.table_html.append('\n<table align="center" border="1"' +
            'cellspacing="0" cellpadding="0" class="main">')
        self.table_html.append('\n<tr>\n<th>Task type</th>\n'\
            '<th>Topology name</th>\n<th>Framework</th>\n'\
            '<th>Input blob sizes</th>\n<th>Batch size</th>\n')
        for infrastr in self.infr_dict:
            self.table_html.append('<th> <table align="center" width="100%"' +
                'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            self.table_html.append('<tr>\n<th>{}</th>\n</tr>'.format(infrastr))
            self.table_html.append('\n<tr>\n<td> <table align="center" width="100%"' +
                'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n<tr>')
            for framework in self.infr_dict[infrastr]:
                self.table_html.append('<th> <table align="center" width="100%"' +
                        'border="1" cellspacing="0" cellpadding="0" class="{}">\n<tr>')
                self.table_html.append('\n<th>{}</th></tr><tr>'.format(framework))
                self.table_html.append('<td> <table align="center" width="100%"' +
                        'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n<tr>')
                for plugin in self.infr_dict[infrastr][framework]:
                    supported_mode = HTMLTable.get_supported_mode(plugin)
                    table_header_class = "standard_table" if (supported_mode == 'ALL' and
                        len(self.infr_dict[infrastr][framework]) > 1)  else "one_type_table"
                    self.table_html.append('<th> <table align="center" width="100%"' +
                        'border="1" cellspacing="0" cellpadding="0" class="{}">\n<tr>'.format(table_header_class))
                    self.table_html.append('\n<th>{}</th>\n</tr>\n<tr>\n'.format(plugin))
                    self.table_html.append('<td> <table align="center" width="100%"' +
                        'border="1" cellspacing="0" cellpadding="0" class="{}">\n<tr>'.format(table_header_class))
                    for weight in self.infr_dict[infrastr][framework][plugin]:
                        table_class = "standard_table" if supported_mode == 'ALL' else "one_type_table"
                        self.table_html.append('<th><table align="center" width="100%"' +
                        'border="1" cellspacing="0" cellpadding="0" class="{}">\n'.format(table_class))
                        self.table_html.append('<tr><th colspan="2">{}</th>\n</tr>'.format(weight))
                        if supported_mode == 'ALL':
                            self.table_html.append('<tr><th class="double">Latency Mode</th>\n')
                            self.table_html.append('<th class="double">Throughput Mode</th></tr>\n</table></th>')
                        elif supported_mode == 'SYNC':
                            self.table_html.append('<tr>\n<th>Latency<br>Mode</th>\n</tr></table></th>\n')
                        elif supported_mode == 'ASYNC':
                            self.table_html.append('<tr><th>Throughput<br>Mode</th>\n</tr>\n</table></th>')

                    self.table_html.append('</tr></table></td></tr>\n</table>\n</th>')
                self.table_html.append('\n</tr></table></td></tr>\n</table>\n</th>\n')
            self.table_html.append('</tr>\n</table></td></tr>')
            #END of one ifr table
            self.table_html.append('\n</table>\n</th>\n')
        self.table_html.append('</tr>\n')

    def write_test_results(self):
        pass
        for task_type in self.task_types_dict:
            self.table_html.append('\n<tr>')
            self.table_html.append('<td>{}</td>'.format(task_type))

            #Print models
            self.table_html.append('<td> <table align="center" class="lock" height="100%"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self.task_types_dict[task_type]:
                self.table_html.append('<tr><td>\n<table align="center" class="border_columns"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                self.table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(model))
            self.table_html.append('</table>\n</td>')

            #Print framework
            self.table_html.append('<td> <table align="center" class="lock" height="100%"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self.task_types_dict[task_type]:
                self.table_html.append('<tr><td>\n<table align="center" class="border_columns"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                self.table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(
                    self.task_types_dict[task_type][model]['framework']))
            self.table_html.append('</table>\n</td>')

            #Print shape
            self.table_html.append('<td> <table align="center" class="lock" height="100%"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self.task_types_dict[task_type]:
                self.table_html.append('<tr><td>\n<table align="center" class="border_columns"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                self.table_html.append('<tr><td align="left">{}</td>\n</tr>\n</table></td></tr>'.format(
                    self.task_types_dict[task_type][model]['shape']))
            self.table_html.append('</table>\n</td>')

            #Print batch
            self.table_html.append('<td > <table align="center" class="lock"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
            for model in self.task_types_dict[task_type]:
                self.table_html.append('<tr>\n <td> <table align="center" class="border_columns"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                for batch in self.task_types_dict[task_type][model]['batch']:
                    self.table_html.append('<tr>\n<td align="right">{}</td>\n</tr>\n'.format(batch))
                self.table_html.append('</table>\n</td></tr>')
            self.table_html.append('</table>\n</td>')

            # Print result
            for infrastr in self.infr_dict:
                self.table_html.append('<td> <table align="center" class="lock"' +
                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                for model in self.task_types_dict[task_type]:
                    self.table_html.append('<tr>\n<td> <table align="center" class="lock"' +
                        'border="1" cellspacing="0" cellpadding="0" class="standard_table">\n')
                    for framework in self.infr_dict[infrastr]:
                        for plugin in self.infr_dict[infrastr][framework]:
                            for weight in self.infr_dict[infrastr][framework][plugin]:
                                self.table_html.append('<td height="120px"> <table align="center" class="result_column"' +
                                    'border="1" cellspacing="0" cellpadding="0" class="standard_table">')
                                for batch in self.task_types_dict[task_type][model]['batch']:
                                    supported_mode = HTMLTable.get_supported_mode(plugin)
                                    table_class = "standard_table" if supported_mode == 'ALL' else "one_type_table"
                                    self.table_html.append('\n<tr><td> <table align="center"' +
                                        'border="1" cellspacing="0" cellpadding="0" class="{}">\n'.format(table_class))
                                    if supported_mode == 'ALL':
                                        self.table_html.append('<tr>\n<td class="double" align="right">{}</td>\n'.format(
                                            self.infr_dict[infrastr][framework][plugin][weight][model][batch]['sync']))
                                        self.table_html.append('<td class="double" align="right">{}</td>\n</tr>'.format(
                                            self.infr_dict[infrastr][framework][plugin][weight][model][batch]['async']))
                                    elif supported_mode == 'SYNC':
                                        self.table_html.append('<tr>\n<td class="double" align="right">{}</td>\n</tr>'.format(
                                            self.infr_dict[infrastr][framework][plugin][weight][model][batch]['sync']))
                                    elif supported_mode == 'ASYNC':
                                       self.table_html.append('<tr><td class="double" align="right">{}</td>\n</tr>'.format(
                                            self.infr_dict[infrastr][framework][plugin][weight][model][batch]['async']))

                                    self.table_html.append('\n</table></td>\n</tr>')
                                self.table_html.append('</table>\n</td>')
                    self.table_html.append('</table>\n</td>\n</tr>')
                self.table_html.append('</table>\n</td>')

            self.table_html.append('\n</tr>')

    def save_html_table(self, path_table_html):
        fileHTML = open(path_table_html, 'w')
        self.table_html.append('</table>')
        for line in self.table_html:
            fileHTML.write(line)