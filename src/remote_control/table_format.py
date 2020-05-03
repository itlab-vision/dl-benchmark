import ftplib
from io import StringIO

def join_tables(ftp_server, table_name):
    tables = []
    ftp_server.retrlines('NLST', tables.append)
    reader = StringIO()
    ftp_server.retrlines('RETR ' + tables[0], reader.write)
    reader.seek(0)
    csv_table = reader.getvalue().split(';')
    number_columns_in_table = 15
    formatted_table = open(table_name, 'w')
    for curr_line in range(0, len(csv_table) - 1, number_columns_in_table):
        next_row = csv_table[curr_line: (curr_line + number_columns_in_table)]
        formatted_table.write(';'.join(next_row) + '\n')
    
    for curr_table in range(1, len(tables)):
        reader.truncate(0)
        reader.seek(0)
        ftp_server.retrlines('RETR ' + tables[curr_table], reader.write)
        csv_table = reader.getvalue().split(';')
        for curr_line in range(number_columns_in_table,
            len(csv_table) - 1, number_columns_in_table):
            next_row = csv_table[curr_line: (curr_line +
                number_columns_in_table)]
            formatted_table.write(';'.join(next_row) + '\n')
    formatted_table.close()

    result_table = open(table_name, 'rb')
    send = ftp_server.storbinary('STOR ' + table_name, result_table)
    result_table.close()
