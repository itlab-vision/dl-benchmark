import argparse
import sys
from pathlib import Path

from accuracy_checker_table_creator import HTMLAccuracyCheckerTable
from benchmark_table_creator import HTMLBenchmarkTable


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--tables',
                        type=str,
                        help='Paths to the inference tables in csv format.',
                        nargs='+',
                        required=True)
    parser.add_argument('-r', '--result_table',
                        type=str,
                        help='Full name of the resulting file',
                        required=True)
    parser.add_argument('-k', '--table_kind',
                        type=str,
                        help='Kind of table: ',
                        choices=['benchmark', 'accuracy_checker'],
                        default='benchmark',
                        required=True)

    args = parser.parse_args()

    return args


def open_csv_table(path_table_csv):
    table_csv = []
    for table in path_table_csv:
        if not Path(table).is_file():
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
        table_csv[row_index] = [field.strip('"') for field in table_csv[row_index].split(';')]


def convert_csv_table_to_html(table_csv, table_type):
    table_html = None
    framework_config = open('frameworks.yml', 'r')
    if table_type == 'benchmark':
        table_html = HTMLBenchmarkTable(table_csv, framework_config)
    elif table_type == 'accuracy_checker':
        table_html = HTMLAccuracyCheckerTable(table_csv, framework_config)

    path_to_styles = Path(__file__).resolve().parent.joinpath('styles.html')
    table_html.add_styles_to_table(path_to_styles)
    table_html.sort_all_tests()
    table_html.create_table_header()
    table_html.write_test_results()

    return table_html


def main():
    args = cli_argument_parser()

    table_csv = open_csv_table(args.tables)
    split_table(table_csv)
    table_html = convert_csv_table_to_html(table_csv, args.table_kind)
    if table_html is None:
        return 1
    table_html.save_html_table(args.result_table)


if __name__ == '__main__':
    sys.exit(main() or 0)
