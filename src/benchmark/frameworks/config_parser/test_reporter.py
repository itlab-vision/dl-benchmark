import abc
import logging as log

from collections import OrderedDict


class Test(metaclass=abc.ABCMeta):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        self.model = model
        self.dataset = dataset
        self.indep_parameters = indep_parameters
        self.dep_parameters = dep_parameters
        self._log = log

    def get_report(self, **kwargs):
        parameters = self.prepare_framework_params()
        other_param = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': self.indep_parameters.batch_size,
            'mode': 'Sync',
            'framework_params': other_param,
        }

        return report_res

    @staticmethod
    def _get_optional_parameters_string(parameters_dict):
        parameter_strings = []
        for key in parameters_dict:
            if parameters_dict[key] is not None:
                parameter_strings.append(f'{key}: {parameters_dict[key]}')
        return ', '.join(parameter_strings)

    def prepare_framework_params(self):
        parameters = OrderedDict()

        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Iteration count': self.indep_parameters.iteration})

        match_parameter_description = {}

        match_parameter_description['code_source'] = 'Code Source'
        match_parameter_description['runtime'] = 'Runtime'
        match_parameter_description['hint'] = 'Hint'
        match_parameter_description['frontend'] = 'Frontend'
        match_parameter_description['backend'] = 'Backend'
        match_parameter_description['delegate'] = 'Delegate'
        match_parameter_description['delegate_options'] = 'Delegate options'

        match_parameter_description['async_request'] = 'Async request count'
        match_parameter_description['nthreads'] = 'Thread count'
        match_parameter_description['thread_count'] = 'Thread count'
        match_parameter_description['nstreams'] = 'Stream count'
        match_parameter_description['kmp_affinity'] = 'KMP_AFFINITY'
        match_parameter_description['num_inter_threads'] = 'Inter threads'
        match_parameter_description['num_intra_threads'] = 'Intra threads'

        match_parameter_description['mean'] = 'Mean'
        match_parameter_description['input_scale'] = 'Scale'
        match_parameter_description['layout'] = 'Layout'
        match_parameter_description['input_shape'] = 'Input shape'
        match_parameter_description['input_name'] = 'Input name'
        match_parameter_description['output_names'] = 'Output names'
        match_parameter_description['normalize'] = 'Normalization flag'
        match_parameter_description['std'] = 'Standard deviation'
        match_parameter_description['channel_swap'] = 'Channel swap'
        match_parameter_description['swapRB'] = 'Channel swap'
        match_parameter_description['crop'] = 'Crop'

        for parameter, description in match_parameter_description.items():
            if hasattr(self.dep_parameters, parameter) and getattr(self.dep_parameters, parameter) is not None:
                parameters.update({description: getattr(self.dep_parameters, parameter)})

        return parameters
