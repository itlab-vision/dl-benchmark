from table_creator import HTMLTable
import sys
import argparse
import os


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--table', type=str, help='Path to the inference table in csv format.', required=True)
    parser.add_argument('-r', '--result_table', type=str, help='Full name of the resulting file', required=True)
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


def convert_csv_table_to_html(table_csv):
    framework_config = open('frameworks.yml', 'r')
    table_html = HTMLTable(table_csv, framework_config)
    script_dir = os.path.split(os.path.abspath(__file__))[0]
    path_to_styles = os.path.join(script_dir, 'styles.html')
    table_html.add_styles_to_table(path_to_styles)
    table_html.sort_all_tests()
    table_html.create_table_header()
    table_html.write_test_results()
    return table_html


def main():
    path_table_csv, path_table_html = build_parser()
    table_csv = open_csv_table(path_table_csv)
    split_table(table_csv)
    table_html = convert_csv_table_to_html(table_csv)
    table_html.save_html_table(path_table_html)


if __name__ == '__main__':
    sys.exit(main() or 0)
