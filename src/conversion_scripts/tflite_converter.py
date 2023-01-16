import ast
import argparse
import copy
import shutil
import sys
import logging as log
from pathlib import Path

import onnx
from onnx_tf.backend import prepare

import tensorflow as tf
import tensorflow.compat.v1 as tf_v1
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants


def is_sequence(element):
    return isinstance(element, (list, tuple))


def shapes_arg(values):
    shapes = ast.literal_eval(values)
    if not is_sequence(shapes):
        raise argparse.ArgumentTypeError(f'{shapes}: must be a sequence')
    if not all(is_sequence(shape) for shape in shapes):
        shapes = (shapes, )
    for shape in shapes:
        if not is_sequence(shape):
            raise argparse.ArgumentTypeError(f'{shape}: must be a sequence')
        for value in shape:
            if not isinstance(value, int) or value < 0:
                raise argparse.ArgumentTypeError(f'Argument {value} must be a positive integer')
    return shapes


def input_parameter(parameter):
    input_name, value = parameter.split('=', 1)
    try:
        value = ast.literal_eval(value)
    except Exception as err:
        print((f'Cannot evaluate {value} value in {parameter}.'
               'For string values use "{input_name}=\'{value}\'" (with all quotes).'))
        sys.exit(err)
    return input_name, value


def parse_args():
    """Parse input arguments"""

    parser = argparse.ArgumentParser(description='Conversion of pretrained models to TensorFlowLite')

    parser.add_argument('--model-path', type=Path, required=True,
                        help='Path to model in TensorFlow or ONNX format')
    parser.add_argument('--input-names', type=str, nargs='+', metavar='L[,L...]', required=False,
                        help='Comma-separated names of the input layers')
    parser.add_argument('--input-shapes', metavar='SHAPE[,SHAPE...]', type=shapes_arg, required=False,
                        help='Comma-separated shapes of the input blobs. Example: [1,1,256,256],[1,3,256,256],...')
    parser.add_argument('--output-names', type=str, nargs='+', metavar='L[,L...]', required=False,
                        help='Comma-separated names of the output layers')
    parser.add_argument('--freeze-constant-input', type=input_parameter, default=[], action='append',
                        help='Pair "name"="value", replaces input layer with constant with provided value')
    parser.add_argument('--source-framework', type=str, required=True,
                        help='Source framework for convertion to TensorFlow Lite format')

    return parser.parse_args()


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


def load_saved_model(saved_model_dir):
    saved_model = tf.saved_model.load(saved_model_dir)
    model = saved_model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
    model._backref_to_saved_model = saved_model

    return model


def load_tf_model(file):
    model_type = file.suffix
    if model_type == '.pb':
        model = load_pb_file(file)
    elif model_type == '.meta':
        model = load_meta_file(file)

    return model


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


def get_saved_model_input_names(graph, input_names=None):
    if input_names is not None:
        return input_names

    input_names = []
    for input_signature in graph.structured_input_signature:
        if input_signature:
            input_names.extend(input_signature.keys())

    return input_names


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


def set_input_shapes(model, inputs):
    for i, _ in enumerate(inputs):
        input_name = model.inputs[i].name.split(':0')[0]
        input_shape = inputs.get(input_name, None)
        if input_shape is None:
            input_shape = inputs.get(f'{input_name}:0', model.inputs[i].shape)
        model.inputs[i].set_shape(input_shape)

    return model


def convert_to_tflite(concrete_function, output_file):
    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_function])

    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS,
    ]
    tflite_model = converter.convert()
    open(output_file, 'wb').write(tflite_model)


def create_new_onnx_model(opset_version, nodes, graph):
    new_graph = onnx.helper.make_graph(
        nodes,
        graph.name,
        graph.input,
        graph.output,
        initializer=graph.initializer,
    )

    new_model = onnx.helper.make_model(new_graph, producer_name='onnx-fix-nodes')
    new_model.opset_import[0].version = opset_version
    onnx.checker.check_model(new_model)

    return new_model


def fix_onnx_resize_nodes(model):
    opset_version = model.opset_import[0].version
    graph = model.graph

    new_nodes = []

    for node in graph.node:
        if node.op_type == 'Resize':
            new_resize = onnx.helper.make_node(
                'Resize',
                inputs=node.input,
                outputs=node.output,
                name=node.name,
                coordinate_transformation_mode='half_pixel',
                mode='linear',
            )

            new_nodes += [new_resize]
        else:
            new_nodes += [node]

    fixed_model = create_new_onnx_model(opset_version, new_nodes, graph)
    return fixed_model


def load_model(model_path, input_names, output_names, const_inputs, log):
    model_type = model_path.suffix
    if model_type:
        model_graph = load_tf_model(model_path)
        output_names = get_tf_output_names(model_graph, output_names)

        if model_type == '.meta':
            checkpoint_path = model_path.parent
            model_graph = freeze_metagraph(model_graph, checkpoint_path, output_names)

        if const_inputs:
            log.info('Freezing constant input')
            for const_input in const_inputs:
                model_graph = freeze_constant_input(model_graph, *const_input)

        input_names = get_tf_input_names(model_graph, input_names)

        model_path = model_path.parent / 'saved_model'
        if model_path.exists():
            shutil.rmtree(str(model_path))

        log.info('Converting to saved model')
        convert_to_saved_model(model_graph, input_names, output_names, str(model_path))

    return load_saved_model(model_path)


def main():
    args = parse_args()
    log.basicConfig(format='[ %(levelname)s ] %(message)s', level=log.INFO, stream=sys.stdout)
    if args.source_framework not in ['onnx', 'tf']:
        raise ValueError(f'Unsupported value {args.source_framework} for source-framework parameter')

    output_file = args.model_path.with_suffix('.tflite')

    if args.source_framework == 'onnx':
        onnx_model = onnx.load(args.model_path)
        args.model_path = args.model_path.parent / 'saved_model'
        log.info('Exporting onnx model to TF saved model')
        try:
            tf_model = prepare(onnx_model)
            tf_model.export_graph(args.model_path)
        except RuntimeError:
            half_pixel_model = fix_onnx_resize_nodes(onnx_model)
            tf_model = prepare(half_pixel_model)
            tf_model.export_graph(args.model_path)

    log.info('Loading TF model')
    model = load_model(args.model_path, args.input_names, args.output_names, args.freeze_constant_input, log)

    if args.input_shapes:
        log.info(f'Setting input shapes to {args.input_shapes}')
        input_names = get_saved_model_input_names(model, args.input_names)
        model = set_input_shapes(model, dict(zip(input_names, args.input_shapes)))

    log.info('Converting to tflite')
    convert_to_tflite(model, output_file)


if __name__ == '__main__':
    main()
