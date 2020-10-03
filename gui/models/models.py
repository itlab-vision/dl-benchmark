from xml.dom import minidom


class Model:
    def __init__(self, task=None, name=None, precision=None, framework=None, model_path=None, weights_path=None):
        self.task = task
        self.name = name
        self.precision = precision
        self.framework = framework
        self.model_path = model_path
        self.weights_path = weights_path

    def get_str(self):
        return self.task + ';' + self.name + ';' + self.precision + ';' + self.framework + ';' + self.model_path + ';' \
               + self.weights_path


class Dataset:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path

    def get_str(self):
        return self.name + ';' + self.path


class Test:
    def __init__(self, model=None, dataset=None, framework=None, batch_size=None, device=None, iter_count=None,
                 test_time_limit=None, mode=None, extension=None, async_req_count=None, thread_count=None,
                 stream_count=None, channel_swap=None, mean=None, input_scale=None):
        self.model = model
        self.dataset = dataset
        self.framework = framework
        self.batch_size = batch_size
        self.device = device
        self.iter_count = iter_count
        self.test_time_limit = test_time_limit
        self.mode = mode
        self.extension = extension
        self.async_req_count = async_req_count
        self.thread_count = thread_count
        self.stream_count = stream_count
        self.channel_swap = channel_swap
        self.mean = mean
        self.input_scale = input_scale


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


class DeployComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, download_folder=None):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.download_folder = download_folder


class Models:
    def __init__(self):
        self.__models = []

    def get_models(self):
        return self.__models

    def get_models_list(self):
        models_list = []
        for model in self.__models:
            models_list.append(model.get_str())
        return models_list

    def set_models(self, models):
        self.__models = models

    def add_model(self, task, name, precision, framework, model_path, weights_path):
        self.__models.append(Model(task, name, precision, framework, model_path, weights_path))

    def change_model(self, row, task, name, precision, framework, model_path, weights_path):
        self.__models[row] = Model(task, name, precision, framework, model_path, weights_path)

    def delete_model(self, index):
        self.__models.pop(index)

    def delete_models(self, indexes):
        for index in indexes:
            if index < len(self.__models):
                self.delete_model(index)

    def clear(self):
        self.__models.clear()


class Data:
    def __init__(self):
        self.__data = []

    def get_data(self):
        return self.__data

    def get_data_list(self):
        data_list = []
        for data in self.__data:
            data_list.append(data.get_str())
        return data_list

    def set_data(self, data):
        self.__data = data

    def add_dataset(self, name, path):
        self.__data.append(Dataset(name, path))

    def change_dataset(self, row, name, path):
        self.__data[row] = Dataset(name, path)

    def delete_dataset(self, index):
        self.__data.pop(index)

    def delete_data(self, indexes):
        for index in indexes:
            if index < len(self.__data):
                self.delete_dataset(index)

    def clear(self):
        self.__data.clear()


