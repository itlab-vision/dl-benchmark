import argparse
import ast
import tensorflow as tf
import tf2onnx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--graphdef',
                        help='Path to the TensorFlow model graphdef file',
                        type=str,
                        dest='graphdef')
    parser.add_argument('--keras_model',
                        help='Path to the Keras model file (.h5)',
                        type=str,
                        dest='keras_model')
    parser.add_argument('--output',
                        help='Path to save the converted ONNX model',
                        required=True,
                        type=str,
                        dest='output')
    parser.add_argument('--input_name',
                        help='Name of the input tensor',
                        required=True,
                        type=str,
                        dest='input_name')
    parser.add_argument('--input_shape',
                        help='Shape of the input tensor as a Python list. '
                             'Should be in the format "[batch_size, height, width, channels]".',
                        required=True,
                        type=str,
                        dest='input_shape')
    parser.add_argument('--output_name',
                        help='Name of the output tensor',
                        type=str,
                        dest='output_name')

    args = parser.parse_args()
    return args


def main():
    args = cli_argument_parser()

    if args.graphdef:
        # Load the TensorFlow graph from the .pb file
        with tf.io.gfile.GFile(args.graphdef, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        try:
            # Convert input_shape string to a Python list
            input_shape = ast.literal_eval(args.input_shape)

            # Call tf2onnx convert function with provided arguments
            model_proto, _ = tf2onnx.convert.from_graph_def(
                graph_def,
                input_names=[args.input_name],
                output_names=[args.output_name],
                shape_override={args.input_name: input_shape},
                output_path=args.output,
            )

            # Print conversion success message and output path
            logger.info('Model successfully converted to ONNX.')
            logger.info(f'ONNX model saved at: {args.output}')
        except Exception as e:
            # If conversion fails, print error message
            logger.error(f'Conversion to ONNX failed: {e}')

    elif args.keras_model:
        try:
            # Load the Keras model
            model = tf.keras.models.load_model(args.keras_model)

            # Convert the Keras model to ONNX format
            model_proto, _ = tf2onnx.convert.from_keras(
                model,
                input_signature=[
                    tf.TensorSpec(
                        shape=ast.literal_eval(args.input_shape),
                        dtype=tf.float32,
                        name=args.input_name,
                    ),
                ],
                opset=13,  # Adjust opset version as needed
                output_path=args.output,
            )

            # Print conversion success message and output path
            logger.info('Model successfully converted to ONNX.')
            logger.info(f'ONNX model saved at: {args.output}')
        except Exception as e:
            # If conversion fails, print error message
            logger.error(f'Conversion to ONNX failed: {e}')


if __name__ == '__main__':
    main()
