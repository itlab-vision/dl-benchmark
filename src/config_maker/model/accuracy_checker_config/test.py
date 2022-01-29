from model.models.model import Model  # pylint: disable=E0401
# pylint: disable-next=E0401
from tags import CONFIG_TEST_TAG, CONFIG_MODEL_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_DEVICE_TAG, CONFIG_CONFIG_TAG, \
    CONFIG_PARAMETERS_TAG


class Test:
    def __init__(self, model, framework, device, config):
        self.parameters = {
            CONFIG_MODEL_TAG: Model(*model.split(';')) if isinstance(model, str) else model,
            CONFIG_FRAMEWORK_TAG: framework,
            CONFIG_DEVICE_TAG: device,
            CONFIG_CONFIG_TAG: config
        }

    def get_values_list(self):
        return list(self.parameters.values())

    def get_values_dict(self):
        return self.parameters

    def grouping_values_check(self, other):
        count = 0
        diff_tag = ""
        self_values = self.get_values_dict()
        other_values = other.get_values_dict()
        for tag in self_values:
            if self_values[tag] != other_values[tag]:
                diff_tag = tag
                count += 1
        if count != 1 or diff_tag == CONFIG_MODEL_TAG:
            return -1
        else:
            return diff_tag

    @staticmethod
    def grouping(self, other, tag):
        self_parameters = self.get_values_dict()
        value = other.get_values_dict()[tag]
        self_parameters[tag] = ';'.join([self_parameters[tag], value])
        return Test(*self_parameters)

    @staticmethod
    def parse(dom):
        model = Model.parse(dom, True)[0]
        parameters = dom.getElementsByTagName(CONFIG_PARAMETERS_TAG)[0]
        return Test(model=model,
                    framework=parameters.getElementsByTagName(CONFIG_FRAMEWORK_TAG)[0].firstChild.data,
                    device=parameters.getElementsByTagName(CONFIG_DEVICE_TAG)[0].firstChild.data,
                    config=parameters.getElementsByTagName(CONFIG_CONFIG_TAG)[0].firstChild.data
                    )

    def create_dom(self, file):
        DOM_TEST_TAG = file.createElement(CONFIG_TEST_TAG)
        DOM_MODEL_TAG = self.parameters[CONFIG_MODEL_TAG].create_dom(file, True)
        DOM_PARAMETERS_TAG = self.__create_dom_parameters(file)

        DOM_TEST_TAG.appendChild(DOM_MODEL_TAG)
        DOM_TEST_TAG.appendChild(DOM_PARAMETERS_TAG)

        return DOM_TEST_TAG

    def __create_dom_parameters(self, file):
        DOM_PARAMETERS_TAG = file.createElement(CONFIG_PARAMETERS_TAG)
        DOM_INFERENCE_FRAMEWORK_TAG = file.createElement(CONFIG_FRAMEWORK_TAG)
        DOM_DEVICE_TAG = file.createElement(CONFIG_DEVICE_TAG)
        DOM_CONFIG_TAG = file.createElement(CONFIG_CONFIG_TAG)

        DOM_INFERENCE_FRAMEWORK_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_FRAMEWORK_TAG]))
        DOM_DEVICE_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_DEVICE_TAG]))
        DOM_CONFIG_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_CONFIG_TAG]))
        DOM_PARAMETERS_TAG.appendChild(DOM_INFERENCE_FRAMEWORK_TAG)
        DOM_PARAMETERS_TAG.appendChild(DOM_DEVICE_TAG)
        DOM_PARAMETERS_TAG.appendChild(DOM_CONFIG_TAG)

        return DOM_PARAMETERS_TAG

    def test_splitting(self):
        new_tests = []
        model = self.parameters[CONFIG_MODEL_TAG]
        frameworks = self.parameters[CONFIG_FRAMEWORK_TAG].split(';')
        devices = self.parameters[CONFIG_DEVICE_TAG].split(';')
        config = self.parameters[CONFIG_CONFIG_TAG]

        for framework in frameworks:
            for device in devices:
                new_tests.append(Test(model, framework, device, config))
        return new_tests
