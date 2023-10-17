from tvm import auto_scheduler


class DLIAutoScheduler:
    @staticmethod
    def extract_tasks(mod, target, params):
        tasks, task_weights = auto_scheduler.extract_tasks(mod, params, target)
        assert (len(tasks) > 0)
        return tasks, task_weights

    @staticmethod
    def tasks_tuning(tasks, task_weights, n_trials, log_file):
        tuner = auto_scheduler.TaskScheduler(tasks, task_weights)
        tune_option = auto_scheduler.TuningOptions(
            num_measure_trials=n_trials,
            runner=auto_scheduler.LocalRunner(repeat=10),
            measure_callbacks=[auto_scheduler.RecordToFile(log_file)],
        )

        tuner.tune(tune_option)

    def run_tuning(self, mod, params, target, n_trials, log_file):
        tasks, task_weights = self.extract_tasks(mod, target, params)
        self.tasks_tuning(tasks, task_weights, n_trials, log_file=log_file)
