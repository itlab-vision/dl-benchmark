import argparse
import tensorflow as tf
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
            non_verbose=True,
        )

        # Print conversion success message and output path
        logger.info('Model successfully converted to ONNX.')
        logger.info(f'ONNX model saved at: {args.output}')
    except Exception as e:
        # If conversion fails, print error message
        logger.error(f'Conversion to ONNX failed: {e}')

    
if __name__ == '__main__':
    main()
