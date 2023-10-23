import argparse
import logging as log
import sys

from tvm import autotvm, relay
from tvm.autotvm.tuner import XGBTuner, GATuner, RandomTuner, GridSearchTuner

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
                        help='Target device information.',
                        required=True,
                        type=str)
    parser.add_argument('-l', '--log',
                        help='Path to file for logging optimization results.',
                        required=True,
                        default='autotvm.log',
                        type=str,
                        dest='log_file')
    parser.add_argument('--tuner',
                        help='Method name for tuning the model.',
                        choices=[
                            'xgb', 'xgb_knob', 'xgb_itervar', 'xgb_curve', 'xgb_rank',
                            'xgb_rank_knob', 'xgb_rank_itervar', 'xgb_rank_curve', 'xgb_rank_binary',
                            'xgb_rank_binary_knob', 'xgb_rank_binary_itervar', 'xgb_rank_binary_curve',
                            'ga', 'random', 'gridsearch',
                        ],
                        default='xgb_rank',
                        type=str,
                        dest='tuner_name')
    parser.add_argument('--layer_names',
                        help='List of layer names be tuned. If not specified, all tunable layers will be extracted.',
                        default=None,
                        nargs='+',
                        dest='layer_names')
    parser.add_argument('--plan_size',
                        help='The size of a plan. After plan_size trials,'
                             'the tuner will refit a new cost model and do planing for the next plan_size trials.',
                        default=64,
                        type=int,
                        dest='plan_size')
    parser.add_argument('--pop_size',
                        help='Number of genes in one generation.',
                        default=100,
                        type=int)
    parser.add_argument('--elite_num',
                        help='Number of elite to keep.',
                        default=3,
                        type=int)
    parser.add_argument('--mutation_prob',
                        help='Probability of mutation of a knob in a gene.',
                        default=0.1,
                        type=float)
    parser.add_argument('--range_idx',
                        help='Probability of mutation of a knob in a gene.',
                        default=0.1,
                        nargs='+',
                        type=int)
    parser.add_argument('--number',
                        help='The number of times to run the generated code for taking average.'
                             'We call these runs as one repeat of measurement.',
                        default=4,
                        type=int)
    parser.add_argument('--repeat',
                        help='The number of times to repeat the measurement.'
                             'In total, the generated code will be run (1 + number x repeat) times,'
                             'where the first one is warm up and will be discarded.',
                        default=3,
                        type=int)
    parser.add_argument('--early_stopping',
                        help='Early stop the tuning when not finding better configs in this number of trials.',
                        default=100,
                        type=int)

    args = parser.parse_args()

    return args


def create_tuner(task, tuner, plan_size, pop_size, elite_num, mutation_prob, range_idx):
    if tuner == 'xgb':
        tuner_obj = XGBTuner(task, loss_type='reg', plan_size=plan_size)
    elif tuner == 'xgb_knob':
        tuner_obj = XGBTuner(task, loss_type='reg', feature_type='knob', plan_size=plan_size)
    elif tuner == 'xgb_itervar':
        tuner_obj = XGBTuner(task, loss_type='reg', feature_type='itervar', plan_size=plan_size)
    elif tuner == 'xgb_curve':
        tuner_obj = XGBTuner(task, loss_type='reg', feature_type='curve', plan_size=plan_size)
    elif tuner == 'xgb_rank':
        tuner_obj = XGBTuner(task, loss_type='rank', plan_size=plan_size)
    elif tuner == 'xgb_rank_knob':
        tuner_obj = XGBTuner(task, loss_type='rank', feature_type='knob', plan_size=plan_size)
    elif tuner == 'xgb_rank_itervar':
        tuner_obj = XGBTuner(task, loss_type='rank', feature_type='itervar', plan_size=plan_size)
    elif tuner == 'xgb_rank_curve':
        tuner_obj = XGBTuner(task, loss_type='rank', feature_type='curve', plan_size=plan_size)
    elif tuner == 'xgb_rank_binary':
        tuner_obj = XGBTuner(task, loss_type='rank-binary', plan_size=plan_size)
    elif tuner == 'xgb_rank_binary_knob':
        tuner_obj = XGBTuner(task, loss_type='rank-binary', feature_type='knob', plan_size=plan_size)
    elif tuner == 'xgb_rank_binary_itervar':
        tuner_obj = XGBTuner(task, loss_type='rank-binary', feature_type='itervar', plan_size=plan_size)
    elif tuner == 'xgb_rank_binary_curve':
        tuner_obj = XGBTuner(task, loss_type='rank-binary', feature_type='curve', plan_size=plan_size)
    elif tuner == 'ga':
        tuner_obj = GATuner(task, pop_size=pop_size, elite_num=elite_num, mutation_prob=mutation_prob)
    elif tuner == 'random':
        tuner_obj = RandomTuner(task)
    elif tuner == 'gridsearch':
        tuner_obj = GridSearchTuner(task, range_idx=range_idx)
    else:
        raise ValueError('Invalid tuner: ' + tuner)

    return tuner_obj


def extract_tasks(mod, params, target, layer_names):
    if layer_names is not None:
        ops = [relay.op.get(layer_name) for layer_name in layer_names]
    else:
        ops = None

    tasks = autotvm.task.extract_from_program(
        mod=mod, target=target, params=params, ops=ops,
    )
    return tasks


def tune_tasks(tasks, tuner_name, plan_size, pop_size, elite_num,
               mutation_prob, range_idx, number, repeat, early_stopping, log_file):

    for task in tasks:
        log.info(f'Tuning task {task}')
        tuner_obj = create_tuner(task, tuner_name, plan_size, pop_size, elite_num, mutation_prob, range_idx)
        n_trial = len(task.config_space)
        tuner_obj.tune(
            n_trial=n_trial,
            measure_option=autotvm.measure_option(
                builder=autotvm.LocalBuilder(),
                runner=autotvm.LocalRunner(number=number, repeat=repeat),
            ),
            early_stopping=early_stopping,
            callbacks=[
                autotvm.callback.log_to_file(log_file),
            ],
        )


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    log.config.dictConfig({'version': 1, 'disable_existing_loggers': True})

    args = cli_argument_parser()
    mod = utils.load_mod(args.model_json)
    params = utils.load_params(args.model_params)

    log.info('Extracting tasks using autotvm')
    tasks = extract_tasks(mod, params, args.target, args.layer_names)

    log.info('Neural network tuning')
    tune_tasks(tasks, args.tuner_name, args.plan_size, args.pop_size, args.elite_num,
               args.mutation_prob, args.range_idx, args.number, args.repeat, args.early_stopping, args.log_file)


if __name__ == '__main__':
    sys.exit(main() or 0)
