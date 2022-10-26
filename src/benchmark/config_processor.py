from xml.dom import minidom

from config_parser_factory import get_parameters_parser
from frameworks.config_parser.dataset_parser import Dataset
from frameworks.config_parser.framework_independent_parameters import FrameworkIndependentParameters
from frameworks.config_parser.model import Model
from frameworks.framework_wrapper_registry import FrameworkWrapperRegistry


def process_config(config, log):
    test_parser = TestConfigParser()
    test_list = []

    tests = test_parser.get_tests_list(config)
    for idx, curr_test in enumerate(tests):
        try:
            model = test_parser.parse_model(curr_test)
            dataset = test_parser.parse_dataset(curr_test)
            indep_parameters = test_parser.parse_independent_parameters(curr_test)
            framework = indep_parameters.inference_framework
            dep_parameters = test_parser.parse_dependent_parameters(curr_test, framework)

            test_list.append(FrameworkWrapperRegistry()[framework].create_test(model, dataset,
                                                                               indep_parameters, dep_parameters))
        except ValueError as valerr:
            log.warning(f'Test {idx + 1} not added to test list: {valerr}')
    return test_list


class TestConfigParser:
    def get_tests_list(self, config):
        CONFIG_ROOT_TAG = 'Test'
        return minidom.parse(config).getElementsByTagName(CONFIG_ROOT_TAG)

    def parse_model(self, curr_test):
        CONFIG_MODEL_TAG = 'Model'
        CONFIG_MODEL_TASK_TAG = 'Task'
        CONFIG_MODEL_NAME_TAG = 'Name'
        CONFIG_MODEL_PRECISION_TAG = 'Precision'
        CONFIG_MODEL_SOURCE_FRAMEWORK_TAG = 'SourceFramework'
        CONFIG_MODEL_MODEL_PATH_TAG = 'ModelPath'
        CONFIG_MODEL_WEIGHTS_PATH_TAG = 'WeightsPath'

        model_tag = curr_test.getElementsByTagName(CONFIG_MODEL_TAG)[0]

        return Model(
            task=model_tag.getElementsByTagName(CONFIG_MODEL_TASK_TAG)[0].firstChild.data,
            name=model_tag.getElementsByTagName(CONFIG_MODEL_NAME_TAG)[0].firstChild.data,
            precision=model_tag.getElementsByTagName(CONFIG_MODEL_PRECISION_TAG)[0].firstChild.data,
            source_framework=model_tag.getElementsByTagName(CONFIG_MODEL_SOURCE_FRAMEWORK_TAG)[0].firstChild.data,
            model_path=model_tag.getElementsByTagName(CONFIG_MODEL_MODEL_PATH_TAG)[0].firstChild.data,
            weights_path=model_tag.getElementsByTagName(CONFIG_MODEL_WEIGHTS_PATH_TAG)[0].firstChild.data,
        )

    def parse_dataset(self, curr_test):
        CONFIG_DATASET_TAG = 'Dataset'
        CONFIG_DATASET_NAME_TAG = 'Name'
        CONFIG_DATASET_PATH_TAG = 'Path'

        dataset_tag = curr_test.getElementsByTagName(CONFIG_DATASET_TAG)[0]

        return Dataset(
            name=dataset_tag.getElementsByTagName(CONFIG_DATASET_NAME_TAG)[0].firstChild.data,
            path=dataset_tag.getElementsByTagName(CONFIG_DATASET_PATH_TAG)[0].firstChild.data,
        )

    def parse_independent_parameters(self, curr_test):
        CONFIG_FRAMEWORK_INDEPENDENT_TAG = 'FrameworkIndependent'
        CONFIG_FRAMEWORK_INDEPENDENT_INFERENCE_FRAMEWORK_TAG = 'InferenceFramework'
        CONFIG_FRAMEWORK_INDEPENDENT_BATCH_SIZE_TAG = 'BatchSize'
        CONFIG_FRAMEWORK_INDEPENDENT_DEVICE_TAG = 'Device'
        CONFIG_FRAMEWORK_INDEPENDENT_ITERATION_COUNT_TAG = 'IterationCount'
        CONFIG_FRAMEWORK_INDEPENDENT_TEST_TIME_LIMIT_TAG = 'TestTimeLimit'

        indep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_INDEPENDENT_TAG)[0]

        return FrameworkIndependentParameters(
            inference_framework=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_INFERENCE_FRAMEWORK_TAG)[0].firstChild.data,
            batch_size=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_BATCH_SIZE_TAG)[0].firstChild.data,
            device=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_DEVICE_TAG)[0].firstChild.data,
            iterarion_count=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_ITERATION_COUNT_TAG)[0].firstChild.data,
            test_time_limit=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_TEST_TIME_LIMIT_TAG)[0].firstChild.data,
        )

    def parse_dependent_parameters(self, curr_test, framework):
        dep_parser = get_parameters_parser(framework)
        return dep_parser.parse_parameters(curr_test)
