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
        return minidom.parse(config).getElementsByTagName('Test')

    def parse_model(self, curr_test):
        model_tag = curr_test.getElementsByTagName('Model')[0]

        return Model(
            task=model_tag.getElementsByTagName('Task')[0].firstChild.data,
            name=model_tag.getElementsByTagName('Name')[0].firstChild.data,
            precision=model_tag.getElementsByTagName('Precision')[0].firstChild.data,
            source_framework=model_tag.getElementsByTagName('SourceFramework')[0].firstChild.data,
            model_path=model_tag.getElementsByTagName('ModelPath')[0].firstChild.data,
            weights_path=model_tag.getElementsByTagName('WeightsPath')[0].firstChild.data,
        )

    def parse_dataset(self, curr_test):
        dataset_tag = curr_test.getElementsByTagName('Dataset')[0]

        return Dataset(
            name=dataset_tag.getElementsByTagName('Name')[0].firstChild.data,
            path=dataset_tag.getElementsByTagName('Path')[0].firstChild.data,
        )

    def parse_independent_parameters(self, curr_test):
        indep_parameters_tag = curr_test.getElementsByTagName('FrameworkIndependent')[0]
        _batch_size = indep_parameters_tag.getElementsByTagName('BatchSize')[0].firstChild

        return FrameworkIndependentParameters(
            inference_framework=indep_parameters_tag.getElementsByTagName('InferenceFramework')[0].firstChild.data,
            batch_size=_batch_size.data if _batch_size else None,
            device=indep_parameters_tag.getElementsByTagName('Device')[0].firstChild.data,
            iterarion_count=indep_parameters_tag.getElementsByTagName('IterationCount')[0].firstChild.data,
            test_time_limit=indep_parameters_tag.getElementsByTagName('TestTimeLimit')[0].firstChild.data,
        )

    def parse_dependent_parameters(self, curr_test, framework):
        dep_parser = get_parameters_parser(framework)
        return dep_parser.parse_parameters(curr_test)
