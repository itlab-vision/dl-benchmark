import abc
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QComboBox
# from config_maker.tags import CONFIG_MODEL_NAME_TAG, CONFIG_WEIGHTS_TAG
# from tags import CONFIG_CONFIG_TAG, CONFIG_QUANTIZATION_METHOD_TAG, CONFIG_NAME_TAG, \
#     CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_PRESET_TAG, CONFIG_AC_CONFIG_TAG, \
#     CONFIG_MAX_DROP_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG, \
#     CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG
from tags import CONFIG_CONFIG_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG, \
    CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG, HEADER_AAQ_PARAMS_TAGS, HEADER_DQ_PARAMS_TAGS, HEADER_INDEPENDENT_PARAMS_TAGS, HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS
from tags import CONFIG_MODEL_NAME_TAG, CONFIG_MODEL_TAG, CONFIG_WEIGHTS_TAG
from tags import HEADER_POT_PARAMS_TAGS, HEADER_MODEL_PARAMS_MODEL_TAGS, HEADER_MODEL_PARAMS_ENGINE_TAGS


class QuantizationConfigDialog(QDialog):
    def __init__(self, parent, models, data):
        super().__init__(parent)
        self.__title = 'Information about model'
        self.__q_method_dependent_params = {
            'DefaultQuantization': DefaultQuantizationDialog(self),
            'AccuracyAwareQuantization': AccuracyAwareQuantizationDialog(self)
        }
        self.__q_method_independent_params = IndependentParameters(
            self, models, data, self.__q_method_dependent_params.keys(), self.__q_method_choice)
        self.__selected_q_method = 'DefaultQuantization'
        self.__pot_params_tags = HEADER_POT_PARAMS_TAGS
        self.__model_params_tags = HEADER_MODEL_PARAMS_MODEL_TAGS + \
            HEADER_MODEL_PARAMS_ENGINE_TAGS + HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS + []
        self.tags = [*self.__pot_params_tags, *self.__model_params_tags]
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle(self.__title)
        self.__create_layout()

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        idx = self.__q_method_independent_params.attach_to_layout(layout, idx)
        dict_q_method_idx = dict.fromkeys(self.__q_method_dependent_params.keys(), idx)
        for key in self.__q_method_dependent_params:
            dict_q_method_idx[key] = self.__q_method_dependent_params[key].attach_to_layout(layout, idx, False)
        self.__q_method_dependent_params['DefaultQuantization'].show()
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, max(*dict_q_method_idx.values()), 0)
        layout.addWidget(cancel_btn, max(*dict_q_method_idx.values()), 1)
        self.setLayout(layout)

    def __q_method_choice(self, q_method):
        for key in self.__q_method_dependent_params:
            if key == q_method:
                self.__q_method_dependent_params[key].show()
                self.__selected_q_method = key
            else:
                self.__q_method_dependent_params[key].hide()

    def get_values(self):
        return self.__q_method_independent_params.get_values(), \
            self.__q_method_dependent_params[self.__selected_q_method].get_values()
        # return [*self.__q_method_independent_params.get_values(),
        #         *self.__q_method_dependent_params[self.__selected_q_method].get_values()]

    def load_values_from_table_row(self, table, row):
        self.__q_method_independent_params.load_values_from_table_row(table, row)
        self.__q_method_dependent_params[self.__selected_q_method].load_values_from_table_row(table, row)

    def accept(self):
        is_ok = self.__q_method_independent_params.check()
        is_ok = is_ok and self.__q_method_dependent_params[self.__selected_q_method].check()
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
        self._labels = {}
        for id, tag in enumerate(self._tags):
            self._labels[id] = QLabel(tag, self._parent)
        self._labels[0].setStyleSheet("font-weight: bold")
        '''
        self._labels = dict.fromkeys(self._tags)
        for key in self._labels:
            self._labels[key] = QLabel(key, self._parent)
        self._labels[self._tags[0]].setStyleSheet("font-weight: bold")
        '''

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
        self._labels[0].hide()
        for id, tag in enumerate(self._tags[1:]):
            self._labels[id].hide()
            self._edits[id].hide()
        '''
        self._labels[self._tags[0]].hide()
        for tag in self._tags[1:]:
            self._labels[tag].hide()
            self._edits[tag].hide()
        '''

    def show(self):
        self._labels[0].show()
        for id, tag in enumerate(self._tags[1:]):
            self._labels[id].show()
            self._edits[id].show()
        '''
        self._labels[self._tags[0]].show()
        for tag in self._tags[1:]:
            self._labels[tag].show()
            self._edits[tag].show()
        '''

    def attach_to_layout(self, layout, idx, show=True):
        # layout.addWidget(self._labels[self._tags[0]], idx, 0)
        layout.addWidget(self._labels[0], idx, 0)
        self_idx = idx + 1
        for id, tag in enumerate(self._tags[1:5]):
            layout.addWidget(self._labels[id], self_idx, 0)
            layout.addWidget(self._edits[id], self_idx, 1)
            self_idx += 1
        self_idx_2 = idx + 1
        for id, tag in enumerate(self._tags[5:-1]):
            layout.addWidget(self._labels[id], self_idx_2, 2)
            layout.addWidget(self._edits[id], self_idx_2, 3)
            self_idx_2 += 1
        '''
        for tag in self._tags[1:]:
            layout.addWidget(self._labels[tag], self_idx, 0)
            layout.addWidget(self._edits[tag], self_idx, 1)
            self_idx += 1
        '''
        if show:
            self.show()
        else:
            self.hide()
        return max(self_idx_2, self_idx)