class BenchmarkConfig:
    def __init__(self):
        self.__tests = []

    def get_tests(self):
        return self.__tests

    def add_test(self, model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode=None,
                 extension=None, async_req_count=None, thread_count=None, stream_count=None, channel_swap=None,
                 mean=None, input_scale=None):
        self.__tests.append(Test(model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode,
                                 extension, async_req_count, thread_count, stream_count, channel_swap, mean,
                                 input_scale))

    def change_test(self, row, model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode=None,
                    extension=None, async_req_count=None, thread_count=None, stream_count=None, channel_swap=None,
                    mean=None, input_scale=None):
        self.__tests[row] = Test(model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode,
                                 extension, async_req_count, thread_count, stream_count, channel_swap, mean,
                                 input_scale)

    def delete_test(self, index):
        self.__tests.pop(index)

    def delete_tests(self, indexes):
        for index in indexes:
            if index < len(self.__tests):
                self.delete_test(index)

    def clear(self):
        self.__tests.clear()

    def parse_config(self, path_to_config):
        CONFIG_ROOT_TAG = 'Test'

        parsed_config = minidom.parse(path_to_config)
        tests = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        self.__tests.clear()
        models = []
        data = []
        for test in tests:
            model = self.__parse_model(test)
            dataset = self.__parse_dataset(test)
            framework_independent = self.__parse_framework_independent(test)
            framework_dependent = self.__parse_framework_dependent(test, framework_independent[0])
            models.append(model)
            data.append(dataset)
            self.__tests.append(Test(model.get_str(), dataset.get_str(), *framework_independent, *framework_dependent))
        return models, data

    def __parse_model(self, test):
        CONFIG_MODEL_TAG = 'Model'
        CONFIG_TASK_TAG = 'Task'
        CONFIG_NAME_TAG = 'Name'
        CONFIG_PRECISION_TAG = 'Precision'
        CONFIG_SOURCEFRAMEWORK_TAG = 'SourceFramework'
        CONFIG_MODEL_PATH_TAG = 'ModelPath'
        CONFIG_WEIGHTS_PATH_TAG = 'WeightsPath'

        parsed_model = test.getElementsByTagName(CONFIG_MODEL_TAG)[0]
        model = Model()
        model.task = parsed_model.getElementsByTagName(CONFIG_TASK_TAG)[0].firstChild.data
        model.name = parsed_model.getElementsByTagName(CONFIG_NAME_TAG)[0].firstChild.data
        model.precision = parsed_model.getElementsByTagName(CONFIG_PRECISION_TAG)[0].firstChild.data
        model.framework = parsed_model.getElementsByTagName(CONFIG_SOURCEFRAMEWORK_TAG)[0].firstChild.data
        model.model_path = parsed_model.getElementsByTagName(CONFIG_MODEL_PATH_TAG)[0].firstChild.data
        model.weights_path = parsed_model.getElementsByTagName(CONFIG_WEIGHTS_PATH_TAG)[0].firstChild.data
        return model

    def __parse_dataset(self, test):
        CONFIG_DATASET_TAG = 'Dataset'
        CONFIG_NAME_TAG = 'Name'
        CONFIG_PATH_TAG = 'Path'

        parsed_dataset = test.getElementsByTagName(CONFIG_DATASET_TAG)[0]
        dataset = Dataset()
        dataset.name = parsed_dataset.getElementsByTagName(CONFIG_NAME_TAG)[0].firstChild.data
        dataset.path = parsed_dataset.getElementsByTagName(CONFIG_PATH_TAG)[0].firstChild.data
        return dataset

    def __parse_framework_independent(self, test):
        CONFIG_FRAMEWORK_INDEPENDENT_TAG = 'FrameworkIndependent'
        CONFIG_INFERENCE_FRAMEWORK_TAG = 'InferenceFramework'
        CONFIG_BATCH_SIZE_TAG = 'BatchSize'
        CONFIG_DEVICE_TAG = 'Device'
        CONFIG_ITERATION_COUNT_TAG = 'IterationCount'
        CONFIG_TEST_TIME_LIMIT_TAG = 'TestTimeLimit'

        parsed_framework_independent = test.getElementsByTagName(CONFIG_FRAMEWORK_INDEPENDENT_TAG)[0]
        framework = parsed_framework_independent.getElementsByTagName(CONFIG_INFERENCE_FRAMEWORK_TAG)[0].firstChild.data
        batch_size = parsed_framework_independent.getElementsByTagName(CONFIG_BATCH_SIZE_TAG)[0].firstChild.data
        device = parsed_framework_independent.getElementsByTagName(CONFIG_DEVICE_TAG)[0].firstChild.data
        iter_count = parsed_framework_independent.getElementsByTagName(CONFIG_ITERATION_COUNT_TAG)[0].firstChild.data
        test_time_limit = parsed_framework_independent.getElementsByTagName(CONFIG_TEST_TIME_LIMIT_TAG)[0].firstChild.data
        return [framework, batch_size, device, iter_count, test_time_limit]

    def __parse_framework_dependent(self, test, framework):
        CONFIG_FRAMEWORK_INDEPENDENT_TAG = 'FrameworkDependent'

        parsed_framework_dependent = test.getElementsByTagName(CONFIG_FRAMEWORK_INDEPENDENT_TAG)[0]
        if framework == 'OpenVINO DLDT':
            CONFIG_MODE_TAG = 'Mode'
            CONFIG_EXTENSION_TAG = 'Extension'
            CONFIG_ASYNC_REQ_COUNT_TAG = 'AsyncRequestCount'
            CONFIG_THREAD_COUNT_TAG = 'ThreadCount'
            CONFIG_STREAM_COUNT_TAG = 'StreamCount'

            mode = parsed_framework_dependent.getElementsByTagName(CONFIG_MODE_TAG)[0].firstChild.data
            extension = parsed_framework_dependent.getElementsByTagName(CONFIG_EXTENSION_TAG)[0].firstChild.data
            asynq_req_count = parsed_framework_dependent.getElementsByTagName(CONFIG_ASYNC_REQ_COUNT_TAG)[0].firstChild.data
            thread_count = parsed_framework_dependent.getElementsByTagName(CONFIG_THREAD_COUNT_TAG)[0].firstChild.data
            stream_count = parsed_framework_dependent.getElementsByTagName(CONFIG_STREAM_COUNT_TAG)[0].firstChild.data
            channel_swap = 'None'
            mean = 'None'
            input_scale = 'None'
        elif framework == 'Caffe':
            CONFIG_CHANNEL_SWAP_TAG = 'ChannelSwap'
            CONFIG_MEAN_TAG = 'Mean'
            CONFIG_INPUT_SCALE_TAG = 'InputScale'

            mode = 'None'
            extension = 'None'
            asynq_req_count = 'None'
            thread_count = 'None'
            stream_count = 'None'
            channel_swap = parsed_framework_dependent.getElementsByTagName(CONFIG_CHANNEL_SWAP_TAG)[0].firstChild.data
            mean = parsed_framework_dependent.getElementsByTagName(CONFIG_MEAN_TAG)[0].firstChild.data
            input_scale = parsed_framework_dependent.getElementsByTagName(CONFIG_INPUT_SCALE_TAG)[0].firstChild.data
        return [mode, extension, asynq_req_count, thread_count, stream_count, channel_swap, mean, input_scale]

    def create_config(self, path_to_config):
        if len(self.__tests) == 0:
            return False
        file = minidom.Document()
        CONFIG_ROOT_TAG = file.createElement('Tests')
        file.appendChild(CONFIG_ROOT_TAG)
        tests = self.__prepare_tests()
        for test in tests:
            CONFIG_TEST_TAG = file.createElement('Test')
            CONFIG_MODEL_TAG = self.__create_model_tag(file, test.model)
            CONFIG_DATASET_TAG = self.__create_dataset_tag(file, test.dataset)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG = self.__create_framework_independent_tag(file, test)
            CONFIG_FRAMEWORK_DEPENDENT_TAG = self.__create_framework_dependent_tag(file, test)
            CONFIG_TEST_TAG.appendChild(CONFIG_MODEL_TAG)
            CONFIG_TEST_TAG.appendChild(CONFIG_DATASET_TAG)
            CONFIG_TEST_TAG.appendChild(CONFIG_FRAMEWORK_INDEPENDENT_TAG)
            CONFIG_TEST_TAG.appendChild(CONFIG_FRAMEWORK_DEPENDENT_TAG)
            CONFIG_ROOT_TAG.appendChild(CONFIG_TEST_TAG)
        xml_str = file.toprettyxml(indent='\t', encoding='utf-8')
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        try:
            f = open(path_to_config, 'r')
            f.close()
        except IOError:
            return False
        return True

    def __prepare_tests(self):
        new_tests = []
        for test in self.__tests:
            model = Model(*test.model.split(';'))
            dataset = Dataset(*test.dataset.split(';'))
            framework = test.framework
            batch_sizes = test.batch_size.split(';')
            devices = test.device.split(';')
            iteration_counts = test.iter_count.split(';')
            test_time_limits = test.test_time_limit.split(';')
            if framework == 'OpenVINO DLDT':
                modes = test.mode.split(';')
                extensions = test.extension.split(';')
                async_req_counts = test.async_req_count.split(';')
                thread_counts = test.thread_count.split(';')
                stream_counts = test.stream_count.split(';')
            elif framework == 'Caffe':
                channel_swaps = test.channel_swap.split(';')
                means = test.mean.split(';')
                input_scales = test.input_scale.split(';')
            for batch_size in batch_sizes:
                for device in devices:
                    for iteration_count in iteration_counts:
                        for test_time_limit in test_time_limits:
                            if framework == 'OpenVINO DLDT':
                                for mode in modes:
                                    for extension in extensions:
                                        for async_req_count in async_req_counts:
                                            for thread_count in thread_counts:
                                                for stream_count in stream_counts:
                                                    new_tests.append(Test(model, dataset, framework, batch_size, device,
                                                                     iteration_count, test_time_limit, mode, extension,
                                                                     async_req_count, thread_count, stream_count))
                            elif framework == 'Caffe':
                                for channel_swap in channel_swaps:
                                    for mean in means:
                                        for input_scale in input_scales:
                                            new_tests.append(Test(model, dataset, framework, batch_size, device,
                                                             iteration_count, test_time_limit, channel_swap=channel_swap,
                                                             mean=mean, input_scale=input_scale))
        return new_tests

    def __create_model_tag(self, file, model):
        CONFIG_MODEL_TAG = file.createElement('Model')
        CONFIG_TASK_TAG = file.createElement('Task')
        CONFIG_NAME_TAG = file.createElement('Name')
        CONFIG_PRECISION_TAG = file.createElement('Precision')
        CONFIG_SOURCEFRAMEWORK_TAG = file.createElement('SourceFramework')
        CONFIG_MODEL_PATH_TAG = file.createElement('ModelPath')
        CONFIG_WEIGHTS_PATH_TAG = file.createElement('WeightsPath')

        CONFIG_TASK_TAG.appendChild(file.createTextNode(model.task))
        CONFIG_NAME_TAG.appendChild(file.createTextNode(model.name))
        CONFIG_PRECISION_TAG.appendChild(file.createTextNode(model.precision))
        CONFIG_SOURCEFRAMEWORK_TAG.appendChild(file.createTextNode(model.framework))
        CONFIG_MODEL_PATH_TAG.appendChild(file.createTextNode(model.model_path))
        CONFIG_WEIGHTS_PATH_TAG.appendChild(file.createTextNode(model.weights_path))
        CONFIG_MODEL_TAG.appendChild(CONFIG_TASK_TAG)
        CONFIG_MODEL_TAG.appendChild(CONFIG_NAME_TAG)
        CONFIG_MODEL_TAG.appendChild(CONFIG_PRECISION_TAG)
        CONFIG_MODEL_TAG.appendChild(CONFIG_SOURCEFRAMEWORK_TAG)
        CONFIG_MODEL_TAG.appendChild(CONFIG_MODEL_PATH_TAG)
        CONFIG_MODEL_TAG.appendChild(CONFIG_WEIGHTS_PATH_TAG)
        return CONFIG_MODEL_TAG

    def __create_dataset_tag(self, file, dataset):
        CONFIG_DATASET_TAG = file.createElement('Dataset')
        CONFIG_NAME_TAG = file.createElement('Name')
        CONFIG_PATH_TAG = file.createElement('Path')

        CONFIG_NAME_TAG.appendChild(file.createTextNode(dataset.name))
        CONFIG_PATH_TAG.appendChild(file.createTextNode(dataset.path))
        CONFIG_DATASET_TAG.appendChild(CONFIG_NAME_TAG)
        CONFIG_DATASET_TAG.appendChild(CONFIG_PATH_TAG)
        return CONFIG_DATASET_TAG

    def __create_framework_independent_tag(self, file, test):
        CONFIG_FRAMEWORK_INDEPENDENT_TAG = file.createElement('FrameworkIndependent')
        CONFIG_INFERENCE_FRAMEWORK_TAG = file.createElement('InferenceFramework')
        CONFIG_BATCH_SIZE_TAG = file.createElement('BatchSize')
        CONFIG_DEVICE_TAG = file.createElement('Device')
        CONFIG_ITERATION_COUNT_TAG = file.createElement('IterationCount')
        CONFIG_TEST_TIME_LIMIT_TAG = file.createElement('TestTimeLimit')

        CONFIG_INFERENCE_FRAMEWORK_TAG.appendChild(file.createTextNode(test.framework))
        CONFIG_BATCH_SIZE_TAG.appendChild(file.createTextNode(test.batch_size))
        CONFIG_DEVICE_TAG.appendChild(file.createTextNode(test.device))
        CONFIG_ITERATION_COUNT_TAG.appendChild(file.createTextNode(test.iter_count))
        CONFIG_TEST_TIME_LIMIT_TAG.appendChild(file.createTextNode(test.test_time_limit))
        CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_INFERENCE_FRAMEWORK_TAG)
        CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_BATCH_SIZE_TAG)
        CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_DEVICE_TAG)
        CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_ITERATION_COUNT_TAG)
        CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_TEST_TIME_LIMIT_TAG)
        return CONFIG_FRAMEWORK_INDEPENDENT_TAG

    def __create_framework_dependent_tag(self, file, test):
        CONFIG_FRAMEWORK_INDEPENDENT_TAG = file.createElement('FrameworkDependent')
        if test.framework == 'OpenVINO DLDT':
            CONFIG_MODE_TAG = file.createElement('Mode')
            CONFIG_EXTENSION_TAG = file.createElement('Extension')
            CONFIG_ASYNC_REQ_COUNT_TAG = file.createElement('AsyncRequestCount')
            CONFIG_THREAD_COUNT_TAG = file.createElement('ThreadCount')
            CONFIG_STREAM_COUNT_TAG = file.createElement('StreamCount')

            CONFIG_MODE_TAG.appendChild(file.createTextNode(test.mode))
            CONFIG_EXTENSION_TAG.appendChild(file.createTextNode(test.extension))
            CONFIG_ASYNC_REQ_COUNT_TAG.appendChild(file.createTextNode(test.async_req_count))
            CONFIG_THREAD_COUNT_TAG.appendChild(file.createTextNode(test.thread_count))
            CONFIG_STREAM_COUNT_TAG.appendChild(file.createTextNode(test.stream_count))
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_MODE_TAG)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_EXTENSION_TAG)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_ASYNC_REQ_COUNT_TAG)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_THREAD_COUNT_TAG)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_STREAM_COUNT_TAG)
        elif test.framework == 'Caffe':
            CONFIG_CHANNEL_SWAP_TAG = file.createElement('ChannelSwap')
            CONFIG_MEAN_TAG = file.createElement('Mean')
            CONFIG_INPUT_SCALE_TAG = file.createElement('InputScale')

            CONFIG_CHANNEL_SWAP_TAG.appendChild(file.createTextNode(test.channel_swap))
            CONFIG_MEAN_TAG.appendChild(file.createTextNode(test.mean))
            CONFIG_INPUT_SCALE_TAG.appendChild(file.createTextNode(test.input_scale))
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_CHANNEL_SWAP_TAG)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_MEAN_TAG)
            CONFIG_FRAMEWORK_INDEPENDENT_TAG.appendChild(CONFIG_INPUT_SCALE_TAG)
        return CONFIG_FRAMEWORK_INDEPENDENT_TAG

