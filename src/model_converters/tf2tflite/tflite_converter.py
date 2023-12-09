import argparse
import ast
import logging as log
import sys
from pathlib import Path

import onnx
import tensorflow as tf
from onnx_tf.backend import prepare

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.model_converters.tf2tflite.tensorflow_common import load_model  # noqa


def is_sequence(element):
    return isinstance(element, (list, tuple))


def shapes_arg(values):
    shapes = ast.literal_eval(values)
    if not is_sequence(shapes):
        raise argparse.ArgumentTypeError(f'{shapes}: must be a sequence')
    if not all(is_sequence(shape) for shape in shapes):
        shapes = (shapes,)
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


def get_saved_model_input_names(graph, input_names=None):
    if input_names is not None:
        return input_names

    input_names = []
    for input_signature in graph.structured_input_signature:
        if input_signature:
            input_names.extend(input_signature.keys())

    return input_names


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


def set_input_shapes(model, inputs):
    for i, _ in enumerate(inputs):
        input_name = model.inputs[i].name.split(':0')[0]
        input_shape = inputs.get(input_name, None)
        if input_shape is None:
            input_shape = inputs.get(f'{input_name}:0', model.inputs[i].shape)
        model.inputs[i].set_shape(input_shape)

    return model


def main():
    args = parse_args()
    log.basicConfig(format='[ %(levelname)s ] %(message)s', level=log.INFO, stream=sys.stdout)
    if args.source_framework not in ['onnx', 'tf']:
        raise ValueError(f'Unsupported value {args.source_framework} for source-framework parameter')

    model_path = args.model_path.resolve(strict=True)

    output_file = model_path.with_suffix('.tflite')

    if args.source_framework == 'onnx':
        onnx_model = onnx.load(model_path)
        model_path = model_path.parent / 'saved_model'
        log.info('Exporting onnx model to TF saved model')
        tf_model = prepare(onnx_model)
        try:
            tf_model.export_graph(model_path)
        except RuntimeError:
            half_pixel_model = fix_onnx_resize_nodes(onnx_model)
            tf_model = prepare(half_pixel_model)
            tf_model.export_graph(model_path)

    log.info('Loading TF model')
    model, _ = load_model(model_path, args.input_names, args.output_names, args.freeze_constant_input, log)

    if args.input_shapes:
        log.info(f'Setting input shapes to {args.input_shapes}')
        input_names = get_saved_model_input_names(model, args.input_names)
        model = set_input_shapes(model, dict(zip(input_names, args.input_shapes)))

    log.info('Converting to tflite')
    convert_to_tflite(model, output_file)


if __name__ == '__main__':
    main()
