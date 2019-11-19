import os
import numpy as np
import logging as log
from copy import copy
import cv2


def classification_output(result, labels, number_top, log):
    log.info('Top {} results: \n'.format(number_top))
    if not labels:
        labels= 'image_net_synset.txt'
    with open(labels, 'r') as f:
        labels_map = [ x.split(sep = ' ', maxsplit = 1)[-1].strip() \
            for x in f ]
    image_count = 1
    for i, probs in enumerate(result):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-number_top:][::-1]
        print("Result for image {}\n".format(image_count))
        image_count += 1
        for id in top_ind:
            det_label = labels_map[id] if labels_map else '#{}'.format(id)
            print('{:.7f} {}'.format(probs[id], det_label))
        print('\n')  


def segmentation_output(result, color_map, log):
    c = 3
    h, w = result.shape[2:]
    if not color_map:
        color_map = 'color_map.txt'
    classes_color_map = []
    with open(color_map, 'r') as f:
        for line in f:
            classes_color_map.append([int(x) for x in line.split()])
    image_count = 1
    for batch, data in enumerate(result):
        classes_map = np.zeros(shape = (h, w, c), dtype = np.int)
        for i in range(h):
            for j in range(w):
                if len(data[:, i, j]) == 1:
                    pixel_class = int(data[:, i, j])
                else:
                    pixel_class = np.argmax(data[:, i, j])
                classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
        out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(image_count))
        image_count += 1
        cv2.imwrite(out_img, classes_map)
        log.info('Result image was saved to {}'.format(out_img))


def detection_output(result, data, prob_threshold):
    for i, r in enumerate(result):
        image = copy(data[i])
        initial_h, initial_w = image.shape[:2]
        for obj in r[0]:
            if obj[2] > prob_threshold:
                xmin = int(obj[3] * initial_w)
                ymin = int(obj[4] * initial_h)
                xmax = int(obj[5] * initial_w)
                ymax = int(obj[6] * initial_h)
                class_id = int(obj[1])
                color = (min(class_id * 12.5, 255), min(class_id * 7, 255),
                    min(class_id * 5, 255))
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.imshow('Detection Results', image)
        cv2.waitKey()
        cv2.destroyAllWindows()


def infer_output(result, input, labels, number_top, prob_threshold,
        color_map, log, task):
    if task == 'feedforward' or len(result) == 0:
        return
    elif task == 'classification':
        classification_output(result['prob'], labels, number_top, log)
    elif task == 'detection':
        detection_output(result['prob'], input['data'], prob_threshold)
    elif task == 'segmentation':
        segmentation_output(result['prob'], color_map, log)