class RemoteConfig:
    def __init__(self):
        self.__computers = []

    def get_computers(self):
        return self.__computers

    def add_computer(self, ip, login, password, os, path_to_ftp_client, benchmark_config, log_file, res_file):
        self.__computers.append(RemoteComputer(ip, login, password, os, path_to_ftp_client, benchmark_config,
                                               log_file, res_file))

    def change_computer(self, row, ip, login, password, os, path_to_ftp_client, benchmark_config, log_file, res_file):
        self.__computers[row] = RemoteComputer(ip, login, password, os, path_to_ftp_client, benchmark_config,
                                               log_file, res_file)

    def delete_computer(self, index):
        self.__computers.pop(index)

    def delete_computers(self, indexes):
        for index in indexes:
            if index < len(self.__computers):
                self.delete_computer(index)

    def clear(self):
        self.__computers.clear()

    def parse_config(self, path_to_config):
        CONFIG_ROOT_TAG = 'Computer'
        CONFIG_IP_TAG = 'IP'
        CONFIG_LOGIN_TAG = 'Login'
        CONFIG_PASSWORD_TAG = 'Password'
        CONFIG_OS_TAG = 'OS'
        CONFIG_FTP_CLIENT_PATH_TAG = 'FTPClientPath'
        CONFIG_BENCHMARK_CONFIG_TAG = 'BenchmarkConfig'
        CONFIG_LOG_FILE_TAG = 'LogFile'
        CONFIG_RESULT_FILE_TAG = 'ResultFile'

        parsed_config = minidom.parse(path_to_config)
        computers = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        self.__computers.clear()
        for idx, computer in enumerate(computers):
            self.__computers.append(RemoteComputer())
            self.__computers[idx].ip = computer.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data
            self.__computers[idx].login = computer.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data
            self.__computers[idx].password = computer.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data
            self.__computers[idx].os = computer.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data
            self.__computers[idx].path_to_ftp_client = computer.getElementsByTagName(CONFIG_FTP_CLIENT_PATH_TAG)[0].firstChild.data
            self.__computers[idx].benchmark_config = computer.getElementsByTagName(CONFIG_BENCHMARK_CONFIG_TAG)[0].firstChild.data
            self.__computers[idx].log_file = computer.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild.data
            self.__computers[idx].res_file = computer.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild.data

    def create_config(self, path_to_config):
        if len(self.__computers) == 0:
            return False
        file = minidom.Document()
        CONFIG_ROOT_TAG = file.createElement('Computers')
        file.appendChild(CONFIG_ROOT_TAG)
        for computer in self.__computers:
            CONFIG_COMPUTER_TAG = file.createElement('Computer')
            CONFIG_IP_TAG = file.createElement('IP')
            CONFIG_LOGIN_TAG = file.createElement('Login')
            CONFIG_PASSWORD_TAG = file.createElement('Password')
            CONFIG_OS_TAG = file.createElement('OS')
            CONFIG_FTP_CLIENT_PATH_TAG = file.createElement('FTPClientPath')
            CONFIG_BENCHMARK_CONFIG_TAG = file.createElement('BenchmarkConfig')
            CONFIG_LOG_FILE_TAG = file.createElement('LogFile')
            CONFIG_RESULT_FILE_TAG = file.createElement('ResultFile')

            CONFIG_IP_TAG.appendChild(file.createTextNode(computer.ip))
            CONFIG_LOGIN_TAG.appendChild(file.createTextNode(computer.login))
            CONFIG_PASSWORD_TAG.appendChild(file.createTextNode(computer.password))
            CONFIG_OS_TAG.appendChild(file.createTextNode(computer.os))
            CONFIG_FTP_CLIENT_PATH_TAG.appendChild(file.createTextNode(computer.path_to_ftp_client))
            CONFIG_BENCHMARK_CONFIG_TAG.appendChild(file.createTextNode(computer.benchmark_config))
            CONFIG_LOG_FILE_TAG.appendChild(file.createTextNode(computer.log_file))
            CONFIG_RESULT_FILE_TAG.appendChild(file.createTextNode(computer.res_file))
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_IP_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_LOGIN_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_PASSWORD_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_OS_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_FTP_CLIENT_PATH_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_BENCHMARK_CONFIG_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_LOG_FILE_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_RESULT_FILE_TAG)
            CONFIG_ROOT_TAG.appendChild(CONFIG_COMPUTER_TAG)
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        try:
            f = open(path_to_config, 'r')
            f.close()
        except IOError:
            return False
        return True


