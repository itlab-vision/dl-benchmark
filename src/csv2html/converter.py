from prettytable import PrettyTable as PT
from lxml.html import fromstring, tostring
import sys
import argparse
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--table', type = str,
        help = 'Path to the inference table in csv format.', required = True)
    parser.add_argument('-r', '--result_table', type = str,
        help = 'Full name of the resulting file', required = True)
    path_table_csv = parser.parse_args().table
    path_table_html = parser.parse_args().result_table
    return path_table_csv, path_table_html

def open_csv_table(path_table_csv):
    if not os.path.isfile(path_table_csv):
        raise ValueError('Wrong path the inference table!')
    with open(path_table_csv) as file:
        table_csv = file.readlines()
        file.close()
    return table_csv

def split_table(table_csv):
    for row_index in range(len(table_csv)):
        table_csv[row_index] = table_csv[row_index].split(';')

def add_styles_to_table(table_html):
    script_dir = os.path.split(os.path.abspath(__file__))[0]
    path_to_styles = os.path.join(script_dir, 'styles.html')   
    styles = open(path_to_styles, 'r')
    for line in styles:    
        table_html.append(line)

def find_all_infr(table_csv):
    infr_list = []
    for row_index in range(1, len(table_csv)):
        infr_list.append(table_csv[row_index][6])
    infr_list = set(infr_list)        
    return list(infr_list)

def create_table_header(sorted_tests, table_html):
    table_html.append('\n<table align="center" border="1"' +
        'cellspacing="0" cellpadding="0" class="main">')
    table_html.append('\n<tr>\n<th>Topology</th>\n')
    for infrastr in sorted_tests:
        table_html.append('<th>{}</th>\n'.format(infrastr[0]))
    table_html.append('</tr>\n')

def find_all_model_tests(model, infrastr, table_csv):
    test_list = []
    for row_index in range(1, len(table_csv)):
        if (table_csv[row_index][6] == infrastr and
            table_csv[row_index][0] == model):
            test_list.append(table_csv[row_index])
    return test_list

def get_all_models_names(table_csv):
    models_set = set()
    for row_index in range(1, len(table_csv)):
        models_set.add(table_csv[row_index][0])
    return models_set

def prep_tests(tests):
    first_tests = tests[0][1]
    for curr_model in range(1, len(tests)):
        for curr_test in range(len(tests[curr_model][1])):
            for i in range(len(tests[curr_model][1])):
                if (first_tests[curr_test][1:6] == tests[curr_model][1][i][1:6]):
                    tests[curr_model][1][i], tests[curr_model][1][curr_test] = tests[curr_model][1][curr_test], tests[curr_model][1][i]

def get_sorted_test(infr_list, table_csv):
    sorted_tests = [(infrastr, []) for infrastr in infr_list]
    models_set = list(get_all_models_names(table_csv))

    for i, infrastr in enumerate(infr_list): 
        for model in models_set:
            model_tests = find_all_model_tests(model,
                infrastr, table_csv)
            if (len(model_tests) > 0):
                sorted_tests[i][1].append((model, model_tests))
        prep_tests(sorted_tests[i][1])
    return sorted_tests    

def write_all_invariants(sorted_tests, table_html):
    table_html.append('\n<tr>\n<td>\n</td>\n')
    for infrastr in sorted_tests:
        table_html.append('<td>\n<table align="center" width="100%"' + 
            'border="1" cellspacing="0" cellpadding="0">\n<tr>\n')
        for test in infrastr[1][0][1]:
            table_html.append('<th>{};{};{};{};{};</th>\n'.format(test[1],
                test[2], test[3], test[4], test[5]))
        table_html.append('</tr>\n<tr>')
        for i in range(len(infrastr[1][0][1])):
            table_html.append('\n<td>\n<table align="center" width="100%"' + 
                'border="1" cellspacing="0" cellpadding="0">' + 
                '\n<tr>\n<th class="double">Time, s</th>\n' + 
                '<th class="double">FPS</th>\n</tr>\n</table>\n</td>\n')
        table_html.append('\n</table>\n</td>')
    table_html.append('\n</tr>')

def write_test_results(infr_list, table_csv, table_html):
    models_set = set()
    used_models = set()
    for row_index in range(1, len(table_csv)):
        models_set.add(table_csv[row_index][0])
    '''Создать список всех тестов для каждой инфраструктуры
чтоб суметь сделать!!!!!!'''

def convert_csv_table_to_html(table_csv):
    table_html = []
    add_styles_to_table(table_html)
    infr_list = find_all_infr(table_csv)
    sorted_tests = get_sorted_test(infr_list, table_csv)
    create_table_header(sorted_tests, table_html)
    write_all_invariants(sorted_tests, table_html)
    write_test_results(sorted_tests, table_html)
    return table_html

def save_html_table(table_html, path_table_html):
    table_html = table_html.get_html_string(attributes={"border":"1",
        "align":"center"})
    html_file = open(path_table_html, 'w')
    html_file.write(table_html)

def main():
    path_table_csv, path_table_html = build_parser()
    table_csv = open_csv_table(path_table_csv)
    split_table(table_csv)
    table_html = convert_csv_table_to_html(table_csv)
    file = open('res.html', 'w')
    table_html.append('</table>')
    for line in table_html:
        file.write(line)
    #save_html_table(table_html, path_table_html)


if __name__ == '__main__':
    sys.exit(main() or 0)