from copy import deepcopy
import yaml

STATUS_POSITION_IN_TABLE = 0
TYPE_POSITION_IN_TABLE = 1
MODEL_POSITION_IN_TABLE = 2
FRAMEWORK_POSITION_IN_TABLE = 3
INFERENCE_POSITION_IN_TABLE = 4
SHAPE_POSITION_IN_TABLE = 5
WEIGHT_POSITION_IN_TABLE = 6
BATCH_POSITION_IN_TABLE = 7
MODE_POSITION_IN_TABLE = 8
INFR_POSITION_IN_TABLE = 10
FPS_POSITION_IN_TABLE = 13

class HTMLTable:
    def __init__(self, _table_csv, _file):
        self.table_html = []
        self.table_csv = _table_csv
        self.frameworks_list = yaml.safe_load(_file)['frameworks']

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
                task_types_dict[models_dict[model]['type']]
            except KeyError:
                task_types_dict[models_dict[model]['type']] = { model: models_dict[model] }

        return task_types_dict

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
                        infr_dict[self.table_csv[row_index][INFR_POSITION_IN_TABLE]][framework['name']][plagin] = \
                            framework[plagin].replace(' ', '').split(',')

        return infr_dict

    def find_test_in_table(self, curr_infr, model_name, batch, weight, mode):
        for row_index in range(1, len(self.table_csv)):
            if (self.table_csv[row_index][MODEL_POSITION_IN_TABLE] == model_name and
                self.table_csv[row_index][INFR_POSITION_IN_TABLE] == curr_infr and
                self.table_csv[row_index][BATCH_POSITION_IN_TABLE] == batch and
                self.table_csv[row_index][WEIGHT_POSITION_IN_TABLE] == weight and
                self.table_csv[row_index][MODE_POSITION_IN_TABLE] == mode):
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
                                    self.find_test_in_table(infr, model, batch, weight, 'Sync')
                                self.infr_dict[infr][framework][plagin][weight][model][batch]['async'] = \
                                    self.find_test_in_table(infr, model, batch, weight, 'Async')

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
                'border="1" cellspacing="0" cellpadding="0">\n')
            self.table_html.append('<tr><th>{}</th><tr>\n'.format(infrastr))
            for framework in self.infr_dict[infrastr]:
                self.table_html.append('<tr>\n<td>{}</td>\n'.format(framework))
            self.table_html.append('\n</tr>\n<tr>\n')
            self.table_html.append('<td> <table align="center" width="100%"' +
                'border="1" cellspacing="0" cellpadding="0">\n<tr>')
            for framework in self.infr_dict[infrastr]:
                for plugin in self.infr_dict[infrastr][framework]:
                    self.table_html.append('\n<th>{}</th>\n'.format(plugin))
            self.table_html.append('\n</tr>\n</table>\n</td>\n</tr>\n<tr>')
            for framework in self.infr_dict[infrastr]:
                for plugin in self.infr_dict[infrastr][framework]:
                    self.table_html.append('<td> <table align="center" width="100%"' +
                        'border="1" cellspacing="0" cellpadding="0">\n<tr>')
                    for weight in self.infr_dict[infrastr][framework][plugin]:
                        self.table_html.append('\n<th>{}</th>\n'.format(weight))
                    self.table_html.append('\n</tr>\n</table>\n</td>\n')
            self.table_html.append('\n</tr>')
            #END of one ifr table
            self.table_html.append('\n</th>\n')
        self.table_html.append('</tr>\n')

    def write_all_invariants(self):
        self.table_html.append('\n<tr>\n<td>\n</td>\n')
        for infrastr in self.sorted_tests:
            self.table_html.append('<td>\n<table align="center" width="100%"' +
            'border="1" cellspacing="0" cellpadding="0">\n<tr>\n')
            for test in infrastr[1][0][1]:
                test[5] = test[5].replace(',', '<br>')
                self.table_html.append(('<th>{};{};{};<br>{};{}</th>\n')
                .format(test[1], test[2], test[3], test[4], test[5]))
            self.table_html.append('</tr>\n<tr>')
            for test in infrastr[1][0][1]:
                if (test[4] == 'Sync'):
                    inv = 'Latency'
                else:
                    inv = 'Average time of single pass'
                self.table_html.append(('\n<td>\n<table align="center"' +
                    'width="100%" border="1" cellspacing="0" cellpadding="0">'+
                    '\n<tr>\n<th class="double">{}</th>\n' +
                    '<th class="double">FPS</th>\n</tr>\n</table>\n</td>\n')
                        .format(inv))
            self.table_html.append('\n</tr>\n</table>\n</td>')
        self.table_html.append('\n</tr>')

    def write_test_results(self):
        self.table_html.append('\n<tr>')
        models_set = list(self.get_all_models_names())
        models_set.sort()
        for model in models_set:
            self.table_html.append('\n<td>{}</td>'.format(model))
            for infrastr in self.sorted_tests:
                self.table_html.append('\n<td>\n<table align="center"' +
                'width="100%" border="1" cellspacing="0" cellpadding="0">\n' +
                '<tr>')    
                for curr_model in infrastr[1]:
                    if (curr_model[0] == model):
                        for test in curr_model[1]:
                            if (test[4] == 'Sync'):
                                result = test[8:10]
                            else:
                                result = test[7:10:2]
                            self.table_html.append(('\n<td><table align="center"' +
                                'width="100%" border="1" cellspacing="0"' + 
                                'cellpadding="0">\n<tr>\n<td class="double" align="right">{}' +
                                '</td>\n<td class="double" align="right">{}</td>\n</tr>\n' +
                                '</table>\n</td>\n').format(result[0],
                                result[1]))    
                self.table_html.append('\n</tr>\n</table>\n</td>')
            self.table_html.append('\n</tr>')

    def save_html_table(self, path_table_html):
        fileHTML = open(path_table_html, 'w')
        self.table_html.append('</table>')
        for line in self.table_html:
            fileHTML.write(line)