class IndependentParameters(ParametersDialog):
    def __init__(self, parent, models, data, q_methods, q_method_choice):
        self.__models = models
        self.__data = data
        self.__q_methods = q_methods
        self.__q_method_choice = q_method_choice
        super().__init__(parent, ['QuantizationMethodIndependent:', *HEADER_INDEPENDENT_PARAMS_TAGS])

    def _create_edits(self):
        self._edits = {}

        self.__ignored_idx = []
        q_methods_idx = len(HEADER_POT_PARAMS_TAGS + HEADER_MODEL_PARAMS_MODEL_TAGS + \
            HEADER_MODEL_PARAMS_ENGINE_TAGS) + 1
        self._edits[q_methods_idx] = QComboBox(self._parent)
        self._edits[q_methods_idx].addItems(self.__q_methods)
        self._edits[q_methods_idx].activated[str].connect(self.__q_method_choice)
        self._edits[q_methods_idx].currentTextChanged[str].connect(self.__q_method_choice)
        self.__ignored_idx.append(q_methods_idx)

        for id, tag in enumerate(self._tags[1:]):
            if id not in self.__ignored_idx:
                self._edits[id] = QLineEdit(self._parent)
        '''
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
        '''

    def get_values(self):
        pot_values = []
        for id, tag in enumerate(self._tags[1:len(HEADER_POT_PARAMS_TAGS)]):
            if id not in self.__ignored_idx:
                pot_values.append(self._edits[id].text())
            else:
                pot_values.append(self._edits[id].currentText())
        model_values = []
        for id, tag in enumerate(self._tags[len(HEADER_POT_PARAMS_TAGS):]):
            if id not in self.__ignored_idx:
                model_values.append(self._edits[id].text())
            else:
                model_values.append(self._edits[id].currentText())
        return pot_values, model_values
        '''
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
        '''

    def load_values_from_table_row(self, table, row):
        for id, tag in enumerate(self._tags[1:]):
            if id not in self.__ignored_idx:
                self._edits[id].setText(table.item(row, id).text())
            else:
                self._edits[id].setCurrentText(table.item(row, id).text())
        '''
        self._edits[CONFIG_MODEL_TAG].setCurrentText(table.item(row, 0).text())
        self._edits[CONFIG_DATASET_TAG].setCurrentText(table.item(row, 1).text())
        self._edits[CONFIG_FRAMEWORK_TAG].setCurrentText(table.item(row, 2).text())
        self._edits[CONFIG_DEVICE_TAG].setCurrentText(table.item(row, 4).text())
        idx = 3
        for tag in self._tags[4:]:
            if tag != CONFIG_DEVICE_TAG:
                self._edits[tag].setText(table.item(row, idx).text())
            idx += 1
        '''

    def check(self):
        for id, tag in enumerate(self._tags[1:]):
            if (id not in self.__ignored_idx) and (self._edits[tag].text() == ''):
                return False
        return True


