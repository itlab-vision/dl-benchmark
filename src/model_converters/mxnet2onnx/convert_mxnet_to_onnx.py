import argparse
from mxnet.onnx import export_model


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .json file with a trained model.',
                        type=str,
                        dest='model_json')
    parser.add_argument('-w', '--weights',
                        help='Path to an .params file with a trained weights.',
                        type=str,
                        dest='model_params')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, '
                             'B is a batch size, '
                             'W is an input tensor width, '
                             'H is an input tensor height, '
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('-p', '--path_save_model',
                        help='Path to save model',
                        default='model.onnx',
                        type=str,
                        dest='path_save_model')

    args = parser.parse_args()

    return args


def convert_model(args):
    export_model(
        sym=args.model_json,
        params=args.model_params,
        in_shapes=[tuple(args.input_shape)],
        onnx_file_path=args.path_save_model
    )


def main():
    args = cli_argument_parser()
    convert_model(args)


if __name__ == '__main__':
    main()
