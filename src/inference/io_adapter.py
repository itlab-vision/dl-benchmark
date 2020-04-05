import os
import abc
import cv2
import numpy as np
from transformer import transformer


class io_adapter(metaclass = abc.ABCMeta):
    def __init__(self, args, io_model_wrapper, transformer):
        self._input = None
        self._batch_size = args.batch_size
        self._labels = args.labels
        self._number_top = args.number_top
        self._threshold = args.threshold
        self._color_map = args.color_map
        self._io_model_wrapper = io_model_wrapper
        self._transformer = transformer


    def __convert_images(self, shape, data):
        c, h, w  = shape[1:]
        images = np.ndarray(shape = (len(data), c, h, w))
        for i in range(len(data)):
            image = cv2.imread(data[i])
            if (image.shape[:-1] != (h, w)):
                image = cv2.resize(image, (w, h))
            image = image.transpose((2, 0, 1))
            images[i] = self._transformer.transform(image)
        return images


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
        result = np.array(value, dtype = np.float32)
        result = result.reshape(shape)
        return result


    def prepare_input(self, model, input):
        self._input = {}
        if ':' in input[0]:
            for str in input:
                key, value = str.split(':')
                file_format = value.split('.')[-1]
                if 'csv' == file_format:
                    value = self.__parse_tensors(value)
                else:
                    value = value.split(',')
                    value = self.__create_list_images(value)
                    shape = self._io_model_wrapper.get_input_layer_shape(model, key)
                    value = self.__convert_images(shape, value)
                self._input.update({key : value})
        else:
            input_blob = shape = self._io_model_wrapper.get_input_layer_names(model)[0]
            file_format = input[0].split('.')[-1]
            if 'csv' == file_format:
                value = self.__parse_tensors(input[0])
            else:
                value = self.__create_list_images(input)
                shape = self._io_model_wrapper.get_input_layer_shape(model, input_blob)
                value = self.__convert_images(shape, value)
            self._input.update({input_blob : value})
        return self._input


    def get_slice_input(self, iteration):
        slice_input = dict.fromkeys(self._input.keys(), None)
        for key in self._input:
            slice_input[key] = self._input[key][(iteration * self._batch_size)
                % len(self._input[key]) : (((iteration + 1) * self._batch_size - 1)
                % len(self._input[key])) + 1:]
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
        elif task == 'human-pose-estimation':
            return human_pose_estimation_io(args, io_model_wrapper, transformer)


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
            self._labels = os.path.join(os.path.dirname(__file__), 'image_net_synset.txt')
        with open(self._labels, 'r') as f:
            labels_map = [ x.split(sep = ' ', maxsplit = 1)[-1].strip() for x in f ]
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
        ib, c, h, w = input.shape
        b = result.shape[0]
        images = np.ndarray(shape = (b, h, w, c))
        for i in range(b):
            images[i] = input[i % ib].transpose((1, 2, 0))
        for batch in range(b):
            for obj in result[batch][0]:
                if obj[2] > self._threshold:
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
                    log.info('Bounding boxes for image {0} for object {1}'.format(image_number, class_id))
                    log.info('Top left: ({0}, {1})'.format(xmin, ymin))
                    log.info('Bottom right: ({0}, {1})'.format(xmax, ymax))
        count = 0
        for image in images:
            out_img = os.path.join(os.path.dirname(__file__), 'out_detection_{}.bmp'.format(count + 1))
            count += 1
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
        c = 3
        h, w = result.shape[1:]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_map.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
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


