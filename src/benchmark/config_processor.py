from xml.dom import minidom

from config_parser_factory import get_parameters_parser
from frameworks.config_parser.dataset_parser import Dataset
from frameworks.config_parser.framework_independent_parameters import FrameworkIndependentParameters
from frameworks.config_parser.model import Model
from frameworks.framework_wrapper_registry import FrameworkWrapperRegistry


def process_config(config, log):
    test_parser = TestConfigParser(log)
    test_list = []

    tests = test_parser.get_tests_list(config)
    status = 0
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
            status = 1

    return test_list, status


class TestConfigParser:
    def __init__(self, log):
        self._log = log

    def get_tests_list(self, config):
        return minidom.parse(config).getElementsByTagName('Test')

    def parse_model(self, curr_test):
        model_tag = curr_test.getElementsByTagName('Model')[0]

        task = model_tag.getElementsByTagName('Task')[0].firstChild.data.strip()
        model_name = model_tag.getElementsByTagName('Name')[0].firstChild.data.strip()
        precision = model_tag.getElementsByTagName('Precision')[0].firstChild.data.strip()
        source_framework = model_tag.getElementsByTagName('SourceFramework')[0].firstChild.data.strip()

        model_path = ''
        if model_tag.getElementsByTagName('ModelPath')[0].firstChild:
            model_path = model_tag.getElementsByTagName('ModelPath')[0].firstChild.data.strip()
        weights_path = ''
        if model_tag.getElementsByTagName('WeightsPath')[0].firstChild:
            weights_path = model_tag.getElementsByTagName('WeightsPath')[0].firstChild.data.strip()

        module = ''
        module_tag = model_tag.getElementsByTagName('Module')
        if module_tag and module_tag[0].firstChild:
            module = module_tag[0].firstChild.data

        self._log.info(f'Model:\n\tName - {model_name}\n\tTask - {task}\n\t'
                       f'Precision - {precision}\n\tSource framework - {source_framework}\n\t'
                       f'Model path - {model_path}\n\tWeights path - {weights_path}\n\t'
                       f'Module - {module}')

        return Model(task=task, name=model_name, precision=precision, source_framework=source_framework,
                     model_path=model_path, weights_path=weights_path, module=module)

    def parse_dataset(self, curr_test):
        dataset_tag = curr_test.getElementsByTagName('Dataset')[0]

        try:
            name = dataset_tag.getElementsByTagName('Name')[0].firstChild.data.strip()
            path = dataset_tag.getElementsByTagName('Path')[0].firstChild.data.strip()

            self._log.info(f'Dataset:\n\tName - {name}\n\tPath - {path}')
            return Dataset(name=name, path=path)
        except AttributeError:
            self._log.warning('No dataset provided. Dummy input will be used')
            return None

    def parse_independent_parameters(self, curr_test):
        indep_parameters_tag = curr_test.getElementsByTagName('FrameworkIndependent')[0]
        inference_framework = indep_parameters_tag.getElementsByTagName('InferenceFramework')[0].firstChild.data.strip()

        _batch_size = indep_parameters_tag.getElementsByTagName('BatchSize')[0].firstChild
        batch_size = _batch_size.data if (_batch_size and _batch_size.data != 'None') else None

        device = indep_parameters_tag.getElementsByTagName('Device')[0].firstChild.data.strip()
        iteration_count = indep_parameters_tag.getElementsByTagName('IterationCount')[0].firstChild.data.strip()
        test_time_limit = int(indep_parameters_tag.getElementsByTagName('TestTimeLimit')[0].firstChild.data)
        timeout_overhead_element = indep_parameters_tag.getElementsByTagName('TimeoutOverhead')
        if timeout_overhead_element:
            timeout_overhead = int(timeout_overhead_element[0].firstChild.data)
        else:
            timeout_overhead = 300  # default value

        custom_models_links = ''
        links_tag = indep_parameters_tag.getElementsByTagName('CustomModelsLinks')
        if links_tag and links_tag[0].firstChild:
            custom_models_links = links_tag[0].firstChild.data.strip()

        self._log.info(f'Framework independent parameters:\n\t'
                       f'Inference framework - {inference_framework}\n\t'
                       f'Batch size - {batch_size}\n\t'
                       f'Device - {device}\n\t'
                       f'Number of iterations - {iteration_count}\n\t'
                       f'Time limit of test execution - {test_time_limit}\n\t'
                       f'Timeout overhead - {timeout_overhead}\n\t'
                       f'Custom models links = {custom_models_links}')

        return FrameworkIndependentParameters(
            inference_framework=inference_framework,
            batch_size=batch_size,
            device=device,
            iterarion_count=iteration_count,
            test_time_limit=test_time_limit,
            timeout_overhead=timeout_overhead,
            custom_models_links=custom_models_links,
        )

    def parse_dependent_parameters(self, curr_test, framework):
        dep_parser = get_parameters_parser(framework)

        return dep_parser.parse_parameters(curr_test)
