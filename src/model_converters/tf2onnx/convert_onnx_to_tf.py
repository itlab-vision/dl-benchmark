import argparse
import onnx2tf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--onnx_model',
                        help='Path to the ONNX model file',
                        type=str,
                        required=True,
                        dest='onnx_model')
    parser.add_argument('--output',
                        help='Path to save the converted TensorFlow model',
                        required=True,
                        type=str,
                        dest='output')
    parser.add_argument('--output_keras_v3',
                        help='Output like keras_v3 model. True or False.',
                        type=str,
                        dest='output_keras_v3')
    parser.add_argument('--output_tfv1_pb',
                        help='Output like tfv1_model model. True or False.',
                        type=str,
                        dest='output_tfv1_pb')
    parser.add_argument('--input_shape',
                        help='Shape of the input tensor as a Python list. '
                             'Should be in the format "[batch_size, height, width, channels]".',
                        required=True,
                        type=str,
                        dest='input_shape')
    parser.add_argument('--input_name',
                        help='Name of the input tensor',
                        type=str,
                        dest='input_name')

    args = parser.parse_args()
    return args


def main():
    args = cli_argument_parser()

    try:
        # Convert the ONNX model to TensorFlow format
        onnx2tf.convert(
            input_onnx_file_path=args.onnx_model,
            output_folder_path=args.output,
            copy_onnx_input_output_names_to_tflite=True,
            non_verbose=False,
            output_tfv1_pb=args.output_tfv1_pb,
            output_keras_v3=args.output_keras_v3,
            overwrite_input_shape=[''.join(args.input_name.split() + ':'.split(' ') + args.input_shape.split(' '))],
        )

        # Print conversion success message and output path
        logger.info('Model successfully converted to TF.')
        logger.info(f'TF model saved at: {args.output}')
    except Exception as e:
        # If conversion fails, print error message
        logger.error(f'Conversion to TF failed: {e}')


if __name__ == '__main__':
    main()