class DeployConfig:
    def __init__(self):
        self.__computers = []

    def get_computers(self):
        return self.__computers

    def add_computer(self, ip, login, password, os, download_folder):
        self.__computers.append(DeployComputer(ip, login, password, os, download_folder))

    def change_computer(self, row, ip, login, password, os, download_folder):
        self.__computers[row] = DeployComputer(ip, login, password, os, download_folder)

    def delete_computer(self, index):
        self.__computers.pop(index)

    def delete_computers(self, indexes):
        for index in indexes:
            if index < len(self.__computers):
                self.delete_computer(index)

    def clear(self):
        self.__computers.clear()

    def parse_config(self, path_to_config):
        CONFIG_ROOT_TAG = 'Computer'
        CONFIG_IP_TAG = 'IP'
        CONFIG_LOGIN_TAG = 'Login'
        CONFIG_PASSWORD_TAG = 'Password'
        CONFIG_OS_TAG = 'OS'
        CONFIG_DOWNLOAD_FOLDER_TAG = 'DownloadFolder'

        parsed_config = minidom.parse(path_to_config)
        computers = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        self.__computers.clear()
        for idx, computer in enumerate(computers):
            self.__computers.append(DeployComputer())
            self.__computers[idx].ip = computer.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data
            self.__computers[idx].login = computer.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data
            self.__computers[idx].password = computer.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data
            self.__computers[idx].os = computer.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data
            self.__computers[idx].download_folder = computer.getElementsByTagName(CONFIG_DOWNLOAD_FOLDER_TAG)[0].firstChild.data

    def create_config(self, path_to_config):
        if len(self.__computers) == 0:
            return False
        file = minidom.Document()
        CONFIG_ROOT_TAG = file.createElement('Computers')
        file.appendChild(CONFIG_ROOT_TAG)
        for computer in self.__computers:
            CONFIG_COMPUTER_TAG = file.createElement('Computer')
            CONFIG_IP_TAG = file.createElement('IP')
            CONFIG_LOGIN_TAG = file.createElement('Login')
            CONFIG_PASSWORD_TAG = file.createElement('Password')
            CONFIG_OS_TAG = file.createElement('OS')
            CONFIG_DOWNLOAD_FOLDER_TAG = file.createElement('DownloadFolder')

            CONFIG_IP_TAG.appendChild(file.createTextNode(computer.ip))
            CONFIG_LOGIN_TAG.appendChild(file.createTextNode(computer.login))
            CONFIG_PASSWORD_TAG.appendChild(file.createTextNode(computer.password))
            CONFIG_OS_TAG.appendChild(file.createTextNode(computer.os))
            CONFIG_DOWNLOAD_FOLDER_TAG.appendChild(file.createTextNode(computer.download_folder))
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_IP_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_LOGIN_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_PASSWORD_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_OS_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_DOWNLOAD_FOLDER_TAG)
            CONFIG_ROOT_TAG.appendChild(CONFIG_COMPUTER_TAG)
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        try:
            f = open(path_to_config, 'r')
            f.close()
        except IOError:
            return False
        return True


class DataBase:
    def __init__(self):
        self.models = Models()
        self.data = Data()
        self.benchmark_config = BenchmarkConfig()
        self.remote_config = RemoteConfig()
        self.deploy_config = DeployConfig()
