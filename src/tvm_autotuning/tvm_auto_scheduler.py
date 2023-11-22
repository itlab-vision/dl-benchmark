import argparse
import logging as log
import sys

import tvm
from tvm import auto_scheduler, relay

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
                        help='Target device information, for example "llvm" for CPU.',
                        required=True,
                        type=str)
    parser.add_argument('-n', '--n_trials',
                        help='The number of measurement trials.',
                        required=True,
                        type=int)
    parser.add_argument('-l', '--log',
                        help='Path to the file for logging optimization results.',
                        default='auto-scheduler.log',
                        type=str,
                        dest='log_file')
    parser.add_argument('-o', '--output',
                        help='Path to the file to save the model.',
                        default='lib.so',
                        type=str,
                        dest='output_file')

    parser.add_argument('--num_cores',
                        help='The number of device cores.',
                        nargs='?',
                        type=int)
    parser.add_argument('--vector_unit_bytes',
                        help='The width of vector units in bytes.',
                        nargs='?',
                        type=int)
    parser.add_argument('--cache_line_bytes',
                        help='The size of cache line in bytes.',
                        nargs='?',
                        type=int)
    parser.add_argument('--max_shared_memory_per_block',
                        help='The max shared memory per block in bytes.',
                        nargs='?',
                        type=int)
    parser.add_argument('--max_local_memory_per_block',
                        help='The max number of threads per block.',
                        nargs='?',
                        type=int)
    parser.add_argument('--max_threads_per_block',
                        help='The max number of threads per block.',
                        nargs='?',
                        type=int)
    parser.add_argument('--max_vthread_extent',
                        help='The max vthread extent.',
                        nargs='?',
                        type=int)
    parser.add_argument('--warp_size',
                        help='The thread numbers of a warp.',
                        nargs='?',
                        type=int)
    parser.add_argument('--include_simple_tasks',
                        help='Whether to extract simple tasks that do not include complicated ops.',
                        action='store_true')
    parser.add_argument('--opt_level',
                        help='The optimization level of the task extractions',
                        type=int,
                        choices=[0, 1, 2, 3, 4],
                        default=2)

    parser.add_argument('--strategy',
                        help='The scheduling strategy.',
                        type=str,
                        choices=['round-robin', 'gradient'],
                        default='round-robin')
    parser.add_argument('--load_model_file',
                        help='Load pre-trained optimization model from this file.',
                        type=str,
                        nargs='?')
    parser.add_argument('--load_log_file',
                        help='Load measurement records from this file.',
                        type=str,
                        nargs='?')
    parser.add_argument('--alpha',
                        help='The parameter used for gradient strategy.',
                        type=float,
                        default=0.2)
    parser.add_argument('--beta',
                        help='The parameter used for gradient strategy.',
                        type=float,
                        default=2)
    parser.add_argument('--backward_window_size',
                        help='The parameter used for gradient strategy.',
                        type=int,
                        default=3)

    parser.add_argument('--per_round',
                        help='The number of measurement trials per round.',
                        default=64,
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

    parser.add_argument('--search_policy',
                        help='The list of search policies.'
                             'If str, use "default" for the default policy (SketchPolicy + XGBModel),'
                             '"sketch.xgb" for SketchPolicy + XGBModel,'
                             '"sketch.random" for SketchPolicy + RandomModel.',
                        default='default')
    parser.add_argument('--search_policy_params',
                        help='The parameters of the search policy.',
                        nargs='?')
    parser.add_argument('--adaptive_training',
                        action='store_true',
                        help='Option used by XGBModel to reduce the model training frequency'
                             'when there are too many logs.')
    parser.add_argument('--per_task_early_stopping',
                        help='Stop tuning a task early if getting no improvement after n measurements.',
                        type=int)

    args = parser.parse_args()

    return args


def extract_tasks(mod, params, target, num_cores, vector_unit_bytes,
                  cache_line_bytes, max_shared_memory_per_block,
                  max_local_memory_per_block, max_threads_per_block,
                  max_vthread_extent, warp_size, include_simple_tasks, opt_level):
    hardware_param_list = [num_cores, vector_unit_bytes,
                           cache_line_bytes, max_shared_memory_per_block,
                           max_local_memory_per_block, max_threads_per_block,
                           max_vthread_extent, warp_size]

    hardware_params = None
    if any(hardware_param_list):
        log.info('setting arguments for HardwareParams')

        if any(True for x in hardware_param_list if x is None):
            raise ValueError('All parameters for HardwareParams must be passed')

        hardware_params = auto_scheduler.HardwareParams(num_cores, vector_unit_bytes,
                                                        cache_line_bytes, max_shared_memory_per_block,
                                                        max_local_memory_per_block, max_threads_per_block,
                                                        max_vthread_extent, warp_size)

    tasks, task_weights = auto_scheduler.extract_tasks(mod=mod, params=params, target=target,
                                                       hardware_params=hardware_params,
                                                       include_simple_tasks=include_simple_tasks, opt_level=opt_level)

    return tasks, task_weights


def tune_tasks(tasks, task_weights, n_trials, per_round, log_file, number, repeat, strategy,
               load_model_file, load_log_file, alpha, beta, backward_window_size,
               search_policy, search_policy_params, adaptive_training, per_task_early_stopping):
    tuner = auto_scheduler.TaskScheduler(tasks, task_weights, strategy=strategy, load_model_file=load_model_file,
                                         load_log_file=load_log_file, alpha=alpha, beta=beta,
                                         backward_window_size=backward_window_size)
    tune_option = auto_scheduler.TuningOptions(num_measure_trials=n_trials,
                                               runner=auto_scheduler.LocalRunner(number=number, repeat=repeat),
                                               verbose=1,
                                               num_measures_per_round=per_round,
                                               measure_callbacks=[auto_scheduler.RecordToFile(log_file)])

    tuner.tune(tune_option, search_policy=search_policy, search_policy_params=search_policy_params,
               adaptive_training=adaptive_training, per_task_early_stopping=per_task_early_stopping)


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )

    args = cli_argument_parser()
    mod = utils.load_mod(args.model_json)
    params = utils.load_params(args.model_params)

    log.info('Extracting tasks using auto_scheduler')
    tasks, task_weights = extract_tasks(mod, params, args.target, args.num_cores, args.vector_unit_bytes,
                                        args.cache_line_bytes, args.max_shared_memory_per_block,
                                        args.max_local_memory_per_block, args.max_threads_per_block,
                                        args.max_vthread_extent, args.warp_size, args.include_simple_tasks,
                                        args.opt_level)

    log.info('Neural network tuning')
    tune_tasks(tasks, task_weights, args.n_trials, args.per_round, args.log_file, args.number, args.repeat,
               args.strategy, args.load_model_file, args.load_log_file, args.alpha, args.beta,
               args.backward_window_size, args.search_policy, args.search_policy_params, args.adaptive_training,
               args.per_task_early_stopping)

    with auto_scheduler.ApplyHistoryBest(args.log_file):
        with tvm.transform.PassContext(opt_level=args.opt_level, config={'relay.backend.use_auto_scheduler': True}):
            lib = relay.build(mod, target=args.target, params=params)
    lib.export_library(args.output_file)


if __name__ == '__main__':
    sys.exit(main() or 0)