class DependentParameters(ParametersDialog):
    def __init__(self, parent, tags):
        super().__init__(parent, tags)

    def _create_edits(self):
        self._edits = {}
        self.__ignored_idx = []

        for id, tag in enumerate(self._tags[1:]):
            if id not in self.__ignored_idx:
                self._edits[id] = QLineEdit(self._parent)
        '''
        self._edits = dict.fromkeys(self._tags[1:])
        for key in self._edits:
            self._edits[key] = QLineEdit(self._parent)
        '''

    def get_values(self):
        values = []
        for id, tag in enumerate(self._tags[1:]):
            if id not in self.__ignored_idx:
                values.append(self._edits[id].text())
            else:
                values.append(self._edits[id].currentText())
        return values
        '''
        values = []
        for tag in self._tags[1:]:
            values.append(self._edits[tag].text())
        return values
        '''

    def load_values_from_table_row(self, table, row):
        for id, tag in enumerate(self._tags[1:]):
            if id not in self.__ignored_idx:
                self._edits[id].setText(table.item(row, id).text())
            else:
                self._edits[id].setCurrentText(table.item(row, id).text())
        '''
        for tag in self._tags[1:]:
            self._edits[tag].setText(table.item(row, table.headers.index(tag)).text())
        '''

    def check(self):
        return True


class DefaultQuantizationDialog(DependentParameters):
    def __init__(self, parent):
        super().__init__(parent, ['DefaultQuantization', *HEADER_DQ_PARAMS_TAGS])

    def check(self):
        '''
        if self._edits[CONFIG_MODE_TAG].text() == '':
            return False
        '''
        return True


class AccuracyAwareQuantizationDialog(DependentParameters):
    def __init__(self, parent):
        super().__init__(parent, ['DefaultQuantization:', *HEADER_AAQ_PARAMS_TAGS])


'''
    def __init__(self, parent, models, data):
        super().__init__(parent)
        self.__title = 'Information about model'
        self.__pot_params_tags = HEADER_POT_PARAMS_TAGS
        self.__model_params_tags = HEADER_MODEL_PARAMS_MODEL_TAGS + \
            HEADER_MODEL_PARAMS_ENGINE_TAGS + HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS + []
        self.tags = [*self.__pot_params_tags, *self.__model_params_tags]
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle(self.__title)
        self.__create_labels()
        self.__create_edits()
        self.__create_layout()

    def __create_labels(self):
        self.labels = dict.fromkeys(self.tags)
        for key in self.labels:
            self.labels[key] = QLabel(key)

    def __create_edits(self):
        self.edits = dict.fromkeys(self.tags)
        for key in self.edits:
            self.edits[key] = QLineEdit(self)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        for tag in self.tags:
            layout.addWidget(self.labels[tag], idx, 0)
            layout.addWidget(self.edits[tag], idx, 1)
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, idx, 0)
        layout.addWidget(cancel_btn, idx, 1)
        self.setLayout(layout)

    def get_values(self):
        # TODO: fix
        pot_params = []
        for tag in self.__pot_params_tags:
            pot_params.append(self.edits[tag].text())
        model_params = []
        for tag in self.__model_params_tags:
            model_params.append(self.edits[tag].text())
        # values = []
        # for tag in self.tags:
        #     values.append(self.edits[tag].text())
        # return values
        return pot_params, model_params

    def accept(self):
        check = False
        for tag in self.tags:
            if self.edits[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()

    def load_values_from_table_row(self, table, row):
        # self._edits[CONFIG_MODEL_TAG].setCurrentText(table.item(row, 0).text())
        # self._edits[CONFIG_DATASET_TAG].setCurrentText(table.item(row, 1).text())
        # self._edits[CONFIG_FRAMEWORK_TAG].setCurrentText(table.item(row, 2).text())
        # self._edits[CONFIG_DEVICE_TAG].setCurrentText(table.item(row, 4).text())
        # idx = 3
        for idx, tag in enumerate(self.tags):
            text = table.item(row, idx).text()
            if text != '':
                self.edits[tag].setText(text)
        # for tag in self._tags[4:]:
        #     if tag != CONFIG_DEVICE_TAG:
        #         self._edits[tag].setText(table.item(row, idx).text())
        #     idx += 1
'''