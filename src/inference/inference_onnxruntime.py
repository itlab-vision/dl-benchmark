import cv2
import argparse
import numpy as np
import os
import sys
from PIL import Image
import tempfile


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',
                        help='Path to an .onnx file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-bch', '--benchmark_app',
                        help='Path to onnxruntime_benchmark',
                        required=True,
                        type=str,
                        dest='benchmark_path')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=True,
                        type=str,
                        dest='input')
    parser.add_argument('-w', '--weights',
                        help='Path to a model weights file',
                        required=False,
                        type=str,
                        default='',
                        dest='weights')
    parser.add_argument('-sh', '--shape',
                        help='Shape for network input <[N,C,H,W]>',
                        required=False,
                        default='',
                        type=str,
                        dest='shape')
    parser.add_argument('-l', '--labels_path',
                        help='Path to labels.txt file',
                        required=False,
                        default='',
                        type=str,
                        dest='labels_path')
    parser.add_argument('-mean',
                        help='Mean values in <[R,G,B]>',
                        required=False,
                        default='',
                        type=str,
                        dest='mean')
    parser.add_argument('-scale',
                        help='Scale values in <[R,G,B]>',
                        required=False,
                        default='',
                        type=str,
                        dest='scale')
    args = parser.parse_args()

    return args


def image_resize(image, min_len):
    image = Image.fromarray(image)
    ratio = float(min_len) / min(image.size[0], image.size[1])
    if image.size[0] > image.size[1]:
        new_size = (int(round(ratio * image.size[0])), min_len)
    else:
        new_size = (min_len, int(round(ratio * image.size[1])))
    image = image.resize(new_size, Image.BILINEAR)
    return np.array(image)


def crop_center(image, crop_w, crop_h):
    h, w, c = image.shape
    start_x = w // 2 - crop_w // 2
    start_y = h // 2 - crop_h // 2
    return image[start_y:start_y + crop_h, start_x:start_x + crop_w, :]


def prepare_input(image_path, temp_dir_path, cur_dir_path, name_of_output):
    image = cv2.imread(image_path)
    image = image_resize(image, 256)
    image = crop_center(image, 224, 224)
    img_data = image.astype('float32')
    os.chdir(temp_dir_path)
    cv2.imwrite(name_of_output, img_data)
    os.chdir(cur_dir_path)


def onnxruntime_benchmark_process(model, input_images, benchmark, num_of_images, dict_of_arguments):
    comm = f'./{benchmark} -m {model} -i {input_images} -niter 1 -nireq {num_of_images}'
    comm = comm + dict_of_arguments[' -w '] + dict_of_arguments[' --shape '] + dict_of_arguments[' --mean '] + dict_of_arguments[' --scale ']
    if dict_of_arguments[' -l '] != '':
        comm += ' --dump_flag'
    os.system(comm)


def output_process(labels_path, tmp_dir):
    print('\n')
    with open(labels_path) as file:
        classes = file.readlines()
        classes = [line.rstrip('\n') for line in classes]
    for i in range(0, len(os.listdir(tmp_dir.name))):
        out = np.loadtxt('output' + str(i))
        result = np.argsort(out)[995:]
        for j in result[::-1]:
            print(f'{classes[j]} {out[j]}')
        print('\n')
        os.remove('output' + str(i))


def std_transformer(std):
    std = std[1:-1]
    tmp = np.array(std.split(','), dtype=float)[::-1] * 255
    return f'[{tmp[0]},{tmp[1]},{tmp[2]}]'


def main():
    tmp = tempfile.TemporaryDirectory()
    cur_path = os.getcwd()
    args = cli_argument_parser()

    if args.mean != '' and args.scale != '':
        args.mean = std_transformer(args.mean)
        args.scale = std_transformer(args.scale)

    dict_of_arguments = {' -w ': args.weights,
                         ' --shape ': args.shape,
                         ' --mean ': args.mean,
                         ' --scale ': args.scale,
                         ' -l ': args.labels_path}

    for par, arg in dict_of_arguments.items():
        if arg != '':
            dict_of_arguments[par] = par + arg
    
    if os.path.isdir(args.input):
        for entry in os.scandir(args.input):
            if entry.is_file():
                print(entry.path)
                prepare_input(entry.path, tmp.name, cur_path, entry.name)
    else:
        prepare_input(args.input, tmp.name, cur_path, os.path.basename(args.input))
     
    onnxruntime_benchmark_process(args.model_path,
                                  args.input,
                                  args.benchmark_path,
                                  len(os.listdir(tmp.name)),
                                  dict_of_arguments)

    if args.labels_path != '':
        output_process(args.labels_path, tmp)
    
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
