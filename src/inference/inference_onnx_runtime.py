import argparse
import json
import sys
import traceback
from pathlib import Path
from time import time

import numpy as np
import onnxruntime as onnx_rt

import postprocessing_data as pp
import preprocessing_data as prep
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import ONNXIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import ONNXRuntimeTransformer

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()

ORT_EXECUTION_MODE = {
    'ORT_SEQUENTIAL': onnx_rt.ExecutionMode.ORT_SEQUENTIAL,
    'ORT_PARALLEL': onnx_rt.ExecutionMode.ORT_PARALLEL,
}

ORT_EXECUTION_PROVIDERS_OPTIONS = {
    'CUDAExecutionProvider': {
        'device_id': 0,
        'arena_extend_strategy': 'kSameAsRequested',
        'cudnn_conv_algo_search': 'DEFAULT',
        'do_copy_in_default_stream': True,
        'cudnn_conv_use_max_workspace': '1',
        'cudnn_conv1d_pad_to_nc1d': '1',
    },
    'TensorrtExecutionProvider': {
        'device_id': 0,
        'trt_fp16_enable': False,
        'trt_max_workspace_size': 4294967296,
    },
}


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to file with a trained model.',
                        type=str,
                        required=True,
                        dest='model')
    parser.add_argument('-mn', '--model_name',
                        help='Name of model.',
                        type=str,
                        default=None,
                        dest='model_name')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--execution_providers',
                        help='Execution provider name (CPUExecutionProvider by default).',
                        default='CPUExecutionProvider',
                        type=prep.names_arg,
                        dest='execution_providers')
    parser.add_argument('--precision',
                        help='Run model in selected precision',
                        default=None,
                        type=str,
                        dest='precision')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification', 'yolo_v7_onnx', 'text-to-image', 'batch-text-generation'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('-in', '--input_names',
                        help='Input layer name',
                        default=None,
                        type=prep.names_arg,
                        dest='input_names')
    parser.add_argument('-on', '--output_names',
                        help='Output layer names',
                        default=None,
                        type=prep.names_arg,
                        dest='output_names')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        type=str,
                        dest='input_scale')
    parser.add_argument('--input_shapes',
                        help='Input tensor shapes',
                        default=None,
                        type=str,
                        dest='input_shapes')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=None,
                        type=str,
                        dest='mean')
    parser.add_argument('--channel_swap',
                        help='Parameter channel swap',
                        default=None,
                        type=str,
                        dest='channel_swap')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('-nthreads', '--number_threads',
                        help='Sets the number of threads used to parallelize the execution within nodes.',
                        default=0,
                        type=int,
                        dest='number_threads')
    parser.add_argument('--number_inter_threads',
                        help='Sets the number of threads used to parallelize the execution of the graph across nodes.',
                        default=0,
                        type=int,
                        dest='num_inter_threads')
    parser.add_argument('--execution_mode',
                        help='Sets the execution mode. Default is sequential.',
                        default='ORT_SEQUENTIAL',
                        type=str,
                        choices=['ORT_SEQUENTIAL', 'ORT_PARALLEL'],
                        dest='execution_mode')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'ort_inference_report.json',
                        dest='report_path')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
    args = parser.parse_args()

    return args


def set_session_options(number_threads, execution_mode, num_inter_threads):
    sess_options = onnx_rt.SessionOptions()
    sess_options.intra_op_num_threads = number_threads
    sess_options.execution_mode = ORT_EXECUTION_MODE[execution_mode]
    sess_options.graph_optimization_level = onnx_rt.GraphOptimizationLevel.ORT_ENABLE_ALL
    if execution_mode == 'ORT_PARALLEL':
        sess_options.inter_op_num_threads = num_inter_threads
    elif num_inter_threads > 0:
        log.warning('Perameter num_inter_threads is only set in ORT_PARALLEL mode')

    return sess_options


def create_inference_session(model, task_type, execution_providers, device, precision, session_options):
    log.info(f'Setting device to {device}')
    log.info(f'Setting execution providers to {execution_providers}')

    if task_type == 'text-to-image':
        from configs.onnx_configs.stable_diffusion import create_inference_session
        if len(execution_providers) > 1:
            log.warning('Cannot run with pipeline of providers, will use only first')
        provider_with_options = (execution_providers[0],
                                 ORT_EXECUTION_PROVIDERS_OPTIONS.get(execution_providers[0], {}))
        return create_inference_session(model,
                                        provider_with_options=provider_with_options,
                                        session_options=session_options,
                                        precision=precision)
    else:
        provider_options = []
        for provider in execution_providers:
            options = ORT_EXECUTION_PROVIDERS_OPTIONS.get(provider, {})
            if provider == 'OpenVINOExecutionProvider':
                options['device_type'] = device
            provider_options.append(options)
        session = onnx_rt.InferenceSession(
            model,
            providers=execution_providers,
            provider_options=provider_options,
            sess_options=session_options,
        )
        return session


