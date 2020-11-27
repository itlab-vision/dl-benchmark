import os
import abc
import cv2
import numpy as np


class io_adapter(metaclass=abc.ABCMeta):
    def __init__(self, args, io_model_wrapper, transformer):
        self._input = None
        self._transformed_input = None
        self._original_shapes = None
        self._batch_size = args.batch_size
        self._labels = args.labels
        self._number_top = args.number_top
        self._threshold = args.threshold
        self._color_map = args.color_map
        self._io_model_wrapper = io_model_wrapper
        self._transformer = transformer

    def __convert_images(self, shape, data):
        c, h, w = self._transformer.get_shape_in_chw_order(shape)
        images = np.ndarray(shape=(len(data), c, h, w))
        image_shapes = []
        for i in range(len(data)):
            image = cv2.imread(data[i])
            image_shapes.append(image.shape[:-1])
            if (image.shape[:-1] != (h, w)):
                image = cv2.resize(image, (w, h))
            image = image.transpose((2, 0, 1))
            images[i] = image
        return images, image_shapes

    def __create_list_images(self, input):
        images = []
        input_is_correct = True
        if os.path.exists(input[0]):
            if os.path.isdir(input[0]):
                path = os.path.abspath(input[0])
                images = [os.path.join(path, file) for file in os.listdir(path)]
            elif os.path.isfile(input[0]):
                for image in input:
                    if not os.path.isfile(image):
                        input_is_correct = False
                        break
                    images.append(os.path.abspath(image))
            else:
                input_is_correct = False
        if not input_is_correct:
            raise ValueError('Wrong path to image or to directory with images')
        return images

    def __parse_tensors(self, filename):
        with open(filename, 'r') as file:
            input = file.readlines()
        input = [line.strip() for line in input]
        shape = [int(number) for number in input[0].split(';')]
        input.pop(0)
        value = []
        for str in input:
            value.append([float(number) for number in str.split(';')])
        result = np.array(value, dtype=np.float32)
        result = result.reshape(shape)
        return result

    def prepare_input(self, model, input):
        self._input = {}
        self._transformed_input = {}
        self._original_shapes = {}
        if ':' in input[0]:
            for str in input:
                key, value = str.split(':')
                file_format = value.split('.')[-1]
                if 'csv' == file_format:
                    value = self.__parse_tensors(value)
                    shapes = [value.shape]
                    transformed_value = value
                else:
                    value = value.split(',')
                    value = self.__create_list_images(value)
                    shape = self._io_model_wrapper.get_input_layer_shape(model, key)
                    value, shapes = self.__convert_images(shape, value)
                    transformed_value = self._transformer.transform_images(value)
                self._input.update({key: value})
                self._original_shapes.update({key: shapes})
                self._transformed_input.update({key: transformed_value})
        else:
            input_blob = shape = self._io_model_wrapper.get_input_layer_names(model)[0]
            file_format = input[0].split('.')[-1]
            if 'csv' == file_format:
                value = self.__parse_tensors(input[0])
                shapes = [value.shape]
                transformed_value = value
            else:
                value = self.__create_list_images(input)
                shape = self._io_model_wrapper.get_input_layer_shape(model, input_blob)
                value, shapes = self.__convert_images(shape, value)
                transformed_value = self._transformer.transform_images(value)
            self._input.update({input_blob: value})
            self._original_shapes.update({input_blob: shapes})
            self._transformed_input.update({input_blob: transformed_value})

    def get_slice_input(self, iteration):
        slice_input = dict.fromkeys(self._transformed_input.keys(), None)
        for key in self._transformed_input:
            slice_input[key] = self._transformed_input[key][
                (iteration * self._batch_size) % len(self._transformed_input[key]):
                (((iteration + 1) * self._batch_size - 1) % len(self._transformed_input[key])) + 1:
            ]
        return slice_input

    def _not_valid_result(self, result):
        return result is None

    @abc.abstractmethod
    def process_output(self, result, log):
        pass

    @staticmethod
    def get_io_adapter(args, io_model_wrapper, transformer):
        task = args.task
        if task == 'feedforward':
            return feedforward_io(args, io_model_wrapper, transformer)
        elif task == 'classification':
            return classification_io(args, io_model_wrapper, transformer)
        elif task == 'detection':
            return detection_io(args, io_model_wrapper, transformer)
        elif task == 'face-detection':
            return face_detection_io(args, io_model_wrapper, transformer)
        elif task == 'segmentation':
            return segmenatation_io(args, io_model_wrapper, transformer)
        elif task == 'adas-segmentation':
            return adas_segmenatation_io(args, io_model_wrapper, transformer)
        elif task == 'road-segmentation':
            return road_segmenatation_io(args, io_model_wrapper, transformer)
        elif task == 'recognition-face':
            return recognition_face_io(args, io_model_wrapper, transformer)
        elif task == 'person-attributes':
            return person_attributes_io(args, io_model_wrapper, transformer)
        elif task == 'age-gender':
            return age_gender_io(args, io_model_wrapper, transformer)
        elif task == 'gaze':
            return gaze_io(args, io_model_wrapper, transformer)
        elif task == 'head-pose':
            return head_pose_io(args, io_model_wrapper, transformer)
        elif task == 'person-detection-asl':
            return person_detection_asl_io(args, io_model_wrapper, transformer)
        elif task == 'license-plate':
            return license_plate_io(args, io_model_wrapper, transformer)
        elif task == 'instance-segmentation':
            return instance_segmenatation_io(args, io_model_wrapper, transformer)
        elif task == 'single-image-super-resolution':
            return single_image_super_resolution_io(args, io_model_wrapper, transformer)
        elif task == 'sphereface':
            return sphereface_io(args, io_model_wrapper, transformer)
        elif task == 'person-detection-action-recognition-old':
            return person_detection_action_recognition_old(args, io_model_wrapper, transformer)
        elif task == 'person-detection-action-recognition-new':
            return person_detection_action_recognition_new(args, io_model_wrapper, transformer)
        elif task == 'person-detection-raisinghand-recognition':
            return person_detection_raisinghand_recognition(args, io_model_wrapper, transformer)
        elif task == 'person-detection-action-recognition-teacher':
            return person_detection_action_recognition_teacher(args, io_model_wrapper, transformer)
        elif task == 'human-pose-estimation':
            return human_pose_estimation_io(args, io_model_wrapper, transformer)
        elif task == 'action-recognition-encoder':
            return action_recognition_encoder_io(args, io_model_wrapper, transformer)
        elif task == 'driver-action-recognition-encoder':
            return driver_action_recognition_encoder_io(args, io_model_wrapper, transformer)
        elif task == 'reidentification':
            return reidentification_io(args, io_model_wrapper, transformer)
        elif task == 'action-recognition-decoder':
            return action_recognition_decoder_io(args, io_model_wrapper, transformer)
        elif task == 'driver-action-recognition-decoder':
            return driver_action_recognition_decoder_io(args, io_model_wrapper, transformer)
        elif task == 'mask-rcnn':
            return mask_rcnn_io(args, io_model_wrapper, transformer)
        elif task == 'yolo_tiny_voc':
            return yolo_tiny_voc_io(args, io_model_wrapper, transformer)
        elif task == 'yolo_v2_voc':
            return yolo_v2_voc_io(args, io_model_wrapper, transformer)
        elif task == 'yolo_v2_coco':
            return yolo_v2_coco_io(args, io_model_wrapper, transformer)
        elif task == 'yolo_v2_tiny_coco':
            return yolo_v2_tiny_coco_io(args, io_model_wrapper, transformer)
        elif task == 'yolo_v3':
            return yolo_v3_io(args, io_model_wrapper, transformer)


