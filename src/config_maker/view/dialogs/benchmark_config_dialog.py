import abc

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox
# pylint: disable-next=E0401
from tags import CONFIG_MODEL_TAG, CONFIG_DATASET_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_BATCH_SIZE_TAG, CONFIG_DEVICE_TAG, \
    CONFIG_ITERATION_COUNT_TAG, CONFIG_TEST_TIME_LIMIT_TAG, CONFIG_MODE_TAG, CONFIG_EXTENSION_TAG, \
    CONFIG_ASYNC_REQ_COUNT_TAG, CONFIG_THREAD_COUNT_TAG, CONFIG_STREAM_COUNT_TAG, CONFIG_CHANNEL_SWAP_TAG, \
    CONFIG_MEAN_TAG, CONFIG_INPUT_SCALE_TAG, CONFIG_INPUT_SHAPE_TAG, CONFIG_INPUT_NAME_TAG, CONFIG_OUTPUT_NAMES_TAG, \
    CONFIG_KMP_AFFINITY_TAG, CONFIG_INTER_OP_THREADS_TAG, CONFIG_INTRA_OP_THREADS_TAG


class BenchmarkConfigDialog(QDialog):
    def __init__(self, parent, models, data):
        super().__init__(parent)
        self.__framework_dependent_parameters = {'OpenVINO DLDT': OpenVINODialog(self), 'Caffe': CaffeDialog(self),
                                                 'TensorFlow': TensorFlowDialog(self)}
        self.__framework_independent_parameters = IndependentParameters(self, models, data,
                                                                        self.__framework_dependent_parameters.keys(),
                                                                        self.__framework_choice)
        self.__selected_framework = 'OpenVINO DLDT'
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about test')
        self.__create_layout()

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        idx = self.__framework_independent_parameters.attach_to_layout(layout, idx)
        dict_framework_idx = dict.fromkeys(self.__framework_dependent_parameters.keys(), idx)
        for key in self.__framework_dependent_parameters:
            dict_framework_idx[key] = self.__framework_dependent_parameters[key].attach_to_layout(layout, idx, False)
        self.__framework_dependent_parameters['OpenVINO DLDT'].show()
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)  # pylint: disable=E1120
        cancel_btn.clicked.connect(self.reject)  # pylint: disable=E1120
        layout.addWidget(ok_btn, max(*dict_framework_idx.values()), 0)
        layout.addWidget(cancel_btn, max(*dict_framework_idx.values()), 1)
        self.setLayout(layout)

    def __framework_choice(self, framework):
        for key in self.__framework_dependent_parameters:
            if key == framework:
                self.__framework_dependent_parameters[key].show()
                self.__selected_framework = key
            else:
                self.__framework_dependent_parameters[key].hide()

    def get_values(self):
        return [*self.__framework_independent_parameters.get_values(),
                *self.__framework_dependent_parameters[self.__selected_framework].get_values()]

    def load_values_from_table_row(self, table, row):
        self.__framework_independent_parameters.load_values_from_table_row(table, row)
        self.__framework_dependent_parameters[self.__selected_framework].load_values_from_table_row(table, row)

    def accept(self):
        is_ok = self.__framework_independent_parameters.check()
        is_ok = is_ok and self.__framework_dependent_parameters[self.__selected_framework].check()
        if is_ok:
            super().accept()
        else:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')


class ParametersDialog(metaclass=abc.ABCMeta):
    def __init__(self, parent, tags):
        self._parent = parent
        self._tags = tags
        self._labels = []
        self._edits = []
        self.__init_ui()

    def __init_ui(self):
        self.__create_labels()
        self._create_edits()

    def __create_labels(self):
        self._labels = dict.fromkeys(self._tags)
        for key in self._labels:
            self._labels[key] = QLabel(key, self._parent)
        self._labels[self._tags[0]].setStyleSheet("font-weight: bold")

    @abc.abstractmethod
    def _create_edits(self):
        pass

    @abc.abstractmethod
    def get_values(self):
        pass

    @abc.abstractmethod
    def load_values_from_table_row(self, table, row):
        pass

    def hide(self):
        self._labels[self._tags[0]].hide()
        for tag in self._tags[1:]:
            self._labels[tag].hide()
            self._edits[tag].hide()

    def show(self):
        self._labels[self._tags[0]].show()
        for tag in self._tags[1:]:
            self._labels[tag].show()
            self._edits[tag].show()

    def attach_to_layout(self, layout, idx, show=True):
        layout.addWidget(self._labels[self._tags[0]], idx, 0)
        self_idx = idx + 1
        for tag in self._tags[1:]:
            layout.addWidget(self._labels[tag], self_idx, 0)
            layout.addWidget(self._edits[tag], self_idx, 1)
            self_idx += 1
        if show:
            self.show()
        else:
            self.hide()
        return self_idx


