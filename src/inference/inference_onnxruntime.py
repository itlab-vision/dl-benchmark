import cv2
import argparse
import numpy as np
import os
import sys
from PIL import Image
import onnxruntime as ort

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
    start_x = w//2 - crop_w//2
    start_y = h//2 - crop_h//2
    return image[start_y:start_y+crop_h, start_x:start_x+crop_w, :]

def prepare_input(mean, std, image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = image_resize(image, 256)

    mean_vec = np.array([0.485, 0.456, 0.406])
    stddev_vec = np.array([0.229, 0.224, 0.225])

    image = crop_center(image, 224, 224)
    img_data = image.astype('float32')
    out = np.zeros((1,1000))
    normir_image_data = np.zeros(img_data.shape).astype('float32')

    for i in range(img_data.shape[2]):
        normir_image_data[:,:,i] = (img_data[:,:,i]/255 - mean_vec[i]) / stddev_vec[i]

    cv2.imwrite("probe.bmp", normir_image_data)

def onnx_py_inference(image_path, model_path, labels_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mean_vec = np.array([0.485, 0.456, 0.406])
    stddev_vec = np.array([0.229, 0.224, 0.225])
    image = crop_center(image, 224, 224)
    image = image.transpose(2, 0 ,1)
    img_data = image.astype('float32')
    normir_image_data = np.zeros(img_data.shape).astype('float32')

    for i in range(img_data.shape[0]):
        normir_image_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]
    
    normir_image_data = normir_image_data.reshape(1, 3, 224, 224).astype('float32')
    ort_sess = ort.InferenceSession(model_path)
    input_name = ort_sess.get_inputs()[0].name
    output_name = ort_sess.get_outputs()[0].name
    outputs = ort_sess.run([output_name],{input_name:normir_image_data})
    result = np.argsort(outputs[0])[0,995:]

    with open(labels_path) as file:
        lines = file.readlines()
    for i in result[::-1]:
        print(lines[i], outputs[0][0][i])





def main():
    image_path = "../../img/ILSVRC2012_val_00000023.JPEG"
    model_path = "../../omz-models/mobilenetv2-12.onnx"
    labels_path = "labels/image_net_synset.txt"
    #onnx_py_inference(image_path, model_path, labels_path)
    prepare_input(0, 0, image_path)
    return 0

if __name__ == '__main__':
    sys.exit(main() or 0)
