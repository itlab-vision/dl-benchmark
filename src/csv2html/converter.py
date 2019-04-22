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

def find_machine_count(table_csv):
    infr_list = []
    for row_index in range(1, len(table_csv)):
        infr_list.append(table_csv[row_index][6])
    machine_list = set(infr_list)        
    return list(machine_list)

def create_table_header(infr_list, table_html):
    table_html.append('<table align="center" border="1"' +
        'cellspacing="0" cellpadding="0" class="main">')
    table_html.append('<tr><th>Topology</th>')
    for infrastr in infr_list:
        table_html.append('<td>{}<td>'.format(infrastr))
    table_html.append('</tr>')

def find_all_model_tests(model, infrastr, table_csv):
    test_list = []
    for row_index in range(1, len(table_csv)):
        if (table_csv[row_index][6] == infrastr and
            table_csv[row_index][0] == model):
            test_list.append(table_csv[row_index])
    return test_list
    
def write_all_invariants(infr_list, table_csv, table_html):
    table_html.append('<tr><td></td>')
    for infrastr in infr_list:
        test_list = find_all_model_tests(table_csv[1][0], infrastr, table_csv)
        table_html.append('<tb><table align="center" width="100%"' + 
            'border="1" cellspacing="0" cellpadding="0"><tr>')
        for test in test_list:
            table_html.append('<td>{};{};{};{};{};</td>'.format(test[1],
                test[2], test[3], test[4], test[5]))
        table_html.append('</tr><tr>')
        for i in range(len(test_list)):
            table_html.append('<td><table align="center" width="100%"' + 
                'border="1" cellspacing="0" cellpadding="0">' + 
                '<tr><th class="double">Time, s</th>' + 
                '<th class="double">FPS</th></tr></table></td>')
        table_html.append('</table></td>')
    table_html.append('</tr>')

def convert_csv_table_to_html(table_csv):
    table_html = []
    add_styles_to_table(table_html)
    machine_list = find_machine_count(table_csv)
    create_table_header(machine_list, table_html)
    write_all_invariants(machine_list, table_csv, table_html)
    #table_headers = table_csv[0].split(';')
    #table_html = PT(table_headers)
    #for row_index in range(1, len(table_csv)):
    #    curr_row = table_csv[row_index].split(';')[:-1]
    #    table_html.add_row(curr_row)
    table_html.append('</table')
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
    html_ = fromstring("".join(table_html))
    print(table_html)
    #save_html_table(table_html, path_table_html)


if __name__ == '__main__':
    sys.exit(main() or 0)