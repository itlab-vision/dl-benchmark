from ..config_parser.test_reporter import Test


class TensorFlowTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        report_res = (f'{self.model.task};{self.model.name};{self.dataset.name};{self.model.source_framework};'
                      f'{self.indep_parameters.inference_framework};input_shape;{self.model.precision};'
                      f'{self.indep_parameters.batch_size};Sync;Device: {self.indep_parameters.device},'
                      f' Iteration count: {self.indep_parameters.iteration},'
                      f' Thread count: {self.dep_parameters.nthreads},'
                      f' Inter threads: {self.dep_parameters.num_inter_threads},'
                      f' Intra threads: {self.dep_parameters.num_intra_threads},'
                      f' KMP_AFFINITY: {self.dep_parameters.kmp_affinity}')
        return report_res
