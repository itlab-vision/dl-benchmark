import argparse
import logging as log
import os
import sys

import tvm
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
                        help='Maximum number of trials to run per task',
                        required=True,
                        type=int)
    parser.add_argument('-w', '--work_dir',
                        help='Working directory for logging results.',
                        default='meta-scheduler',
                        type=str)
    parser.add_argument('-o', '--output',
                        help='Path to the file to save the model.',
                        default='lib.so',
                        type=str,
                        dest='output_file')

    parser.add_argument('--opt_level',
                        help='The optimization level of the task extractions.',
                        type=int,
                        choices=[0, 1, 2, 3, 4],
                        default=2)

    parser.add_argument('--space',
                        help='The space generator to use.',
                        default='post-order-apply',
                        choices=['post-order-apply', 'union'],
                        type=str)
    parser.add_argument('--strategy',
                        help='The search strategy to use.',
                        default='evolutionary',
                        choices=['replay-func', 'replay-trace', 'evolutionary'],
                        type=str)
    parser.add_argument('--num_tuning_cores',
                        help='The number of CPU cores to use during tuning.',
                        default='physical',
                        type=str)
    parser.add_argument('--seed',
                        help='The random seed to use.',
                        nargs='?',
                        type=int)

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
                        help='Number of trials to run per iteration.',
                        type=int,
                        default=64)
    parser.add_argument('--database',
                        help='The database.',
                        default='json',
                        choices=['json', 'memory'],
                        type=str)
    parser.add_argument('--cost_model',
                        help='The cost model.',
                        default='xgb',
                        choices=['xgb', 'mlp', 'random'],
                        type=str)
    parser.add_argument('--task_scheduler',
                        help='The task scheduler.',
                        default='gradient',
                        choices=['gradient', 'round-robin'],
                        type=str)

    args = parser.parse_args()

    return args


def extract_tasks(mod, params, target, work_dir, opt_level, space, strategy, num_tuning_cores, seed):
    extracted_tasks = ms.relay_integration.extract_tasks(mod=mod, params=params, target=target, opt_level=opt_level)

    tasks, task_weights = ms.relay_integration.extracted_tasks_to_tune_contexts(extracted_tasks=extracted_tasks,
                                                                                work_dir=work_dir,
                                                                                space=space, strategy=strategy,
                                                                                num_tuning_cores=num_tuning_cores,
                                                                                seed=seed)
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

    database = ms.database.JSONDatabase(
        f"{args.work_dir}/database_workload.json",
        f"{args.work_dir}/database_tuning_record.json",
        allow_missing=False
    )
    with tvm.transform.PassContext(opt_level=args.opt_level):
        lib = ms.relay_integration.compile_relay(database, mod, args.target, params)
    lib.export_library(args.output_file)


if __name__ == '__main__':
    sys.exit(main() or 0)
