import os
from tvm import meta_schedule as ms


class DLIMetaSchedule:
    @staticmethod
    def extract_tasks(mod, target, params, strategy, work_dir):
        extracted_tasks = ms.relay_integration.extract_tasks(
            mod, target, params
        )
        assert (len(extracted_tasks) > 0)

        tasks, task_weights = ms.relay_integration.extracted_tasks_to_tune_contexts(
            extracted_tasks, work_dir, strategy=strategy,
        )
        return tasks, task_weights

    @staticmethod
    def tasks_tuning(tasks, task_weights, n_trials, work_dir):
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
        evaluator_config = ms.runner.config.EvaluatorConfig(number=1, repeat=10)
        ms.tune.tune_tasks(
            tasks=tasks,
            task_weights=task_weights,
            work_dir=work_dir,
            max_trials_global=n_trials,
            num_trials_per_iter=64,
            max_trials_per_task=256,
            builder=ms.builder.LocalBuilder(),
            runner=ms.runner.LocalRunner(evaluator_config=evaluator_config),
        )

    def run_tuning(self, mod, params, target, n_trials, work_dir):
        tasks, task_weights = self.extract_tasks(mod, target, params, 'evolutionary', work_dir)
        self.tasks_tuning(tasks, task_weights, n_trials, work_dir)