class feedforward_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        return


class classification_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        log.info('Top {} results:'.format(self._number_top))
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/image_net_synset.txt')
        with open(self._labels, 'r') as f:
            labels_map = [line.strip() for line in f]
        for batch, probs in enumerate(result):
            probs = np.squeeze(probs)
            top_ind = np.argsort(probs)[-self._number_top:][::-1]
            log.info('Result for image {}'.format(batch + 1))
            for id in top_ind:
                det_label = labels_map[id] if labels_map else '#{}'.format(id)
                log.info('{:.7f} {}'.format(probs[id], det_label))


class detection_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        result_layer_name = next(iter(result))
        input = self._input[input_layer_name]
        result = result[result_layer_name]
        shapes = self._original_shapes[input_layer_name]
        ib = input.shape[0]
        b = result.shape[0]
        N = result.shape[2] // ib
        images = []
        for i in range(b * ib):
            orig_h, orig_w = shapes[i % ib]
            image = input[i % ib].transpose((1, 2, 0))
            images.append(cv2.resize(image, (orig_w, orig_h)))
        for batch in range(b):
            for out_num in range(ib):
                isbreak = False
                for obj in result[batch][0][out_num * N: (out_num + 1) * N]:
                    image_number = int(obj[0])
                    if image_number < 0:
                        isbreak = True
                        break
                    if obj[2] > self._threshold:
                        image = images[image_number + batch * ib]
                        initial_h, initial_w = image.shape[:2]
                        xmin = int(obj[3] * initial_w)
                        ymin = int(obj[4] * initial_h)
                        xmax = int(obj[5] * initial_w)
                        ymax = int(obj[6] * initial_h)
                        class_id = int(obj[1])
                        color = (
                            min(int(class_id * 12.5), 255),
                            min(class_id * 7, 255),
                            min(class_id * 5, 255)
                        )
                        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
                        log.info('Bounding boxes for image {0} for object {1}'.format(image_number, class_id))
                        log.info('Top left: ({0}, {1})'.format(xmin, ymin))
                        log.info('Bottom right: ({0}, {1})'.format(xmax, ymax))
                if isbreak:
                    break
        count = 0
        for image in images:
            out_img = os.path.join(os.path.dirname(__file__), 'out_detection_{}.bmp'.format(count + 1))
            cv2.imwrite(out_img, image)
            log.info('Result image was saved to {}'.format(out_img))
            count += 1


class face_detection_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        labels = result['labels']
        count_of_detected_faces = 0
        for i, label in enumerate(labels):
            if label == -1:
                count_of_detected_faces = i
                break
        boxes = result['boxes'][:count_of_detected_faces]
        input = self._input[input_layer_name]
        image = input[0].transpose((1, 2, 0))
        initial_h, initial_w = image.shape[:2]
        shapes = self._original_shapes[input_layer_name]
        orig_h, orig_w = shapes[0]
        image = cv2.resize(image, (orig_w, orig_h))
        face_id = 0
        for obj in boxes:
            if obj[4] > self._threshold:
                face_id += 1
                xmin = int(obj[0] * orig_w / initial_w)
                ymin = int(obj[1] * orig_h / initial_h)
                xmax = int(obj[2] * orig_w / initial_w)
                ymax = int(obj[3] * orig_h / initial_h)
                color = (0, 0, 0)
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
                log.info('Bounding boxes for face of person {0}'.format(face_id))
                log.info('Top left: ({0}, {1})'.format(xmin, ymin))
                log.info('Bottom right: ({0}, {1})'.format(xmax, ymax))
        out_img = os.path.join(os.path.dirname(__file__), 'out_face_detection.bmp')
        cv2.imwrite(out_img, image)
        log.info('Result image was saved to {}'.format(out_img))


class segmenatation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        shapes = self._original_shapes[next(iter(self._original_shapes))]
        c = 3
        h, w = result.shape[1:]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_maps/color_map.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        for batch, data in enumerate(result):
            classes_map = np.zeros(shape=(h, w, c), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    pixel_class = int(data[i, j])
                    classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
            out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch + 1))
            orig_h, orig_w = shapes[batch % self._batch_size]
            classes_map = cv2.resize(classes_map, (orig_w, orig_h))
            cv2.imwrite(out_img, classes_map)
            log.info('Result image was saved to {}'.format(out_img))


class adas_segmenatation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        shapes = self._original_shapes[next(iter(self._original_shapes))]
        c = 3
        h, w = result.shape[-2:]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_maps/color_map.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        for batch, data in enumerate(result):
            data = np.squeeze(data)
            classes_map = np.zeros(shape=(h, w, c), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    pixel_class = int(data[i, j])
                    classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
            out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch + 1))
            orig_h, orig_w = shapes[batch % self._batch_size]
            classes_map = cv2.resize(classes_map, (orig_w, orig_h))
            cv2.imwrite(out_img, classes_map)
            log.info('Result image was saved to {}'.format(out_img))


class road_segmenatation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        shapes = self._original_shapes[next(iter(self._original_shapes))]
        c = 3
        h, w = result.shape[2:]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_maps/color_map_road_segmentation.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        for batch, data in enumerate(result):
            data = data.transpose((1, 2, 0))
            classes_map = np.zeros(shape=(h, w, c), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    pixel_class = np.argmax(data[i][j])
                    classes_map[i, j, :] = classes_color_map[pixel_class]
            out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch + 1))
            orig_h, orig_w = shapes[batch % self._batch_size]
            classes_map = cv2.resize(classes_map, (orig_w, orig_h))
            cv2.imwrite(out_img, classes_map)
            log.info('Result image was saved to {}'.format(out_img))


class recognition_face_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        result_layer_name = next(iter(result))
        input = self._input[input_layer_name]
        result = result[result_layer_name]
        ib, c, h, w = input.shape
        b = result.shape[0]
        images = np.ndarray(shape=(b, h, w, c))
        for i in range(b):
            images[i] = input[i % ib].transpose((1, 2, 0))
        for i, r in enumerate(result):
            image = images[i]
            initial_h, initial_w = image.shape[:2]
            log.info('Landmarks coordinates for {} image'.format(i))
            for j in range(0, len(r), 2):
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


