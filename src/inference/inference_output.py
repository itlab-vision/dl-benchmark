import os
import numpy as np
import logging as log
from copy import copy
import cv2


def classification_output(result, labels, number_top, log):
    log.info('Top {} results: \n'.format(number_top))
    if not labels:
        labels= os.path.join(os.path.dirname(__file__), 'image_net_synset.txt')
    with open(labels, 'r') as f:
        labels_map = [ x.split(sep = ' ', maxsplit = 1)[-1].strip() \
            for x in f ]
    for batch, probs in enumerate(result):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-number_top:][::-1]
        print("Result for image {}\n".format(batch + 1))
        for id in top_ind:
            det_label = labels_map[id] if labels_map else '#{}'.format(id)
            print('{:.7f} {}'.format(probs[id], det_label))
        print('\n')  


def segmentation_output(result, color_map, log):
    c = 3
    h, w = result.shape[1:]
    if not color_map:
        color_map = os.path.join(os.path.dirname(__file__), 'color_map.txt')
    classes_color_map = []
    with open(color_map, 'r') as f:
        for line in f:
            classes_color_map.append([int(x) for x in line.split()])
    for batch, data in enumerate(result):
        classes_map = np.zeros(shape = (h, w, c), dtype = np.int)
        for i in range(h):
            for j in range(w):
                pixel_class = int(data[i, j])
                classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
        out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch + 1))
        cv2.imwrite(out_img, classes_map)
        log.info('Result image was saved to {}'.format(out_img))


def detection_output(result, input, prob_threshold, log):
    ib, c, h, w = input.shape
    b, _, _, _ = result.shape
    images = np.ndarray(shape = (b, h, w, c))
    i = 0
    while i < b:
        images[i] = input[i % ib].transpose((1, 2, 0))
        i += 1
    for batch in range(b):
        for obj in result[batch][0]:
            if obj[2] > prob_threshold:
                image_number = int(obj[0])
                image = images[image_number]
                initial_h, initial_w = image.shape[:2]
                xmin = int(obj[3] * initial_w)
                ymin = int(obj[4] * initial_h)
                xmax = int(obj[5] * initial_w)
                ymax = int(obj[6] * initial_h)
                class_id = int(obj[1])
                color = (min(int(class_id * 12.5), 255), min(class_id * 7, 255),
                    min(class_id * 5, 255))
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
                log.info("Bounding boxes for image {0} for object {1}".format(image_number, class_id))
                log.info("Top left: ({0}, {1})".format(xmin, ymin))
                log.info("Bottom right: ({0}, {1})".format(xmax, ymax))

    count = 0
    for image in images:
        out_img = os.path.join(os.path.dirname(__file__), 'out_detection_{}.bmp'.format(count + 1))
        count += 1
        cv2.imwrite(out_img, image)
        log.info('Result image was saved to {}'.format(out_img))


def recognition_face_output(result, input, log):
    ib, c, h, w = input.shape
    b, _, _, _ = result.shape
    images = np.ndarray(shape = (b, h, w, c))
    i = 0
    while i < b:
        images[i] = input[i % ib].transpose((1, 2, 0))
        i += 1
    for i, r in enumerate(result):
        image = images[i]
        initial_h, initial_w = image.shape[:2]
        log.info('Landmarks coordinates for {} image'.format(i))
        for j in range (0, len(r), 2):
            index = int(j / 2) + 1
            x = int(r[j] * initial_w)
            y = int(r[j + 1] * initial_h)
            color = (0, 255, 255)
            cv2.circle(image, (x, y), 1, color, -1)
            log.info('Point {0} - ({1}, {2})'.format(index, x, y))
    count = 0
    for image in images:
        out_img = os.path.join(os.path.dirname(__file__), 'out_recognition_face_{}.bmp'.format(count + 1))
        count += 1
        cv2.imwrite(out_img, image)
        log.info('Result image was saved to {}'.format(out_img)) 


def infer_output(model, result, input, labels, number_top, prob_threshold,
        color_map, log, task):
    if task == 'feedforward':
        return
    elif result is None:
        log.warning("Model output is processed only for the number iteration = 1")
    elif task == 'classification':
        result_layer_name = next(iter(model.outputs))
        classification_output(result[result_layer_name], labels, number_top, log)
    elif task == 'detection':
        input_layer_name = next(iter(model.inputs))
        result_layer_name = next(iter(model.outputs))
        detection_output(result[result_layer_name], input[input_layer_name], prob_threshold, log)
    elif task == 'recognition-face':
        input_layer_name = next(iter(model.inputs))
        result_layer_name = next(iter(model.outputs))
        recognition_face_output(result[result_layer_name], input[input_layer_name], log)
    elif task == 'segmentation':
        result_layer_name = next(iter(model.outputs))
        segmentation_output(result[result_layer_name], color_map, log)