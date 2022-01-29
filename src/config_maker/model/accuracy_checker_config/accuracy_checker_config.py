import os
from xml.dom import minidom
from .test import Test  # pylint: disable=E0402
from tags import CONFIG_TESTS_TAG, CONFIG_TEST_TAG, CONFIG_MODEL_TAG  # pylint: disable=E0401


class AccuracyCheckerConfig:
    def __init__(self):
        self.__tests = []

    def get_tests(self):
        return self.__tests

    def add_test(self, model, framework, device, config):
        self.__tests.append(Test(model, framework, device, config))

    def change_test(self, row, model, framework, device, config):
        self.__tests[row] = Test(model, framework, device, config)

    def delete_test(self, index):
        self.__tests.pop(index)

    def delete_tests(self, indexes):
        for index in indexes:
            if index < len(self.__tests):
                self.delete_test(index)

    def copy_tests(self, indexes):
        for index in indexes:
            if index < len(self.__tests):
                self.__tests.append(self.__tests[index])

    def clear(self):
        self.__tests.clear()

    def parse_config(self, path_to_config):
        parsed_config = minidom.parse(path_to_config)
        tests = parsed_config.getElementsByTagName(CONFIG_TEST_TAG)
        self.__tests.clear()
        models = []
        data = []
        for dom in tests:
            test = Test.parse(dom)
            self.__tests.append(test)
            models.append(test.parameters[CONFIG_MODEL_TAG])
        self.__tests_grouping()
        return models, data

    def create_config(self, path_to_config):
        if len(self.__tests) == 0:
            return False
        file = minidom.Document()
        DOM_ROOT_TAG = file.createElement(CONFIG_TESTS_TAG)
        file.appendChild(DOM_ROOT_TAG)
        tests = self.__prepare_tests()
        for test in tests:
            DOM_TEST_TAG = test.create_dom(file)
            DOM_ROOT_TAG.appendChild(DOM_TEST_TAG)
        xml_str = file.toprettyxml(indent='\t', encoding='utf-8')
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        return os.path.exists(path_to_config)

    def __prepare_tests(self):
        new_tests = []
        for test in self.__tests:
            splitting_tests = test.test_splitting()
            new_tests.extend(splitting_tests)
        return new_tests

    def __tests_grouping(self):
        while True:
            for i in range(len(self.__tests)):
                if self.__tests[i] is not None:
                    for j in range(i + 1, len(self.__tests)):
                        if self.__tests[j] is not None:
                            diff_tag = self.__tests[i].grouping_values_check(self.__tests[j])
                            if diff_tag != -1:
                                self.__tests[i] = Test.grouping(self.__tests[i], self.__tests[j], diff_tag)
                                self.__tests[j] = None
            if None not in self.__tests:
                break
            self.__tests = [test for test in self.__tests if test is not None]