class person_attributes_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        input = self._input[input_layer_name]
        layer_iter = iter(result)
        result_attributes = result[next(layer_iter)]
        result_top = result[next(layer_iter)]
        result_bottom = result[next(layer_iter)]
        b = result_attributes.shape[0]
        ib, c, h, w = input.shape
        images = np.ndarray(shape=(b, h, w * 4, c))
        attributes = [
            'is_male',
            'has_bag',
            'has_backpack',
            'has_hat',
            'has_longsleeves',
            'has_longpants',
            'has_longhair',
            'has_coat_jacket'
        ]
        color_point = (0, 0, 255)
        for i in range(b):
            for x in range(w):
                for y in range(h):
                    images[i][y][x] = input[i % ib].transpose((1, 2, 0))[y][x]
            x_top = int(result_top[i][0] * w)
            y_top = int(result_top[i][1] * h)
            x_bottom = int(result_bottom[i][0] * w)
            y_bottom = int(result_bottom[i][1] * h)
            color_top = (
                int(images[i][y_top][x_top][0]),
                int(images[i][y_top][x_top][1]),
                int(images[i][y_top][x_top][2])
            )
            color_bottom = (
                int(images[i][y_bottom][x_bottom][0]),
                int(images[i][y_bottom][x_bottom][1]),
                int(images[i][y_bottom][x_bottom][2])
            )
            cv2.circle(images[i], (x_top, y_top), 3, color_point, -1)
            cv2.circle(images[i], (x_bottom, y_bottom), 3, color_point, -1)
            for x in range(w, 2 * w):
                for y in range(0, int(h / 2)):
                    images[i][y][x] = color_top
                    images[i][y + int(h / 2)][x] = color_bottom
            for j, val in enumerate(result_attributes[i]):
                color_attribut = (0, 255 * bool(val > 0.5), 255 * bool(val <= 0.5))
                cv2.putText(
                    images[i],
                    '{0} {1}'.format(attributes[j], bool(val > 0.5)),
                    (w * 2 + 5, 20 + j * 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    color_attribut
                )
        count = 0
        for image in images:
            out_img = os.path.join(os.path.dirname(__file__), 'out_person_attributes_{}.bmp'.format(count + 1))
            count += 1
            cv2.imwrite(out_img, image)
            log.info('Result image was saved to {}'.format(out_img))


class age_gender_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        layer_iter = iter(result)
        result_age = result[next(layer_iter)]
        result_gender = result[next(layer_iter)]
        b = result_age.shape[0]
        gender = ['Male', 'Female']
        for i in range(b):
            log.info('Information for {} image'.format(i))
            log.info('Gender: {}'.format(gender[bool(result_gender[i][0] > 0.5)]))
            log.info('Years: {:.2f}'.format(result_age[i][0][0][0] * 100))


class gaze_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result = result[next(iter(result))]
        b = result.shape[0]
        input_angles = self._input['head_pose_angles']
        input_left_eye = self._input['left_eye_image']
        input_right_eye = self._input['right_eye_image']
        ib, c, h, w = input_left_eye.shape
        images = np.ndarray(shape=(b, h, w * 2, c))
        images_left_eye = np.ndarray(shape=(b, h, w, c))
        images_right_eye = np.ndarray(shape=(b, h, w, c))
        center_x = int(w / 2)
        center_y = int(h / 2)
        color = (255, 0, 0)
        for i in range(b):
            images_left_eye[i] = input_left_eye[i % ib].transpose((1, 2, 0))
            images_right_eye[i] = input_right_eye[i % ib].transpose((1, 2, 0))
            roll = input_angles[i][1] * np.pi / 180.0
            vector_length = np.linalg.norm(result[i])
            vector_x = result[i][0] / vector_length
            vector_y = result[i][1] / vector_length
            gaze_x = int((vector_x * np.cos(roll) - vector_y * np.sin(roll)) * 50)
            gaze_y = int((vector_x * np.sin(roll) + vector_y * np.cos(roll)) * -50)
            cv2.line(images_left_eye[i], (center_x, center_y), (center_x + gaze_x, center_y + gaze_y), color, 2)
            cv2.line(images_right_eye[i], (center_x, center_y), (center_x + gaze_x, center_y + gaze_y), color, 2)
            for x in range(w):
                for y in range(h):
                    images[i][y][x] = images_left_eye[i % ib][y][x]
                    images[i][y][x + w] = images_right_eye[i % ib][y][x]
        count = 0
        for image in images:
            out_img = os.path.join(os.path.dirname(__file__), 'out_gaze_{}.bmp'.format(count + 1))
            count += 1
            cv2.imwrite(out_img, image)
            log.info('Result image was saved to {}'.format(out_img))


class head_pose_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        input = self._input[input_layer_name]
        result_pitch = result['angle_p_fc']
        result_roll = result['angle_r_fc']
        result_yaw = result['angle_y_fc']
        b = result_pitch.shape[0]
        ib, c, h, w = input.shape
        images = np.ndarray(shape=(b, h, w, c))
        center_x = int(w / 2)
        center_y = int(h / 2)
        color_x = (0, 0, 255)
        color_y = (0, 255, 0)
        color_z = (255, 0, 0)
        focal_length = 950.0
        for i in range(b):
            images[i] = input[i % ib].transpose((1, 2, 0))
            yaw = result_yaw[i][0] * np.pi / 180.0
            pitch = result_pitch[i][0] * np.pi / 180.0
            roll = result_roll[i][0] * np.pi / 180.0
            Rx = np.array([
                [1, 0, 0],
                [0, np.cos(pitch), -np.sin(pitch)],
                [0, np.sin(pitch), np.cos(pitch)]
            ])
            Ry = np.array([
                [np.cos(yaw), 0, -np.sin(yaw)],
                [0, 1, 0],
                [np.sin(yaw), 0, np.cos(yaw)]
            ])
            Rz = np.array([
                [np.cos(roll), -np.sin(roll), 0],
                [np.sin(roll), np.cos(roll), 0],
                [0, 0, 1]
            ])
            R = np.dot(Rx, np.dot(Ry, Rz))
            o = np.array(([0, 0, 0]), dtype='float32').reshape(3, 1)
            o[2] = focal_length
            X = np.dot(R, np.array(([25, 0, 0]), dtype='float32').reshape(3, 1)) + o
            Y = np.dot(R, np.array(([0, -25, 0]), dtype='float32').reshape(3, 1)) + o
            Z = np.dot(R, np.array(([0, 0, -25]), dtype='float32').reshape(3, 1)) + o
            Z1 = np.dot(R, np.array(([0, 0, 25]), dtype='float32').reshape(3, 1)) + o
            point_x = int(X[0] / X[2] * focal_length) + center_x
            point_y = int(X[1] / X[2] * focal_length) + center_y
            cv2.line(images[i], (center_x, center_y), (point_x, point_y), color_x)
            point_x = int(Y[0] / Y[2] * focal_length) + center_x
            point_y = int(Y[1] / Y[2] * focal_length) + center_y
            cv2.line(images[i], (center_x, center_y), (point_x, point_y), color_y)
            point_x = int(Z[0] / Z[2] * focal_length) + center_x
            point_y = int(Z[1] / Z[2] * focal_length) + center_y
            point_x1 = int(Z1[0] / Z1[2] * focal_length) + center_x
            point_y1 = int(Z1[1] / Z1[2] * focal_length) + center_y
            cv2.line(images[i], (point_x1, point_y1), (point_x, point_y), color_z)
        for i in range(b):
            out_img = os.path.join(os.path.dirname(__file__), 'out_head_pose_{}.bmp'.format(i + 1))
            cv2.imwrite(out_img, images[i])
            log.info('Result image was saved to {}'.format(out_img))
        file_angles = os.path.join(os.path.dirname(__file__), 'out_head_pose.csv')
        with open(file_angles, 'w+') as f:
            f.write('{};3\n'.format(b))
            for i in range(b):
                f.write('{:.3f};{:.3f};{:.3f}\n'.format(result_pitch[i][0], result_roll[i][0], result_yaw[i][0]))
        log.info('Result angles was saved to {}'.format(file_angles))


class person_detection_asl_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        input = self._input[input_layer_name]
        result = result['17701/Split.0']
        _, c, h, w = input.shape
        images = np.ndarray(shape=(1, h, w, c))
        images[0] = input[0].transpose((1, 2, 0))
        count = 0
        for obj in result:
            if obj[4] > self._threshold:
                count += 1
                xmin = int(obj[0])
                ymin = int(obj[1])
                xmax = int(obj[2])
                ymax = int(obj[3])
                color = (0, 0, 255)
                cv2.rectangle(images[0], (xmin, ymin), (xmax, ymax), color, 2)
                log.info('Object {} box:'.format(count))
                log.info('Top left: ({0}, {1})'.format(xmin, ymin))
                log.info('Bottom right: ({0}, {1})'.format(xmax, ymax))
        out_img = os.path.join(os.path.dirname(__file__), 'out_person_detection_asl.bmp')
        cv2.imwrite(out_img, images[0])
        log.info('Result image was saved to {}'.format(out_img))


class license_plate_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def get_slice_input(self, iteration):
        slice_input = dict.fromkeys(self._input.keys(), None)
        slice_input['data'] = self._input['data'][
            (iteration * self._batch_size) % len(self._input['data']):
            (((iteration + 1) * self._batch_size - 1) % len(self._input['data'])) + 1:
        ]
        slice_input['seq_ind'] = self._input['seq_ind'][
            (iteration * 88 * self._batch_size) % len(self._input['seq_ind']):
            (((iteration + 1) * 88 * self._batch_size - 1) % len(self._input['seq_ind'])) + 1:
        ]
        return slice_input

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result = result[next(iter(result))]
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/dictionary.txt')
        lexis = []
        with open(self._labels, 'r') as f:
            lexis = [line.strip() for line in f]
        for lex in result:
            s = ''
            for j in range(lex.shape[0]):
                if (lex[j] == -1):
                    break
                s = s + str(lexis[int(lex[j])])
            log.info('Plate: {}'.format(s))


class instance_segmenatation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_maps/mscoco_color_map.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/mscoco_names.txt')
        labels_map = []
        labels_map.append('background')
        with open(self._labels, 'r') as f:
            for line in f:
                labels_map.append(line.strip())
        shapes = self._original_shapes[next(iter(self._original_shapes))]
        image = self._input['im_data'][0].transpose((1, 2, 0))
        boxes = result['boxes']
        scores = result['scores']
        classes = result['classes'].astype(np.uint32)
        masks = result['raw_masks']
        labels_on_image = []
        for i in range(len(classes)):
            if (scores[i] > self._threshold):
                object_width = boxes[i][2] - boxes[i][0]
                object_height = boxes[i][3] - boxes[i][1]
                mask = masks[i][classes[i]]
                label_on_image_point = (int(boxes[i][0] + object_width / 3), int(boxes[i][3] - object_height / 2))
                label_on_image = '<' + labels_map[classes[i]] + '>'
                labels_on_image.append((label_on_image, label_on_image_point))
                for j in range(len(mask)):
                    for k in range(len(mask[j])):
                        if (mask[j][k] > self._threshold):
                            dh = int(object_height / len(mask))
                            dw = int(object_width / len(mask[j]))
                            x = int(boxes[i][0] + k * dw)
                            y = int(boxes[i][1] + j * dh)
                            for c in range(dh):
                                for t in range(dw):
                                    image[y + c][x + t] = classes_color_map[classes[i] - 1]
        for i in range(len(labels_on_image)):
            image = cv2.putText(
                image,
                labels_on_image[i][0],
                labels_on_image[i][1],
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1
            )
        out_img = os.path.join(os.path.dirname(__file__), 'instance_segmentation_out.bmp')
        orig_h, orig_w = shapes[0]
        image = cv2.resize(image, (orig_w, orig_h))
        cv2.imwrite(out_img, image)
        log.info('Result image was saved to {}'.format(out_img))


class single_image_super_resolution_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        c = 3
        h, w = result.shape[2:]
        for batch, data in enumerate(result):
            classes_map = np.zeros(shape=(h, w, c), dtype=np.uint8)
            colors = data * 255
            np.clip(colors, 0., 255.)
            classes_map = colors.transpose((1, 2, 0))
            out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.png'.format(batch + 1))
            cv2.imwrite(out_img, classes_map)
            log.info('Result image was saved to {}'.format(out_img))


class sphereface_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result = result[next(iter(result))]
        file_name = os.path.join(os.path.dirname(__file__), 'sphereface_out.csv')
        with open(file_name, 'w+'):
            np.savetxt(
                'sphereface_out.csv',
                result,
                fmt='%1.2f',
                delimiter=';',
                header='{};{}'.format(result.shape[0], result.shape[1]),
                comments=''
            )
        log.info('Result was saved to {}'.format(file_name))


class detection_ssd(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    @abc.abstractmethod
    def _get_action_map(self):
        pass

    def _parse_det_conf(self, detection_conf_data, i):
        return detection_conf_data[i * 2 + 1]

    def _parse_action(self, action_data, position, num_classes, scale, shift=1):
        action_exp_max = 0.
        action_exp_sum = 0.
        action_id = -1
        action_threshold = 0.75
        for num in range(num_classes):
            action_exp = np.exp(scale * action_data[position + num * shift])
            action_exp_sum += action_exp
            if action_exp > action_exp_max:
                action_exp_max = action_exp
                action_id = num
        action_conf = action_exp_max / action_exp_sum
        if action_conf < action_threshold:
            action_id = 0
            action_conf = 0.
        return action_id, action_conf

    @abc.abstractmethod
    def _parse_prior_box(self, prior_data, i, w=0, h=0):
        pass

    @abc.abstractmethod
    def _parse_variance_box(self, prior_data=None, i=0):
        pass

    @abc.abstractmethod
    def _parse_encoded_box(self, encoded_data, i):
        pass

    def _parse_decoded_bbox(self, prior_box, variance_box, encoded_box, w, h):
        prior_width = prior_box[2] - prior_box[0]
        prior_height = prior_box[3] - prior_box[1]
        prior_xcenter = (prior_box[2] + prior_box[0]) / 2
        prior_ycenter = (prior_box[3] + prior_box[1]) / 2
        decoded_xcenter = variance_box[0] * encoded_box[0] * prior_width + prior_xcenter
        decoded_ycenter = variance_box[1] * encoded_box[1] * prior_height + prior_ycenter
        decoded_width = np.exp(variance_box[2] * encoded_box[2]) * prior_width
        decoded_height = np.exp(variance_box[3] * encoded_box[3]) * prior_height
        decoded_xmin = int((decoded_xcenter - 0.5 * decoded_width) * w)
        decoded_ymin = int((decoded_ycenter - 0.5 * decoded_height) * h)
        decoded_xmax = int((decoded_xcenter + 0.5 * decoded_width) * w)
        decoded_ymax = int((decoded_ycenter + 0.5 * decoded_height) * h)
        decoded_bbox = [decoded_xmin, decoded_ymin, decoded_xmax, decoded_ymax]
        return decoded_bbox

    def _non_max_supression(self, detections, det_threshold):
        detections.sort(key=lambda detection: detection[0], reverse=True)
        valid_detections = []
        for idx in range(len(detections)):
            max_detection = max(detections, key=lambda detection: detection[0])
            if max_detection[0] < det_threshold:
                break
            valid_detections.append(max_detection)
            max_detection[0] = 0
            for detection in detections:
                if detection[0] < det_threshold:
                    continue
                current_rect_area = (
                    (detection[1][2] - detection[1][0]) *
                    (detection[1][3] - detection[1][1])
                )
                max_rect_area = (
                    (max_detection[1][2] - max_detection[1][0]) *
                    (max_detection[1][3] - max_detection[1][1])
                )
                intersection_area = 0
                if not (detection[1][0] >= max_detection[1][2] or
                        detection[1][1] >= max_detection[1][3] or
                        max_detection[1][0] >= detection[1][2] or
                        max_detection[1][1] >= detection[1][3]):
                    intersection_area = (
                        (min(detection[1][2], max_detection[1][2]) -
                         max(detection[1][0], max_detection[1][0])) *
                        (min(detection[1][3], max_detection[1][3]) -
                         max(detection[1][1], max_detection[1][1]))
                    )
                overlap = intersection_area / (current_rect_area + max_rect_area - intersection_area)
                detection[0] *= np.exp(-overlap * overlap / 0.6)
        return valid_detections

    def _draw_detections(self, images, batch, valid_detections, action_map, h, w):
        image = cv2.resize(images[batch], (w, h))
        rect_color = (255, 255, 255)
        for detection in valid_detections:
            left_point = (detection[1][0], detection[1][1])
            right_point = (detection[1][2], detection[1][3])
            cv2.rectangle(image, left_point, right_point, rect_color, 1)
            action_color = (0, 0, 0)
            if detection[3] == 0:
                action_color = (0, 255, 0)
            else:
                action_color = (0, 0, 255)
            text_area = (detection[1][0], detection[1][1] + 10)
            cv2.putText(
                image,
                action_map[detection[3]],
                text_area,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                action_color
            )
        return image

    def _save_output_images(self, images, log):
        count = 0
        for image in images:
            out_img = os.path.join(os.path.dirname(__file__), 'out_human_pose_{}.bmp'.format(count + 1))
            count += 1
            cv2.imwrite(out_img, image)
            log.info('Result image was saved to {}'.format(out_img))

    @abc.abstractmethod
    def process_output(self, result, log):
        pass


class detection_ssd_old_format(detection_ssd):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _parse_prior_box(self, prior_data, i, w=0, h=0):
        prior_xmin = prior_data[i * 4]
        prior_ymin = prior_data[i * 4 + 1]
        prior_xmax = prior_data[i * 4 + 2]
        prior_ymax = prior_data[i * 4 + 3]
        return prior_xmin, prior_ymin, prior_xmax, prior_ymax

    def _parse_variance_box(self, prior_data=None, i=0):
        variance_xmin = prior_data[(4300 + i) * 4]
        variance_ymin = prior_data[(4300 + i) * 4 + 1]
        variance_xmax = prior_data[(4300 + i) * 4 + 2]
        variance_ymax = prior_data[(4300 + i) * 4 + 3]
        return variance_xmin, variance_ymin, variance_xmax, variance_ymax

    def _parse_encoded_box(self, encoded_data, i):
        encoded_xmin = encoded_data[i * 4]
        encoded_ymin = encoded_data[i * 4 + 1]
        encoded_xmax = encoded_data[i * 4 + 2]
        encoded_ymax = encoded_data[i * 4 + 3]
        return encoded_xmin, encoded_ymin, encoded_xmax, encoded_ymax

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        input = self._input[input_layer_name]
        b, c, h, w = input.shape
        images = np.ndarray(shape=(b, h, w, c))
        for i in range(b):
            images[i] = input[i].transpose((1, 2, 0))
        detections = []
        action_map = self._get_action_map()
        num_classes = len(action_map)
        prior_data = result['mbox/priorbox'].flatten()
        shapes = self._original_shapes[input_layer_name]
        output_images = []
        for batch in range(b):
            orig_h, orig_w = shapes[batch]
            encoded_data = result['mbox_loc1/out/conv/flat'][batch]
            detection_conf_data = result['mbox_main_conf/out/conv/flat/softmax/flat'][batch]
            action_blobs = np.ndarray(shape=(4, 25, 43, num_classes))
            for i in range(4):
                action_blobs[i] = result['out/anchor{}'.format(i + 1)][batch]
            for i in range(4300):
                detection_conf = self._parse_det_conf(detection_conf_data, i)
                if detection_conf < self._threshold:
                    continue
                action_data = action_blobs[i % 4].flatten()
                action_id, action_conf = self._parse_action(
                    action_data,
                    i // 4 * num_classes,
                    num_classes,
                    3
                )
                prior_box = self._parse_prior_box(prior_data, i)
                variance_box = self._parse_variance_box(prior_data, i)
                encoded_box = self._parse_encoded_box(encoded_data, i)
                decoded_bbox = self._parse_decoded_bbox(prior_box, variance_box, encoded_box, orig_w, orig_h)
                detection = [detection_conf, decoded_bbox, action_conf, action_id]
                detections.append(detection)
            valid_detections = self._non_max_supression(detections, self._threshold)
            output_images.append(self._draw_detections(images, batch, valid_detections, action_map, orig_h, orig_w))
        self._save_output_images(output_images, log)


class detection_ssd_new_format(detection_ssd):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _parse_prior_box(self, prior_data, i, w, h):
        blob_size, step = [], 0
        if i < 4250:
            blob_size = [50, 85]
            step = 8
        else:
            blob_size = [43, 25]
            step = 16
            i = (i - 4250) // 4
        row = i // blob_size[0]
        col = i % blob_size[0]
        xcenter = (col + 0.5) * step
        ycenter = (row + 0.5) * step
        prior_xmin = (xcenter - 0.5 * prior_data[0]) / w
        prior_ymin = (ycenter - 0.5 * prior_data[1]) / h
        prior_xmax = (xcenter + 0.5 * prior_data[0]) / w
        prior_ymax = (ycenter + 0.5 * prior_data[1]) / h
        return prior_xmin, prior_ymin, prior_xmax, prior_ymax

    def _parse_variance_box(self, prior_data=None, i=0):
        return 0.1, 0.1, 0.2, 0.2

    def _parse_encoded_box(self, encoded_data, i):
        encoded_xmin = encoded_data[i * 4 + 1]
        encoded_ymin = encoded_data[i * 4]
        encoded_xmax = encoded_data[i * 4 + 3]
        encoded_ymax = encoded_data[i * 4 + 2]
        return encoded_xmin, encoded_ymin, encoded_xmax, encoded_ymax

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        input_layer_name = next(iter(self._input))
        input = self._input[input_layer_name]
        b, c, h, w = input.shape
        images = np.ndarray(shape=(b, h, w, c))
        for i in range(b):
            images[i] = input[i].transpose((1, 2, 0))
        detections = []
        action_map = self._get_action_map()
        num_classes = len(action_map)
        main_anchor = [26.17863728, 58.670372]
        anchors = [
            [35.36, 81.829632],
            [45.8114572, 107.651852],
            [63.31491832, 142.595732],
            [93.5070856, 201.107692]
        ]
        shapes = self._original_shapes[input_layer_name]
        output_images = []
        for batch in range(b):
            orig_h, orig_w = shapes[batch]
            encoded_data = result['ActionNet/out_detection_loc'][batch].flatten()
            detection_conf_data = result['ActionNet/out_detection_conf'][batch].flatten()
            main_action_data = result['ActionNet/action_heads/out_head_1_anchor_1'][batch].flatten()
            action_blobs = np.ndarray(shape=(4, 6, 25, 43))
            for i in range(4):
                action_blobs[i] = result['ActionNet/action_heads/out_head_2_anchor_{}'.format(i + 1)][batch]
            detections = []
            for i in range(8550):
                detection_conf = self._parse_det_conf(detection_conf_data, i)
                if detection_conf < self._threshold:
                    continue
                action_data = []
                action_id, action_conf = 0, 0.
                if i < 4250:
                    action_data = main_action_data
                    action_id, action_conf = self._parse_action(
                        main_action_data,
                        i,
                        num_classes,
                        16,
                        4250
                    )
                else:
                    action_data = action_blobs[(i - 4250) % 4].flatten()
                    action_id, action_conf = self._parse_action(
                        action_data,
                        (i - 4250) // 4,
                        num_classes,
                        16,
                        1075
                    )
                prior_box = []
                if i < 4250:
                    prior_box = self._parse_prior_box(main_anchor, i, w, h)
                else:
                    prior_box = self._parse_prior_box(anchors[(i - 4250) % 4], i, w, h)
                variance_box = self._parse_variance_box()
                encoded_box = self._parse_encoded_box(encoded_data, i)
                decoded_bbox = self._parse_decoded_bbox(prior_box, variance_box, encoded_box, orig_w, orig_h)
                detection = [detection_conf, decoded_bbox, action_conf, action_id]
                detections.append(detection)
            valid_detections = self._non_max_supression(detections, self._threshold)
            output_images.append(self._draw_detections(images, batch, valid_detections, action_map, orig_h, orig_w))
        self._save_output_images(output_images, log)


class person_detection_action_recognition_old(detection_ssd_old_format):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_action_map(self):
        action_map = ['sitting', 'standing', 'rasing hand']
        return action_map


class person_detection_raisinghand_recognition(detection_ssd_old_format):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_action_map(self):
        action_map = ['sitting', 'other']
        return action_map


class person_detection_action_recognition_teacher(detection_ssd_old_format):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_action_map(self):
        action_map = ['standing', 'writing', 'demonstrating']
        return action_map


class person_detection_action_recognition_new(detection_ssd_new_format):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_action_map(self):
        action_map = [
            'sitting',
            'writing',
            'raising_hand',
            'standing',
            'turned around',
            'lie on the desk'
        ]
        return action_map


class human_pose_estimation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def __create_pafs(self, fields):
        pafX = [fields[i] for i in range(0, fields.shape[0], 2)]
        pafY = [fields[i] for i in range(1, fields.shape[0], 2)]
        return pafX, pafY

    def __search_keypoints(self, keypoints_prob_map, frame_height, frame_width):
        keypoints = {}
        keypoint_id = 0
        for i in range(keypoints_prob_map.shape[0] - 1):
            prob_map = cv2.resize(keypoints_prob_map[i], (frame_height, frame_width))
            mapSmooth = cv2.GaussianBlur(prob_map, (3, 3), 0, 0)
            mapMask = np.uint8(mapSmooth > self._threshold)
            contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            keypoints[i] = []
            for cnt in contours:
                blobMask = np.zeros(mapMask.shape)
                blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                maskedProbMap = mapSmooth * blobMask
                _, _, _, (y, x) = cv2.minMaxLoc(maskedProbMap)
                keypoints[i].append({'coordinates': (x, y), 'id': keypoint_id})
                keypoint_id += 1
        return keypoints

    def __create_points(self, keypoints):
        points = []
        point_id = 0
        for part in range(len(keypoints)):
            if not (len(keypoints[part]) == 0):
                for point in keypoints[part]:
                    points.append({
                        'coordinates': point['coordinates'],
                        'part': part,
                        'id': point_id
                    })
                    point_id += 1
        return points

    def __search_connections(self, edges, keypoints, pafX, pafY, frame_width, frame_height):
        valid_connections = []
        invalid_connections = []
        for edge in edges:
            valid_pairs = []
            fieldX = cv2.resize(pafX[edges.index(edge)], (frame_width, frame_height))
            fieldY = cv2.resize(pafY[edges.index(edge)], (frame_width, frame_height))
            start_point_candidates = keypoints[edge['startVertex']]
            end_point_candidates = keypoints[edge['endVertex']]
            if (not (len(start_point_candidates) == 0) and not (len(end_point_candidates) == 0)):
                for start_point in start_point_candidates:
                    max_end_point_id = -1
                    max_score = -1
                    found = False
                    for end_point in end_point_candidates:
                        distance = np.subtract(end_point['coordinates'], start_point['coordinates'])
                        norm = np.linalg.norm(distance)
                        if norm:
                            norm_distance = distance/norm
                        else:
                            continue
                        interp_coord = list(
                            zip(
                                np.linspace(
                                    start_point['coordinates'][0],
                                    end_point['coordinates'][0],
                                    num=10
                                ),
                                np.linspace(
                                    start_point['coordinates'][1],
                                    end_point['coordinates'][1],
                                    num=10)
                            )
                        )
                        paf_interp = []
                        for coord in interp_coord:
                            x = int(round(coord[0]))
                            y = int(round(coord[1]))
                            paf_interp.append((fieldX[y, x], fieldY[y, x]))
                        paf_scores = np.dot(paf_interp, norm_distance)
                        avg_paf_score = sum(paf_scores)/len(paf_scores)
                        valid_points = np.where(paf_scores > self._threshold)[0]
                        if ((len(valid_points) / 10) > 0.7):
                            if avg_paf_score > max_score:
                                max_end_point_id = end_point['id']
                                max_score = avg_paf_score
                                found = True
                    if (found):
                        valid_pairs.append([start_point['id'], max_end_point_id])
                valid_connections.append(valid_pairs)
            else:
                valid_connections.append([])
                invalid_connections.append(edge)
        return valid_connections, invalid_connections

    def __search_persons_keypoints(self, edges, valid_connections, invalid_connections):
        persons_keypoints = -1 * np.ones((0, 18))
        for edge in edges:
            if edge not in invalid_connections:
                start_point = edge['startVertex']
                end_point = edge['endVertex']
                for connection in valid_connections[edges.index(edge)]:
                    found = False
                    person_index = -1
                    for person_index in range(len(persons_keypoints)):
                        if persons_keypoints[person_index][start_point] == connection[0]:
                            found = True
                            break
                    if found:
                        persons_keypoints[person_index][end_point] = connection[1]
                    elif not found and edges.index(edge) < 17:
                        new_person_points = -1 * np.ones(18)
                        new_person_points[start_point] = connection[0]
                        new_person_points[end_point] = connection[1]
                        persons_keypoints = np.vstack((persons_keypoints, new_person_points))
        return persons_keypoints

    def __print_edges(self, edges, persons_keypoints, points, frame, colors):
        for edge in edges:
            for person_points in persons_keypoints:
                start_point_id = int(person_points[edge['startVertex']])
                end_point_id = int(person_points[edge['endVertex']])
                connection = (start_point_id, end_point_id)
                if -1 in connection:
                    continue
                start_point = points[start_point_id]['coordinates']
                end_point = points[end_point_id]['coordinates']
                frame = cv2.line(frame, start_point, end_point, colors[edges.index(edge)], 2, cv2.LINE_AA)
        return frame

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        edges = [
            {'startVertex': 1, 'endVertex': 8},
            {'startVertex': 8, 'endVertex': 9},
            {'startVertex': 9, 'endVertex': 10},
            {'startVertex': 1, 'endVertex': 11},
            {'startVertex': 11, 'endVertex': 12},
            {'startVertex': 12, 'endVertex': 13},
            {'startVertex': 1, 'endVertex': 2},
            {'startVertex': 2, 'endVertex': 3},
            {'startVertex': 3, 'endVertex': 4},
            {'startVertex': 2, 'endVertex': 16},
            {'startVertex': 1, 'endVertex': 5},
            {'startVertex': 5, 'endVertex': 6},
            {'startVertex': 6, 'endVertex': 7},
            {'startVertex': 5, 'endVertex': 17},
            {'startVertex': 1, 'endVertex': 0},
            {'startVertex': 0, 'endVertex': 14},
            {'startVertex': 0, 'endVertex': 15},
            {'startVertex': 15, 'endVertex': 17},
            {'startVertex': 14, 'endVertex': 16},
        ]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_maps/pose_estimation_color_map.txt')
        colors = []
        with open(self._color_map, 'r') as f:
            for line in f:
                colors.append([int(x) for x in line.split()])
        shapes = self._original_shapes[next(iter(self._original_shapes))]
        for batch, frame in enumerate(self._input['data']):
            frame = frame.transpose((1, 2, 0))
            frame_height = frame.shape[0]
            frame_width = frame.shape[1]
            keypoints_prob_map = result['Mconv7_stage2_L2'][batch].transpose(0, 2, 1)
            fields = result['Mconv7_stage2_L1'][batch]
            pafX, pafY = self.__create_pafs(fields)
            keypoints = self.__search_keypoints(keypoints_prob_map, frame_height, frame_width)
            points = self.__create_points(keypoints)
            valid_connections, invalid_connections = self.__search_connections(
                edges,
                keypoints,
                pafX,
                pafY,
                frame_width,
                frame_height
            )
            persons_keypoints = self.__search_persons_keypoints(edges, valid_connections, invalid_connections)
            frame = self.__print_edges(edges, persons_keypoints, points, frame, colors)
            out_img = os.path.join(os.path.dirname(__file__), 'out_pose_estimation_{}.png'.format(batch + 1))
            orig_h, orig_w = shapes[batch % self._batch_size]
            frame = cv2.resize(frame, (orig_w, orig_h))
            cv2.imwrite(out_img, frame)
            log.info('Result image was saved to {}'.format(out_img))


class action_recognition_encoder_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        file_name = os.path.join(os.path.dirname(__file__), 'action_recognition_encoder_out.csv')
        batch_size, dim1 = result.shape[:2]
        with open(file_name, 'w+'):
            probs = np.reshape(np.squeeze(result), (batch_size, dim1))
            np.savetxt(
                'action_recognition_encoder_out.csv',
                probs,
                fmt='%1.7f',
                delimiter=';',
                header='{};{}'.format(batch_size, dim1),
                comments=''
            )
        log.info('Result was saved to {}'.format(file_name))


class driver_action_recognition_encoder_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        file_name = os.path.join(os.path.dirname(__file__), 'driver_action_recognition_encoder_out.csv')
        batch_size, dim1 = result.shape[:2]
        with open(file_name, 'w+'):
            probs = np.reshape(np.squeeze(result), (batch_size, dim1))
            np.savetxt(
                'driver_action_recognition_encoder_out.csv',
                probs,
                fmt='%1.7f',
                delimiter=';',
                header='{};{}'.format(batch_size, dim1),
                comments=''
            )
        log.info('Result was saved to {}'.format(file_name))


class reidentification_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        file_name = os.path.join(os.path.dirname(__file__), 'reidentification.csv')
        batch_size, dim1 = result.shape[:2]
        with open(file_name, 'w+'):
            probs = np.reshape(np.squeeze(result), (batch_size, dim1))
            np.savetxt(
                'reidentification.csv',
                probs,
                fmt='%1.7f',
                delimiter=';',
                header='{};{}'.format(batch_size, dim1),
                comments=''
            )
        log.info('Result was saved to {}'.format(file_name))


class action_recognition_decoder_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/kinetics.txt')
        with open(self._labels, 'r') as f:
            labels_map = [line.strip() for line in f]
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        for batch, data in enumerate(result):
            probs = np.squeeze(result)
            top_ind = np.argsort(probs)[-self._number_top:][::-1]
            log.info("\nResult:")
            for id in top_ind:
                det_label = labels_map[id] if labels_map else '#{}'.format(id)
                log.info('{:.7f} {}'.format(probs[id], det_label))


class driver_action_recognition_decoder_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/driver_action_labels.txt')
        with open(self._labels, 'r') as f:
            labels_map = [line.strip() for line in f]
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        for batch, data in enumerate(result):
            probs = np.squeeze(data)
            top_ind = np.argsort(probs)[::-1]
            log.info("\nResult:")
            for id in top_ind:
                det_label = labels_map[id] if labels_map else '#{}'.format(id)
                log.info('{:.7f} {}'.format(probs[id], det_label))


class mask_rcnn_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_maps/mscoco_color_map_90.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/mscoco_names_90.txt')
        labels_map = []
        with open(self._labels, 'r') as f:
            for line in f:
                labels_map.append(line.strip())

        shapes = self._original_shapes[next(iter(self._original_shapes))]
        image = self._input['image_tensor'][0].transpose((1, 2, 0))

        detections_info = result['reshape_do_2d']
        masks = result['masks']

        count_of_detected_objects = 0
        for i, detection_info in enumerate(detections_info):
            image_number = detection_info[0]
            if image_number == -1:
                count_of_detected_objects = i
                break
        masks = masks[:count_of_detected_objects]
        detections_info = detections_info[:count_of_detected_objects]

        labels_on_image = []

        for idx, detection_info in enumerate(detections_info):
            if detection_info[2] > self._threshold:
                initial_h, initial_w = image.shape[:2]
                left = int(detection_info[3] * initial_w)
                top = int(detection_info[4] * initial_h)
                right = int(detection_info[5] * initial_w)
                bottom = int(detection_info[6] * initial_h)

                class_id = int(detection_info[1]) - 1
                mask = masks[idx][class_id]
                color = classes_color_map[class_id]

                object_width = abs(right - left)
                object_height = abs(top - bottom)

                dw = int(object_width / mask.shape[-1])
                dh = int(object_height / mask.shape[-2])

                label_on_image_point = (int(left + object_width / 3), int(bottom - object_height / 2))
                label_on_image = '<' + labels_map[class_id] + '>'
                labels_on_image.append((label_on_image, label_on_image_point))

                for j in range(mask.shape[-2]):
                    for i in range(mask.shape[-1]):
                        if (mask[j][i] < self._threshold):
                            continue

                        x = int(left + i * dw)
                        y = int(top + j * dh)

                        for m in range(y, y + dh):
                            for n in range(x, x + dw):
                                image[m, n] = color

        for i in range(len(labels_on_image)):
            image = cv2.putText(cv2.UMat(image), labels_on_image[i][0], labels_on_image[i][1], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        orig_h, orig_w = shapes[0]
        image = cv2.UMat(cv2.resize(cv2.UMat(image), (orig_w, orig_h)))
        out_img = os.path.join(os.path.dirname(__file__), 'mask_rcnn_out.bmp')
        cv2.imwrite(out_img, image)
        log.info('Result image was saved to {}'.format(out_img))


class yolo(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _sigmoid(self, x) -> float:
        return 1 / (1 + np.exp(-x))

    def _softmax(self, x):
        e_x = np.exp(x)
        return e_x / e_x.sum(axis=0)

    @abc.abstractmethod
    def _get_anchors(self):
        pass

    @abc.abstractmethod
    def _get_shapes(self):
        pass

    def __non_max_supression(self, predictions, score_threshold, nms_threshold):
        predictions.sort(key=lambda prediction: prediction[0], reverse=True)
        valid_detections = []
        while (len(predictions) > 0):
            max_detection = predictions[0]
            if max_detection[0] < score_threshold:
                break
            valid_detections.append(max_detection)
            predictions.remove(max_detection)
            remove_detections = []
            for detection in predictions:
                if detection[0] < score_threshold:
                    remove_detections.append(detection)
                    continue
                if not (max_detection[1] == detection[1]):
                    continue
                current_rect_area = detection[2][2] * detection[2][3]
                max_rect_area = max_detection[2][2] * max_detection[2][3]
                intersection_area = 0
                if not (detection[2][2] <= 0 or detection[2][3] <= 0 or max_detection[2][2] <= 0 or max_detection[2][3] <= 0):
                    intersection_area = float(
                        (min(detection[2][0] + detection[2][2], max_detection[2][0] + max_detection[2][2]) -
                         max(detection[2][0], max_detection[2][0])) *
                        (min(detection[2][1] + detection[2][3], max_detection[2][1] + max_detection[2][3]) -
                         max(detection[2][1], max_detection[2][1]))
                    )
                overlap = intersection_area / (current_rect_area + max_rect_area - intersection_area)
                if (overlap > nms_threshold):
                    remove_detections.append(detection)
            for detection in remove_detections:
                predictions.remove(detection)
        return valid_detections

    def __print_detections(self, detections, labels_map, image, scales, orig_shape, batch, log):
        image = cv2.resize(image, orig_shape)
        for detection in detections:
            left = int(detection[2][0] * scales['W'])
            top = int(detection[2][1] * scales['H'])
            right = int((detection[2][2] + detection[2][0]) * scales['W'])
            bottom = int((detection[2][3] + detection[2][1]) * scales['H'])
            class_id = int(detection[1])
            color = (min(int(class_id / 25 % 5) * 50, 255), min(int(class_id / 5 % 5) * 50, 255), min(int(class_id % 5) * 50, 255))
            log.info('Bounding boxes for image {0} for object {1}'.format(batch, class_id))
            log.info('Top left: ({0}, {1})'.format(top, left))
            log.info('Bottom right: ({0}, {1})'.format(bottom, right))
            label = '<' + labels_map[class_id] + '>'
            image = cv2.rectangle(image, (left, top), (right, bottom), color, 3)
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 1)
            cv2.rectangle(image, (left - 2, top - 4 - base_line - label_size[1]), (left + label_size[0], top), color, -2)
            image = cv2.putText(image, label, (left, top - base_line - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
        return image

    def _get_cell_predictions(self, cx, cy, dx, dy, detection, anchor_box_number, frameHeight, frameWidth, anchors):
        tx, ty, tw, th, to = detection[0:5]
        bbox_center_x = (float(cx) + self._sigmoid(tx)) * (float(frameWidth) / dx)
        bbox_center_y = (float(cy) + self._sigmoid(ty)) * (float(frameHeight) / dy)
        prior_width, prior_height = anchors[anchor_box_number]
        bbox_width = (np.exp(tw) * prior_width) * (float(frameWidth) / dx)
        bbox_height = (np.exp(th) * prior_height) * (float(frameHeight) / dy)
        confidence = self._sigmoid(to)
        scores = detection[5:]
        class_id = np.argmax(self._softmax(scores))
        best_class_score = scores[class_id]
        confidence_in_class = confidence * best_class_score
        if (confidence_in_class > self._threshold):
            bbox = [
                float(bbox_center_x - bbox_width / 2),
                float(bbox_center_y - bbox_height / 2),
                float(bbox_width),
                float(bbox_height)
            ]
            prediction = [[best_class_score, class_id, bbox]]
            return prediction
        return None

    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'labels/pascal_voc.txt')
        with open(self._labels, 'r') as f:
            labels_map = [line.strip() for line in f]
        anchors = self._get_anchors()
        shapes = self._get_shapes()
        input_layer_name = next(iter(self._input))
        input = self._input[input_layer_name]
        frameHeight, frameWidth = input.shape[-2:]
        result = list(result.values())
        ib, c, h, w = input.shape
        b = result[0].shape[0]
        images = np.ndarray(shape=(b, h, w, c))
        for i in range(b):
            images[i] = input[i % ib].transpose((1, 2, 0))
        for batch in range(ib):
            image = images[batch]
            predictions = []
            orig_h, orig_w = self._original_shapes[next(iter(self._original_shapes))][batch]
            scales = {'W': orig_w / frameWidth, 'H': orig_h / frameHeight}
            for i, array_of_detections in enumerate(result):
                anchors_boxes = anchors[i]
                data = array_of_detections[batch]
                data_shape = shapes[i]
                dx, dy = data_shape[-2:]
                cells = data.reshape(data_shape).transpose((2, 3, 0, 1))
                for cx in range(dy):
                    for cy in range(dx):
                        for anchor_box_number, detection in enumerate(cells[cy, cx]):
                            if (detection[4] >= 0.5):
                                prediction = self._get_cell_predictions(cx, cy, dx, dy, detection, anchor_box_number,
                                                                        frameHeight, frameWidth, anchors_boxes)
                                if prediction is not None:
                                    predictions += prediction
            valid_detections = self.__non_max_supression(predictions, self._threshold, 0.4)
            image = self.__print_detections(valid_detections, labels_map, cv2.UMat(image), scales, (orig_w, orig_h), batch, log)
            out_img = os.path.join(os.path.dirname(__file__), 'out_yolo_detection_{}.bmp'.format(batch + 1))
            cv2.imwrite(out_img, image)
            log.info('Result image was saved to {}'.format(out_img))


class yolo_v2_voc_io(yolo):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_shapes(self):
        shapes = [
            (5, 25, 13, 13)
        ]
        return shapes

    def _get_anchors(self):
        anchors = [
            ((1.3221,  1.73145), (3.19275, 4.00944), (5.05587, 8.09892), (9.47112, 4.84053), (11.2364, 10.0071))
        ]
        return anchors


class yolo_tiny_voc_io(yolo):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_shapes(self):
        shapes = [
            (5, 25, 13, 13)
        ]
        return shapes

    def _get_anchors(self):
        anchors = [
            ((1.08, 1.19), (3.42, 4.41), (6.63, 11.38), (9.42, 5.11), (16.62, 10.52))
        ]
        return anchors


class yolo_v2_coco_io(yolo):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_shapes(self):
        shapes = [
            (5, 85, 19, 19)
        ]
        return shapes

    def _get_anchors(self):
        anchors = [
            ((0.57273, 0.677385), (1.87446, 2.06253), (3.33843, 5.47434), (7.88282, 3.52778), (9.77052, 9.16828))
        ]
        return anchors


class yolo_v2_tiny_coco_io(yolo_v2_coco_io):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_shapes(self):
        shapes = [
            (5, 85, 13, 13)
        ]
        return shapes


class yolo_v3_io(yolo):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)

    def _get_cell_predictions(self, cx, cy, dx, dy, detection, anchor_box_number, frameHeight, frameWidth, anchors):
        predictions = []
        tx, ty, tw, th = detection[0:4]
        prior_width, prior_height = anchors[anchor_box_number]
        bbox_center_x = (float(cx) + tx) * (float(frameHeight) / dx)
        bbox_center_y = (float(cy) + ty) * (float(frameWidth) / dy)
        bbox_width = np.exp(tw) * prior_width
        bbox_height = np.exp(th) * prior_height
        for class_id in range(80):
            confidence = detection[5 + class_id]
            if confidence >= self._threshold:
                bbox = [
                    float(bbox_center_x - bbox_width / 2),
                    float(bbox_center_y - bbox_height / 2),
                    float(bbox_width),
                    float(bbox_height)
                ]
                prediction = [confidence, class_id, bbox]
                predictions.append(prediction)
        return predictions

    def _get_shapes(self):
        shapes = [
            (3, 85, 13, 13),
            (3, 85, 26, 26),
            (3, 85, 52, 52)
        ]
        return shapes

    def _get_anchors(self):
        anchors = [
            ((116, 90), (156, 198), (373, 326)),
            ((30, 61), (62, 45), (59, 119)),
            ((10, 13), (16, 30), (33, 23))
        ]
        return anchors
