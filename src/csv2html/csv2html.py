from prettytable import PrettyTable as PT
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

def convert_csv_table_to_html(table_csv):
    table_headers = table_csv[0].split(';')
    table_html = PT(table_headers)
    for row_index in range(1, len(table_csv)):
        curr_row = table_csv[row_index].split(';')[:-1]
        table_html.add_row(curr_row)
    return table_html

def save_html_table(table_html, path_table_html):
    table_html = table_html.get_html_string()
    html_file = open(path_table_html, 'w')
    html_file.write(table_html)

def main():
    path_table_csv, path_table_html = build_parser()
    table_csv = open_csv_table(path_table_csv)
    table_html = convert_csv_table_to_html(table_csv)
    save_html_table(table_html, path_table_html)


if __name__ == '__main__':
    sys.exit(main() or 0)