def inference_onnx_runtime(session_or_pipeline, task_type, model_name, output_names, number_iter,
                           get_slice, test_duration, device):
    result = None
    time_infer = []
    num_tokens = None

    if task_type == 'batch-text-generation':
        from configs.pytorch_configs.causal_lm_base import create_tokenizer, tokenize
        from configs.onnx_configs.gpt_2 import batch_text_generation, MAX_TEXT_LEN

        tokenizer = create_tokenizer(model_name)
        encodings_dict = tokenize(tokenizer, get_slice())
        num_tokens = MAX_TEXT_LEN
    if number_iter == 1:
        if task_type not in ['batch-text-generation']:
            slice_input = get_slice()

        t0 = time()

        if task_type == 'text-to-image':
            result = session_or_pipeline(slice_input)
        elif task_type == 'batch-text-generation':
            result = batch_text_generation(ort_session=session_or_pipeline, tokenizer=tokenizer, device=device,
                                           output_names=output_names, encodings_dict=encodings_dict)
        else:
            result = session_or_pipeline.run(output_names, slice_input)

        t1 = time()
        time_infer.append(t1 - t0)
    else:
        time_infer = loop_inference(number_iter,
                                    test_duration)(inference_iteration)(get_slice, model_name, output_names,
                                                                        session_or_pipeline, task_type, device)

    return result, time_infer, num_tokens


def inference_iteration(get_slice, model_name, output_names, session, task_type, device):
    inputs = get_slice()
    _, exec_time = infer_slice(output_names, model_name, session, task_type, device, inputs)

    return exec_time


@get_exec_time()
def infer_slice(output_names, model_name, session_or_pipeline, task_type, device, slice_input):
    if task_type == 'text-to-image':
        res = session_or_pipeline(slice_input)
    elif task_type == 'batch-text-generation':
        from configs.pytorch_configs.causal_lm_base import create_tokenizer, tokenize
        from configs.onnx_configs.gpt_2 import batch_text_generation

        tokenizer = create_tokenizer(model_name)
        encodings_dict = tokenize(tokenizer, slice_input)

        res = batch_text_generation(ort_session=session_or_pipeline, tokenizer=tokenizer, device=device,
                                    output_names=output_names, encodings_dict=encodings_dict)
    else:
        res = session_or_pipeline.run(output_names, slice_input)

    return res


def prepare_output(result, output_names, model_name, task, args):
    if (output_names is None) or len(output_names) == 0:
        output_names = ['_output']

    if task == 'feedforward':
        return {}
    elif task == 'classification':
        return {output_names[0]: np.array(result).reshape(args.batch_size, -1)}
    elif task == 'yolo_v7_onnx':
        return result
    elif task == 'text-to-image':
        return result.images
    elif task == 'batch-text-generation':
        from configs.pytorch_configs.causal_lm_base import create_tokenizer, decode

        tokenizer = create_tokenizer(model_name)
        decoded_result = decode(tokenizer, result)

        return decoded_result
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='OnnxRuntime', version=onnx_rt.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    try:
        args.input_shapes = prep.parse_input_arg(args.input_shapes, args.input_names)
        model_wrapper = ONNXIOModelWrapper(args.input_shapes, args.batch_size)

        log.info('Setting inference session options')
        sess_options = set_session_options(args.number_threads, args.execution_mode, args.num_inter_threads)

        log.info(f'Creating inference session:\n\t {args.model}')
        inference_session = create_inference_session(args.model, args.task, args.execution_providers,
                                                     args.device, args.precision, sess_options)

        if args.task not in ['text-to-image']:
            args.input_names = model_wrapper.get_input_layer_names(inference_session)

        if args.model_name is None:
            args.model_name = Path(args.model).stem

        args.mean = prep.parse_input_arg(args.mean, args.input_names)
        args.input_scale = prep.parse_input_arg(args.input_scale, args.input_names)
        args.channel_swap = prep.parse_input_arg(args.channel_swap, args.input_names)
        args.layout = prep.parse_layout_arg(args.layout, args.input_names)

        data_transformer = ONNXRuntimeTransformer(prep.create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        if args.task not in ['text-to-image', 'batch-text-generation']:
            for layer_name in args.input_names:
                layer_shape = model_wrapper.get_input_layer_shape(inference_session, layer_name)
                log.info(f'Shape for input layer {layer_name}: {layer_shape}')

        if args.input:
            log.info('Preparing input data')
            io.prepare_input(inference_session, args.input)
        try:
            io.fill_unset_inputs(inference_session, log)
        except Exception:
            log.warning('Could not fill unset inputs')

        if args.task not in ['text-to-image']:
            if args.output_names is None:
                outputs = inference_session.get_outputs()
                args.output_names = [output.name for output in outputs]

        log.info(f'Starting inference ({args.number_iter} iterations)')
        result, inference_time, num_tokens = inference_onnx_runtime(
            session_or_pipeline=inference_session,
            task_type=args.task,
            model_name=args.model_name,
            output_names=args.output_names,
            number_iter=args.number_iter,
            get_slice=io.get_slice_input,
            test_duration=args.time,
            device=args.device)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time,
                                                                      num_tokens=num_tokens)

        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.model_name, args.task, args)
                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
