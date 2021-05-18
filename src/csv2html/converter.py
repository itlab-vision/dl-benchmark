import sys
import argparse
import os
from benchmark_table_creator import HTMLBenchmarkTable
from accuracy_checker_table_creator import HTMLAccuracyCheckerTable


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tables', type=str, help='Paths to the inference tables in csv format.', nargs='+', required=True)
    parser.add_argument('-r', '--result_table', type=str, help='Full name of the resulting file', required=True)
    parser.add_argument('-k', '--table_kind', type=str, help='Kind of table: ', choices=['benchmark', 'accuracy_checker'],
                        default='benchmark', required=True)
    path_table_csv = parser.parse_args().tables
    path_table_html = parser.parse_args().result_table
    table_kind = parser.parse_args().table_kind
    return path_table_csv, path_table_html, table_kind


def open_csv_table(path_table_csv):
    table_csv = []
    for table in path_table_csv:
        if not os.path.isfile(table):
            raise ValueError('Wrong path the table!')
        with open(table) as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if i == 0 and len(table_csv) != 0:
                    continue
                table_csv.append(line)
            file.close()
    return table_csv


def split_table(table_csv):
    for row_index in range(len(table_csv)):
        table_csv[row_index] = table_csv[row_index].split(';')


def convert_csv_table_to_html(table_csv, table_type):
    framework_config = open('frameworks.yml', 'r')
    if table_type == 'benchmark':
        table_html = HTMLBenchmarkTable(table_csv, framework_config)
    elif table_type == 'accuracy_checker':
        table_html = HTMLAccuracyCheckerTable(table_csv, framework_config)
    script_dir = os.path.split(os.path.abspath(__file__))[0]
    path_to_styles = os.path.join(script_dir, 'styles.html')
    table_html.add_styles_to_table(path_to_styles)
    table_html.sort_all_tests()
    table_html.create_table_header()
    table_html.write_test_results()
    return table_html


def main():
    path_table_csv, path_table_html, table_type = build_parser()
    table_csv = open_csv_table(path_table_csv)
    split_table(table_csv)
    table_html = convert_csv_table_to_html(table_csv, table_type)
    table_html.save_html_table(path_table_html)


if __name__ == '__main__':
    sys.exit(main() or 0)
