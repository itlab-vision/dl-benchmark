from copy import deepcopy
INFR_POSITION_IN_TABLE = 8
MODEL_POSITION_IN_TABLE = 1
ATOSP_POSITION_IN_TABLE = 9
LATENCY_POSITION_IN_TABLE = 10
FPS_POSITION_IN_TABLE = 11


class HTMLTable:
    def __init__(self, _table_csv):
        self.table_html = []
        self.table_csv = _table_csv

    def add_styles_to_table(self, path_to_styles):
        styles = open(path_to_styles, 'r')
        for line in styles:    
            self.table_html.append(line)

    def find_all_infr(self):
        infr_list = []
        for row_index in range(1, len(self.table_csv)):
            infr_list.append(self.table_csv[row_index][INFR_POSITION_IN_TABLE])
        infr_list = set(infr_list)
        return list(infr_list)

    def get_all_models_names(self):
        models_set = set()
        for row_index in range(1, len(self.table_csv)):
            models_set.add(self.table_csv[row_index][MODEL_POSITION_IN_TABLE])
        return models_set

    def prep_tests(self, tests):
        max_len = -1
        first_tests = None
        for test_tuple in tests:
            if (len(test_tuple[1]) > max_len):
                first_tests = test_tuple[1]
                max_len = len(test_tuple[1])

        for curr_model in range(0, len(tests)):
            for curr_test in range(len(first_tests)):
                i = 0
                while (i <  len(tests[curr_model][1])):
                    if (first_tests[curr_test][4:9] ==
                        tests[curr_model][1][i][4:9]):
                        (tests[curr_model][1][i], \
                        tests[curr_model][1][curr_test]) = \
                        (tests[curr_model][1][curr_test], \
                        tests[curr_model][1][i])
                    i += 1
                else:
                    if (len(tests[curr_model][1]) < curr_test):
                        tests[curr_model][1].append(
                            deepcopy(tests[curr_model][1][curr_test]))
                        tests[curr_model][1][curr_test] = \
                            deepcopy(first_tests[curr_test])
                        tests[curr_model][1][curr_test][MODEL_POSITION_IN_TABLE] = \
                            tests[curr_model][MODEL_POSITION_IN_TABLE]
                        tests[curr_model][1][curr_test][ATOSP_POSITION_IN_TABLE] = \
                            '-'
                        tests[curr_model][1][curr_test][LATENCY_POSITION_IN_TABLE] = \
                            '-'
                        tests[curr_model][1][curr_test][FPS_POSITION_IN_TABLE] = \
                            '-'
                    elif (len(tests[curr_model][1]) < len(first_tests)):
                        tests[curr_model][1].append(
                            deepcopy(first_tests[curr_test]))
                        tests[curr_model][1][-1][MODEL_POSITION_IN_TABLE] = \
                            tests[curr_model][1][0][MODEL_POSITION_IN_TABLE]
                        tests[curr_model][1][-1][ATOSP_POSITION_IN_TABLE] = \
                            '-'
                        tests[curr_model][1][-1][LATENCY_POSITION_IN_TABLE] = \
                            '-'
                        tests[curr_model][1][-1][FPS_POSITION_IN_TABLE] = \
                            '-'
            if (len(tests[curr_model][1]) != len(first_tests)):
                print(len(tests[curr_model][1]), len(first_tests))

    def sort_all_tests(self):
        infr_list = self.find_all_infr()
        self.sorted_tests = [(infrastr, []) for infrastr in infr_list]
        models_set = list(self.get_all_models_names())
        unused_models = []

        for i, infrastr in enumerate(infr_list):
            unused_models.clear()
            for model in models_set:
                model_tests = self.find_all_model_tests(model,
                    infrastr)
                if (len(model_tests) > 0):
                    self.sorted_tests[i][1].append((model, model_tests))
                else:
                    unused_models.append(model)
            for model in unused_models:
                copy_model_tests = deepcopy(self.sorted_tests[i][1][1][1])
                for test in copy_model_tests:
                    test[1] = model
                    test[ATOSP_POSITION_IN_TABLE] = '-'
                    test[LATENCY_POSITION_IN_TABLE] = '-'
                    test[FPS_POSITION_IN_TABLE] = '-'
                self.sorted_tests[i][1].append((model, copy_model_tests))
            self.prep_tests(self.sorted_tests[i][1])

    def find_all_model_tests(self, model, infrastr):
        # If infr and model == test.infr and test.model than add test in pack
        test_list = []
        for row_index in range(1, len(self.table_csv)):
            if (self.table_csv[row_index][INFR_POSITION_IN_TABLE] == infrastr
                and
                self.table_csv[row_index][MODEL_POSITION_IN_TABLE] == model):
                test_list.append(self.table_csv[row_index])
        return test_list

    def create_table_header(self):
        self.table_html.append('\n<table align="center" border="1"' +
            'cellspacing="0" cellpadding="0" class="main">')
        self.table_html.append('\n<tr>\n<th>Topology</th>\n')
        for infrastr in self.sorted_tests:
            self.table_html.append('<th>{}</th>\n'.format(infrastr[0]))
        self.table_html.append('</tr>\n')

    def write_all_invariants(self):
        self.table_html.append('\n<tr>\n<td>\n</td>\n')
        for infrastr in self.sorted_tests:
            self.table_html.append('<td>\n<table align="center" width="100%"' +
            'border="1" cellspacing="0" cellpadding="0">\n<tr>\n')
            for test in infrastr[1][0][1]:
                test[7] = test[7].replace(',', '<br>')
                self.table_html.append(('<th>{};{};{};<br>{}</th>\n')
                .format(test[4], test[5], test[6], test[7]))
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
                            if (test[6] == 'Sync'):
                                result = test[ATOSP_POSITION_IN_TABLE:FPS_POSITION_IN_TABLE + 1]
                            else:
                                result = test[ATOSP_POSITION_IN_TABLE:FPS_POSITION_IN_TABLE + 1:2]
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