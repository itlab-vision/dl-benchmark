import ftplib


class table_handler:
    def __init__(self):
        self.__my_lines = []
        self.__my_current_line = 0


    def set_line(self, line):
        self.__my_lines.append(line)


    def get_line(self):
        if self.__my_current_line < len(self.__my_lines):
            line = self.__my_lines[self.__my_current_line]
            self.__my_current_line += 1
            return line
        else:
            return None


    def skip_line(self):
        self.__my_current_line += 1


def join_tables(ftp_server, table_name):
    tables = []
    ftp_server.retrlines('NLST', tables.append)
    result_tables = [ table_handler() for i in range(len(tables)) ]
    for idx, table in enumerate(tables):
        ftp_server.retrlines('RETR ' + tables[0], result_tables[idx].set_line)

    result_table = open(table_name, 'w')
    for idx in range(len(result_tables)):
        if idx:
            result_tables[idx].skip_line()

        line = result_tables[idx].get_line()
        while (line):
            result_table.write(line + '\n')
            line = result_tables[idx].get_line()
    result_table.close()

    result_table = open(table_name, 'rb')
    send = ftp_server.storbinary('STOR ' + table_name, result_table)
    result_table.close()