class IndependentParameters(ParametersDialog):
    def __init__(self, parent, models, data, frameworks, framework_choice):
        self.__models = models
        self.__data = data
        self.__frameworks = frameworks
        self.__framework_choice = framework_choice
        super().__init__(parent, ['FrameworkIndependent:', CONFIG_MODEL_TAG, CONFIG_DATASET_TAG, CONFIG_FRAMEWORK_TAG,
                                  CONFIG_BATCH_SIZE_TAG, CONFIG_DEVICE_TAG, CONFIG_ITERATION_COUNT_TAG,
                                  CONFIG_TEST_TIME_LIMIT_TAG])

    def _create_edits(self):
        self._edits = dict.fromkeys(self._tags[1:])
        self._edits[CONFIG_MODEL_TAG] = QComboBox(self._parent)
        self._edits[CONFIG_MODEL_TAG].addItems(self.__models)
        self._edits[CONFIG_DATASET_TAG] = QComboBox(self._parent)
        self._edits[CONFIG_DATASET_TAG].addItems(self.__data)
        self._edits[CONFIG_FRAMEWORK_TAG] = QComboBox(self._parent)
        self._edits[CONFIG_FRAMEWORK_TAG].addItems(self.__frameworks)
        self._edits[CONFIG_FRAMEWORK_TAG].activated[str].connect(self.__framework_choice)
        self._edits[CONFIG_FRAMEWORK_TAG].currentTextChanged[str].connect(self.__framework_choice)
        self._edits[CONFIG_DEVICE_TAG] = QComboBox(self._parent)
        self._edits[CONFIG_DEVICE_TAG].addItems(('CPU', 'GPU', 'MYRIAD', 'CPU;GPU', 'CPU;MYRIAD', 'GPU;MYRIAD',
                                                 'CPU;GPU;MYRIAD'))
        for tag in self._tags[4:]:
            if tag != CONFIG_DEVICE_TAG:
                self._edits[tag] = QLineEdit(self._parent)

    def get_values(self):
        values = []
        values.append(self._edits[CONFIG_MODEL_TAG].currentText())
        values.append(self._edits[CONFIG_DATASET_TAG].currentText())
        values.append(self._edits[CONFIG_FRAMEWORK_TAG].currentText())
        for tag in self._tags[4:]:
            if tag != CONFIG_DEVICE_TAG:
                values.append(self._edits[tag].text())
            else:
                values.append(self._edits[tag].currentText())
        return values

    def load_values_from_table_row(self, table, row):
        self._edits[CONFIG_MODEL_TAG].setCurrentText(table.item(row, 0).text())
        self._edits[CONFIG_DATASET_TAG].setCurrentText(table.item(row, 1).text())
        self._edits[CONFIG_FRAMEWORK_TAG].setCurrentText(table.item(row, 2).text())
        self._edits[CONFIG_DEVICE_TAG].setCurrentText(table.item(row, 4).text())
        idx = 3
        for tag in self._tags[4:]:
            if tag != CONFIG_DEVICE_TAG:
                self._edits[tag].setText(table.item(row, idx).text())
            idx += 1

    def check(self):
        for tag in self._tags[4:]:
            if tag != CONFIG_DEVICE_TAG and self._edits[tag].text() == '':
                return False
        return True


class DependentParameters(ParametersDialog):
    def __init__(self, parent, tags):
        super().__init__(parent, tags)

    def _create_edits(self):
        self._edits = dict.fromkeys(self._tags[1:])
        for key in self._edits:
            self._edits[key] = QLineEdit(self._parent)

    def get_values(self):
        values = []
        for tag in self._tags[1:]:
            values.append(self._edits[tag].text())
        return values

    def load_values_from_table_row(self, table, row):
        for tag in self._tags[1:]:
            self._edits[tag].setText(table.item(row, table.headers.index(tag)).text())

    def check(self):
        return True


class OpenVINODialog(DependentParameters):
    def __init__(self, parent):
        super().__init__(parent,
                         ['OpenVINO DLDT:', CONFIG_MODE_TAG, CONFIG_EXTENSION_TAG, CONFIG_ASYNC_REQ_COUNT_TAG,
                          CONFIG_THREAD_COUNT_TAG, CONFIG_STREAM_COUNT_TAG])

    def check(self):
        if self._edits[CONFIG_MODE_TAG].text() == '':
            return False
        return True


class CaffeDialog(DependentParameters):
    def __init__(self, parent):
        super().__init__(parent,
                         ['Caffe:', CONFIG_CHANNEL_SWAP_TAG, CONFIG_MEAN_TAG, CONFIG_INPUT_SCALE_TAG,
                          CONFIG_THREAD_COUNT_TAG, CONFIG_KMP_AFFINITY_TAG])


class TensorFlowDialog(DependentParameters):
    def __init__(self, parent):
        super().__init__(parent,
                         ['TensorFlow:', CONFIG_CHANNEL_SWAP_TAG, CONFIG_MEAN_TAG, CONFIG_INPUT_SCALE_TAG,
                          CONFIG_INPUT_SHAPE_TAG, CONFIG_INPUT_NAME_TAG, CONFIG_OUTPUT_NAMES_TAG,
                          CONFIG_THREAD_COUNT_TAG, CONFIG_INTER_OP_THREADS_TAG, CONFIG_INTRA_OP_THREADS_TAG,
                          CONFIG_KMP_AFFINITY_TAG])