class adas_segmenatation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)


    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        c = 3
        h, w = result.shape[1:]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_map.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        for batch, data in enumerate(result):
            data = np.squeeze(data)
            classes_map = np.zeros(shape = (h, w, c), dtype = np.int)
            for i in range(h):
                for j in range(w):
                    pixel_class = int(data[i, j])
                    classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)]
            out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch + 1))
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
        c = 3
        h, w = result.shape[1:]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'color_map_road_segmentation.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        for batch, data in enumerate(result):
            data = data.transpose((1, 2, 0))
            classes_map = np.zeros(shape = (h, w, c), dtype = np.int)
            for i in range(h):
                for j in range(w):
                    pixel_class = np.argmax(data[i][j])
                    classes_map[i, j, :] = classes_color_map[pixel_class]
            out_img = os.path.join(os.path.dirname(__file__), 'out_segmentation_{}.bmp'.format(batch + 1))
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
        images = np.ndarray(shape = (b, h, w, c))
        for i in range(b):
            images[i] = input[i % ib].transpose((1, 2, 0))
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
        images = np.ndarray(shape = (b, h, w * 4, c))
        attributes = ['is_male', 'has_bag', 'has_backpack', 'has_hat', 'has_longsleeves',
            'has_longpants', 'has_longhair', 'has_coat_jacket']
        color_point = (0, 0, 255)
        for i in range(b):
            for x in range(w):
                for y in range(h):
                    images[i][y][x] = input[i % ib].transpose((1, 2, 0))[y][x]
            x_top = int(result_top[i][0] * w)
            y_top = int(result_top[i][1] * h)
            x_bottom = int(result_bottom[i][0] * w)
            y_bottom = int(result_bottom[i][1] * h)
            color_top = (int(images[i][y_top][x_top][0]), int(images[i][y_top][x_top][1]),
                int(images[i][y_top][x_top][2]))
            color_bottom = (int(images[i][y_bottom][x_bottom][0]), int(images[i][y_bottom][x_bottom][1]),
                int(images[i][y_bottom][x_bottom][2]))
            cv2.circle(images[i], (x_top, y_top), 3, color_point, -1)
            cv2.circle(images[i], (x_bottom, y_bottom), 3, color_point, -1)  
            for x in range(w, 2 * w):
                for y in range(0, int(h / 2)):
                    images[i][y][x] = color_top
                    images[i][y + int(h / 2)][x] = color_bottom
            for j, val in enumerate(result_attributes[i]):
                color_attribut = (0, 255 * bool(val > 0.5), 255 * bool(val <= 0.5))
                cv2.putText(images[i], '{0} {1}'.format(attributes[j], bool(val > 0.5)), 
                    (w * 2 + 5, 20 + j * 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color_attribut)
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
        images = np.ndarray(shape = (b, h, w * 2, c))
        images_left_eye = np.ndarray(shape = (b, h, w, c))
        images_right_eye = np.ndarray(shape = (b, h, w, c))
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
        images = np.ndarray(shape = (b, h, w, c))
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
            Rx = np.array([[1, 0, 0], 
                        [0, np.cos(pitch), -np.sin(pitch)],
                        [0, np.sin(pitch), np.cos(pitch)]])
            Ry = np.array([[np.cos(yaw), 0, -np.sin(yaw)], 
                        [0, 1, 0],
                        [np.sin(yaw), 0, np.cos(yaw)]])
            Rz = np.array([[np.cos(roll), -np.sin(roll), 0],
                        [np.sin(roll), np.cos(roll), 0], 
                        [0, 0, 1]])
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
        images = np.ndarray(shape = (1, h, w, c))
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
        slice_input['data'] = self._input['data'][(iteration * self._batch_size)
                % len(self._input['data']) : (((iteration + 1) * self._batch_size - 1)
                % len(self._input['data'])) + 1:]
        slice_input['seq_ind'] = self._input['seq_ind'][(iteration * 88 * self._batch_size)
                % len(self._input['seq_ind']) : (((iteration + 1) * 88 * self._batch_size - 1)
                % len(self._input['seq_ind'])) + 1:]
        return slice_input


    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        result = result[next(iter(result))]
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
        lexis = []
        with open(self._labels, 'r') as f:
            for line in f:
                lexis.append([str(x) for x in line.split()])
        for lex in result:
            s = ''
            for j in range(lex.shape[0]):
                if (lex[j] == -1):
                    break
                s = s + str(lexis[int(lex[j])][1])
            log.info('Plate: {}'.format(s))


class instance_segmenatation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)


    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'mscoco_color_map.txt')
        classes_color_map = []
        with open(self._color_map, 'r') as f:
            for line in f:
                classes_color_map.append([int(x) for x in line.split()])
        if not self._labels:
            self._labels = os.path.join(os.path.dirname(__file__), 'mscoco_names.txt')
        labels_map = []
        labels_map.append('background')
        with open(self._labels, 'r') as f:
            for x in f:
                labels_map.append(x.split(sep = ' ', maxsplit = 1)[-1].strip())
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
                                    image[y + c][x + t] += classes_color_map[classes[i]]
        for l in range(len(labels_on_image)):
            image = cv2.putText(image, labels_on_image[l][0], labels_on_image[l][1], \
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        out_img = os.path.join(os.path.dirname(__file__), 'instance_segmentation_out.bmp')
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
            classes_map = np.zeros(shape = (h, w, c), dtype = np.int)
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
            np.savetxt('sphereface_out.csv', result, fmt = '%1.2f', delimiter = ';', 
                        header = '{};{}'.format(result.shape[0], result.shape[1]), comments = '')
        log.info('Result was saved to {}'.format(file_name))


class human_pose_estimation_io(io_adapter):
    def __init__(self, args, io_model_wrapper, transformer):
        super().__init__(args, io_model_wrapper, transformer)


    def process_output(self, result, log):
        if (self._not_valid_result(result)):
            log.warning('Model output is processed only for the number iteration = 1')
            return
        edges = [
            {'startVertex' : 1, 'endVertex': 8},
            {'startVertex' : 8, 'endVertex': 9},
            {'startVertex' : 9, 'endVertex': 10},
            {'startVertex' : 1, 'endVertex': 11},
            {'startVertex' : 11, 'endVertex': 12},
            {'startVertex' : 12, 'endVertex': 13},
            {'startVertex' : 1, 'endVertex': 2},
            {'startVertex' : 2, 'endVertex': 3},
            {'startVertex' : 3, 'endVertex': 4},
            {'startVertex' : 2, 'endVertex': 16}, #connect right ear and right shoulder
            {'startVertex' : 1, 'endVertex': 5},
            {'startVertex' : 5, 'endVertex': 6},
            {'startVertex' : 6, 'endVertex': 7},
            {'startVertex' : 5, 'endVertex': 17}, #connect left ear and left shoulder
            {'startVertex' : 1, 'endVertex': 0},
            {'startVertex' : 0, 'endVertex': 14},
            {'startVertex' : 0, 'endVertex': 15},
            {'startVertex' : 15, 'endVertex': 17},
            {'startVertex' : 14, 'endVertex': 16},
        ]
        if not self._color_map:
            self._color_map = os.path.join(os.path.dirname(__file__), 'pose_estimation_color_map.txt')
        colors = []
        with open(self._color_map, 'r') as f:
            for line in f:
                colors.append([int(x) for x in line.split()])
        for batch, fields in enumerate(result['Mconv7_stage2_L1']):
            frame = self._input['data'][batch].transpose((1, 2, 0))
            frame_height = frame.shape[0]
            frame_width = frame.shape[1]
            keypoints_prob_map = result['Mconv7_stage2_L2'][batch].transpose(0, 2, 1)
            W = keypoints_prob_map.shape[1]
            H = keypoints_prob_map.shape[2]

# create_pafs:
            pafX = [fields[i] for i in range(0, fields.shape[0], 2)]
            pafY = [fields[i] for i in range(1, fields.shape[0], 2)]

# search_keypoints:
            keypoints = {}
            keypoint_id = 0
            for i in range(keypoints_prob_map.shape[0] - 1):
                prob_map = cv2.resize(keypoints_prob_map[i], (frame_height, frame_width))
                mapSmooth = cv2.GaussianBlur(prob_map, (3,3), 0, 0)
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

# create_points:
            points = []
            point_id = 0
            for part in range(len(keypoints)):
                if not (len(keypoints[part]) == 0):
                    for point in keypoints[part]:
                        points.append({'coordinates': point['coordinates'], 
                                       'part': part, 
                                       'id': point_id})
                        point_id += 1

# search_valid_connections:
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
                            interp_coord = list(zip(np.linspace(start_point['coordinates'][0], end_point['coordinates'][0], num=10),\
                                                    np.linspace(start_point['coordinates'][1], end_point['coordinates'][1], num=10)))
                            paf_interp = []
                            for coord in interp_coord:
                                x = int(round(coord[0]))
                                y = int(round(coord[1]))
                                paf_interp.append((fieldX[y, x], fieldY[y, x]))
                            paf_scores = np.dot(paf_interp, norm_distance)
                            avg_paf_score = sum(paf_scores)/len(paf_scores)
                            valid_points = np.where(paf_scores > self._threshold)[0]
                            if ((len(valid_points) / 10) > 0.7):   # if (valid points is 70%):
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

#search_persons_keypoints:
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

# print_edges:
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
            out_img = os.path.join(os.path.dirname(__file__), 'out_pose_estimation_{}.png'.format(batch + 1))
            cv2.imwrite(out_img, frame)
            log.info('Result image was saved to {}'.format(out_img))
