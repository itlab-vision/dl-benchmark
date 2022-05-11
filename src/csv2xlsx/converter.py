import sys
import argparse
from benchmark_table_creator import XlsxBenchmarkTable

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tables', type=str, \
                        help='Paths to the inference tables in csv format.', \
                        nargs='+', required=True)
    parser.add_argument('-r', '--result_table', type=str, \
                        help='Full name of the resulting file', required=True)
    parser.add_argument('-k', '--table_kind', type=str, help='Kind of table: ', \
                        choices=['benchmark'], # 'accuracy_checker'
                        default='benchmark', required=True)
    paths_table_csv = parser.parse_args().tables
    path_table_xlsx = parser.parse_args().result_table
    table_kind = parser.parse_args().table_kind
    return paths_table_csv, path_table_xlsx, table_kind


def convert_csv_table_to_xlsx(paths_table_csv, path_table_xlsx, table_type):
    if table_type == 'benchmark':
        table_xlsx = XlsxBenchmarkTable(paths_table_csv, path_table_xlsx)
    elif table_type == 'accuracy_checker':
        raise 'Table type \'{}\' is not supported'.format(table_type)
    table_xlsx.read_csv_table()
    table_xlsx.create_table_header()
    table_xlsx.create_table_rows()
    table_xlsx.write_test_results()
    table_xlsx.close_table()

def main():
    paths_table_csv, path_table_xlsx, table_type = build_parser()
    convert_csv_table_to_xlsx(paths_table_csv, path_table_xlsx, table_type)


if __name__ == '__main__':
    sys.exit(main() or 0)
