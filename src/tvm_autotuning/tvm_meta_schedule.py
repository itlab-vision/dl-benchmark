import argparse
import logging as log
import os
import sys

from tvm import meta_schedule as ms

import utils


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mod',
                        help='Path to an .json file with a model.',
                        required=True,
                        type=str,
                        dest='model_json')
    parser.add_argument('-p', '--params',
                        help='Path to an .params file with a model parameters.',
                        required=True,
                        type=str,
                        dest='model_params')
    parser.add_argument('-t', '--target',
                        help='Target device information, for example "llvm -num-cores 6" for CPU.',
                        required=True,
                        type=str)
    parser.add_argument('-n', '--n_trials',
                        help='The number of measurement trials.',
                        required=True,
                        type=int)
    parser.add_argument('--max_trials_per_task',
                        type=int,
                        help='Maximum number of trials to run per task')
    parser.add_argument('-w', '--work_dir',
                        help='Working directory for logging results.',
                        required=True,
                        default='meta-scheduler',
                        type=str)

    parser.add_argument('--opt_level',
                        help='The optimization level of the task extractions.',
                        type=int,
                        choices=[0, 1, 2, 3],
                        default=3)

    parser.add_argument('--space',
                        default='post-order-apply',
                        choices=['post-order-apply', 'union'],
                        type=str,
                        help='The space generator to use.')
    parser.add_argument('--strategy',
                        default='evolutionary',
                        choices=['replay-func', 'replay-trace', 'evolutionary'],
                        type=str,
                        help='The search strategy to use.')
    parser.add_argument('--num_tuning_cores',
                        default='physical',
                        type=str,
                        help='The number of CPU cores to use during tuning.')
    parser.add_argument('--seed',
                        type=int,
                        help='The random seed to use.',
                        nargs='?')

    parser.add_argument('--number',
                        help='The number of times to run the generated code for taking average.'
                             'We call these runs as one repeat of measurement.',
                        default=3,
                        type=int)
    parser.add_argument('--repeat',
                        help='The number of times to repeat the measurement.'
                             'In total, the generated code will be run (1 + number x repeat) times,'
                             'where the first one is warm up and will be discarded.',
                        default=1,
                        type=int)

    parser.add_argument('--num_trials_per_iter',
                        type=int,
                        default=64,
                        help='Number of trials to run per iteration.')
    parser.add_argument('--database',
                        default='json',
                        choices=['json', 'memory'],
                        type=str,
                        help='The database.')
    parser.add_argument('--cost_model',
                        default='xgb',
                        choices=['xgb', 'mlp', 'random'],
                        type=str,
                        help='The cost model.')
    parser.add_argument('--task_scheduler',
                        default='gradient',
                        choices=['gradient', 'round-robin'],
                        type=str,
                        help='The task scheduler.')

    args = parser.parse_args()

    return args


def extract_tasks(mod, params, target, work_dir, opt_level, space, strategy, num_tuning_cores, seed):
    extracted_tasks = ms.relay_integration.extract_tasks(
        mod, target, params, opt_level=opt_level,
    )

    tasks, task_weights = ms.relay_integration.extracted_tasks_to_tune_contexts(
        extracted_tasks, work_dir, space=space, strategy=strategy, num_tuning_cores=num_tuning_cores, seed=seed,
    )
    return tasks, task_weights


def tune_tasks(tasks, task_weights, n_trials, work_dir,
               number, repeat, num_trials_per_iter, max_trials_per_task,
               database, cost_model, task_scheduler):
    evaluator_config = ms.runner.config.EvaluatorConfig(number=number, repeat=repeat)

    ms.tune.tune_tasks(
        tasks=tasks,
        task_weights=task_weights,
        work_dir=work_dir,
        max_trials_global=n_trials,
        num_trials_per_iter=num_trials_per_iter,
        max_trials_per_task=max_trials_per_task,
        database=database,
        cost_model=cost_model,
        task_scheduler=task_scheduler,
        builder=ms.builder.LocalBuilder(),
        runner=ms.runner.LocalRunner(evaluator_config=evaluator_config),

    )


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )

    args = cli_argument_parser()
    mod = utils.load_mod(args.model_json)
    params = utils.load_params(args.model_params)

    if not os.path.exists(args.work_dir):
        log.info('Creating a directory for the database')
        os.mkdir(args.work_dir)

    log.info('Extracting tasks using meta_schedule')
    tasks, task_weights = extract_tasks(mod, params, args.target, args.work_dir,
                                        args.opt_level, args.space, args.strategy,
                                        args.num_tuning_cores, args.seed)

    log.info('Neural network tuning')
    tune_tasks(tasks, task_weights, args.n_trials, args.work_dir,
               args.number, args.repeat, args.num_trials_per_iter, args.max_trials_per_task,
               args.database, args.cost_model, args.task_scheduler)


if __name__ == '__main__':
    sys.exit(main() or 0)
