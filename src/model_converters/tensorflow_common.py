import copy
import shutil
from pathlib import Path

import tensorflow as tf
import tensorflow.compat.v1 as tf_v1
from tensorflow.python.saved_model import signature_constants, tag_constants


def load_saved_model(saved_model_dir, log):
    log.info(f'Loading saved model from {saved_model_dir}')
    saved_model = tf.saved_model.load(saved_model_dir)
    model = saved_model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
    model._backref_to_saved_model = saved_model
    return model


def load_pb_file(file):
    with tf_v1.io.gfile.GFile(file, 'rb') as f:
        graph_def = tf_v1.GraphDef()
        graph_def.ParseFromString(f.read())

        return graph_def


def load_meta_file(file):
    with open(file, 'rb') as f:
        graph_def = tf_v1.MetaGraphDef()
        graph_def.ParseFromString(f.read())

        return graph_def


def load_tf_model(file):
    model_type = file.suffix
    if model_type in ['.pb', '.frozen']:
        model = load_pb_file(file)
    elif model_type == '.meta':
        model = load_meta_file(file)
    else:
        raise ValueError(f'Unsupported file type: {model_type}')

    return model


def convert_to_saved_model(model_graph, input_names, output_names, saved_model_dir):
    builder = tf_v1.saved_model.builder.SavedModelBuilder(saved_model_dir)
    sigs = {}
    with tf_v1.Session(graph=tf_v1.Graph()) as sess:
        tf_v1.import_graph_def(model_graph, name='')
        g = tf_v1.get_default_graph()

        inputs = {}
        for input_name in input_names:
            inputs[input_name] = g.get_tensor_by_name(f'{input_name}:0')

        outputs = {}
        for output_name in output_names:
            outputs[output_name] = g.get_tensor_by_name(f'{output_name}:0')

        def_key = signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
        sigs[def_key] = tf_v1.saved_model.signature_def_utils.predict_signature_def(inputs, outputs)
        builder.add_meta_graph_and_variables(sess,
                                             [tag_constants.SERVING],
                                             signature_def_map=sigs)
        builder.save()


def get_tf_output_names(graph, output_names=None):
    if output_names is not None:
        return output_names

    nodes_map = {}
    try:
        nodes = graph.node
    except AttributeError:
        nodes = graph.graph_def.node

    for node in nodes:
        for parent in node.input:
            nodes_map.update({parent: nodes_map.get(parent, []) + [node.name]})

    not_outputs_types = {'Const', 'Assign', 'NoOp', 'Placeholder', 'Assert'}
    output_names = [
        x.name for x in nodes
        if x.name not in nodes_map and x.op not in not_outputs_types
    ]

    if not output_names:
        raise ValueError('No output blobs found, please set --output-names parameter')

    return output_names


def get_tf_input_names(graph, input_names=None):
    if input_names is not None:
        return input_names

    try:
        nodes = graph.node
    except AttributeError:
        nodes = graph.graph_def.node

    inputs_ops = {'Placeholder'}
    input_names = [x.name for x in nodes if not x.input and x.op in inputs_ops]

    if not input_names:
        raise ValueError('No input blobs found, please set --input-names parameter')

    return input_names


def load_model(model_path, input_names, output_names, const_inputs, log, saved_model_dir='auto'):
    if not model_path.is_dir():
        model_graph = load_tf_model(model_path)
        output_names = get_tf_output_names(model_graph, output_names)

        if model_path.suffix == '.meta':
            checkpoint_path = model_path.parent
            model_graph = freeze_metagraph(model_graph, checkpoint_path, output_names)

        if const_inputs:
            log.info('Freezing constant input')
            for const_input in const_inputs:
                model_graph = freeze_constant_input(model_graph, *const_input)

        if input_names is None:
            raise AssertionError('To load model in format differing from saved model Input names should be specified')
        input_names = get_tf_input_names(model_graph, input_names)

        if saved_model_dir == 'auto':
            model_path = model_path.parent / 'saved_model'
        else:
            model_path = Path(saved_model_dir)

        if model_path.exists():
            shutil.rmtree(str(model_path))

        log.info(f'Converting to saved model into folder {model_path}')
        convert_to_saved_model(model_graph, input_names, output_names, str(model_path))

    return load_saved_model(model_path, log), model_path


def freeze_constant_input(model_graph, constant_input_name, constant_value):
    new_graph_def = tf_v1.GraphDef()
    with tf_v1.Session(graph=tf_v1.Graph()):
        tf_v1.import_graph_def(model_graph, name='')

        c = tf.constant(constant_value, name=f'{constant_input_name}_1')

        for node in model_graph.node:
            if node.name == constant_input_name:
                new_graph_def.node.extend([c.op.node_def])
            else:
                node_inputs = node.input
                for i, node_input in enumerate(node_inputs):
                    if constant_input_name in node_input:
                        node.input[i] = node_input.replace(constant_input_name, f'{constant_input_name}_1')
                new_graph_def.node.extend([copy.deepcopy(node)])

    return new_graph_def


def freeze_metagraph(meta_graph, checkpoint_path, output_names):
    with tf_v1.Session() as sess:
        saver = tf_v1.train.import_meta_graph(meta_graph, clear_devices=True)
        saver.restore(sess, tf_v1.train.latest_checkpoint(checkpoint_path))
        frozen_graph_def = tf_v1.graph_util.convert_variables_to_constants(
            sess,
            sess.graph_def,
            output_names,
        )

    return frozen_graph_def


def convert_with_tensor_rt(input_saved_model_dir, output_model_dir, log, precision='FP32'):
    from tensorflow.python.compiler.tensorrt import trt_convert as trt

    log.info('Optimize model with tensorRT')
    if precision == 'FP32':
        precision_mode = trt.TrtPrecisionMode.FP32
    elif precision == 'FP16':
        precision_mode = trt.TrtPrecisionMode.FP16
    else:
        raise AssertionError(f'Unknown tensor-RT precision {precision}')

    # Conversion Parameters
    conversion_params = trt.TrtConversionParams(
        precision_mode=precision_mode,
    )

    converter = trt.TrtGraphConverterV2(
        input_saved_model_dir=str(input_saved_model_dir),
        conversion_params=conversion_params,
    )
    converter.convert()
    converter.summary()
    log.info(f'Save converted model to {output_model_dir}')
    converter.save(output_saved_model_dir=output_model_dir)


def get_gpu_devices():
    return tf.config.list_physical_devices('GPU')


def is_gpu_available():
    return len(get_gpu_devices()) > 0


def get_input_operation_name(input_name):
    input_op_name = [ts.split(':')[0] for ts in input_name] if input_name is not None else None
    return input_op_name
