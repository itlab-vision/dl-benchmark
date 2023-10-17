from tvm_autotvm import DLIAutoTVM
from tvm_auto_scheduler import DLIAutoScheduler
from tvm_meta_schedule import DLIMetaSchedule


class TVMAutoTuning:

    @staticmethod
    def run_autotvm(mod, params, target, log_file):
        tuning = DLIAutoTVM()
        tuning.run_tuning(mod, params, target, log_file)

    @staticmethod
    def run_auto_scheduler(mod, params, target, n_trials, log_file):
        tuning = DLIAutoScheduler()
        tuning.run_tuning(mod, params, target, n_trials, log_file)

    @staticmethod
    def run_meta_schedule(mod, params, target, n_trials, work_dir):
        tuning = DLIMetaSchedule()
        tuning.run_tuning(mod, params, target, n_trials, work_dir)
