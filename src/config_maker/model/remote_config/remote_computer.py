class RemoteComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, path_to_ftp_client=None, benchmark_config=None,
                 log_file=None, res_file=None):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.path_to_ftp_client = path_to_ftp_client
        self.benchmark_config = benchmark_config
        self.log_file = log_file
        self.res_file = res_file
