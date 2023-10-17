from tvm import autotvm
from tvm.autotvm.tuner import XGBTuner, GATuner, RandomTuner, GridSearchTuner


class DLIAutoTVM:
    @staticmethod
    def create_tuner(task, tuner):
        if tuner == "xgb":
            tuner_obj = XGBTuner(task, loss_type="reg")
        elif tuner == "xgb_knob":
            tuner_obj = XGBTuner(task, loss_type="reg", feature_type="knob")
        elif tuner == "xgb_itervar":
            tuner_obj = XGBTuner(task, loss_type="reg", feature_type="itervar")
        elif tuner == "xgb_curve":
            tuner_obj = XGBTuner(task, loss_type="reg", feature_type="curve")
        elif tuner == "xgb_rank":
            tuner_obj = XGBTuner(task, loss_type="rank")
        elif tuner == "xgb_rank_knob":
            tuner_obj = XGBTuner(task, loss_type="rank", feature_type="knob")
        elif tuner == "xgb_rank_itervar":
            tuner_obj = XGBTuner(task, loss_type="rank", feature_type="itervar")
        elif tuner == "xgb_rank_curve":
            tuner_obj = XGBTuner(task, loss_type="rank", feature_type="curve")
        elif tuner == "xgb_rank_binary":
            tuner_obj = XGBTuner(task, loss_type="rank-binary")
        elif tuner == "xgb_rank_binary_knob":
            tuner_obj = XGBTuner(task, loss_type="rank-binary", feature_type="knob")
        elif tuner == "xgb_rank_binary_itervar":
            tuner_obj = XGBTuner(task, loss_type="rank-binary", feature_type="itervar")
        elif tuner == "xgb_rank_binary_curve":
            tuner_obj = XGBTuner(task, loss_type="rank-binary", feature_type="curve")
        elif tuner == "ga":
            tuner_obj = GATuner(task, pop_size=50)
        elif tuner == "random":
            tuner_obj = RandomTuner(task)
        elif tuner == "gridsearch":
            tuner_obj = GridSearchTuner(task)
        else:
            raise ValueError("Invalid tuner: " + tuner)

        return tuner_obj

    @staticmethod
    def extract_tasks(mod, target, params):
        tasks = autotvm.task.extract_from_program(
            mod=mod, target=target, params=params
        )
        assert (len(tasks) > 0)
        return tasks

    def tasks_tuning(self, tasks, tuner_name, early_stopping=None, log_filename="tuning.log"):
        for i, task in enumerate(tasks):
            prefix = "[Task %2d/%2d] " % (i + 1, len(tasks))
            tuner_obj = self.create_tuner(task, tuner_name)
            n_trial = len(task.config_space)
            tuner_obj.tune(
                n_trial=n_trial,
                early_stopping=early_stopping,
                measure_option=autotvm.measure_option(
                    builder=autotvm.LocalBuilder(),
                    runner=autotvm.LocalRunner(repeat=10),
                ),
                callbacks=[
                    autotvm.callback.progress_bar(n_trial, prefix=prefix),
                    autotvm.callback.log_to_file(log_filename),
                ],
            )

    def run_tuning(self, mod, params, target, log_file):
        tasks = self.extract_tasks(mod, target, params)
        self.tasks_tuning(tasks, 'xgb_rank', log_filename=log_file)
