import csv


class CsvReport:
    def __init__(self, path, output_headers=None, output_delimiter=';'):
        """CsvReport constructor

        :param path: Path to CSV file
        :param output_headers: List of column headers to use in output file
        :param output_delimiter: Delimiter to use in output file, defaults to ';'
        """
        self._path = path
        self._headers = output_headers
        self._delimiter = output_delimiter

    def read(self):
        """Read all data from the CSV file. File format details (like used delimiter)
        will be deduced automatically.

        :return: List of rows as dict with column name and cell value
        """
        with open(self._path, 'r') as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            reader = csv.DictReader(csv_file, dialect=dialect)
            return list(reader)

    def write_headers(self):
        """Create CSV file with headers
        """
        with open(self._path, 'w') as csv_file:
            self._writer = csv.DictWriter(csv_file, fieldnames=self._headers, dialect=csv.excel,
                                          delimiter=self._delimiter, quoting=csv.QUOTE_ALL)
            self._writer.writeheader()

    def append_row(self, row_dict):
        """Append row to the CSV file

        :param row_dict: Dict with column name and cell value
        """
        with open(self._path, 'a') as csv_file:
            self._writer = csv.DictWriter(csv_file, fieldnames=self._headers, dialect=csv.excel,
                                          delimiter=self._delimiter, quoting=csv.QUOTE_ALL)
            self._writer.writerow(row_dict)
