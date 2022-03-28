from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
# from config_maker.tags import CONFIG_MODEL_NAME_TAG, CONFIG_WEIGHTS_TAG
# from tags import CONFIG_CONFIG_TAG, CONFIG_QUANTIZATION_METHOD_TAG, CONFIG_NAME_TAG, \
#     CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_PRESET_TAG, CONFIG_AC_CONFIG_TAG, \
#     CONFIG_MAX_DROP_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG, \
#     CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG
from tags import CONFIG_CONFIG_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG, \
    CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG, HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS
from tags import CONFIG_MODEL_NAME_TAG, CONFIG_MODEL_TAG, CONFIG_WEIGHTS_TAG
from tags import HEADER_POT_PARAMS_TAGS, HEADER_MODEL_PARAMS_MODEL_TAGS, HEADER_MODEL_PARAMS_ENGINE_TAGS


class QuantizationConfigDialog(QDialog):
    def __init__(self, parent, models, data):
        super().__init__(parent)
        self.__title = 'Information about model'
        # self.__pot_params_tags = [CONFIG_CONFIG_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, \
        #     CONFIG_DIRECT_DUMP_TAG, CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, \
        #     CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG]
        # self.__model_params_model_tags = [CONFIG_MODEL_NAME_TAG, CONFIG_MODEL_TAG, CONFIG_WEIGHTS_TAG]
        self.__pot_params_tags = HEADER_POT_PARAMS_TAGS
        self.__model_params_tags = HEADER_MODEL_PARAMS_MODEL_TAGS + \
            HEADER_MODEL_PARAMS_ENGINE_TAGS + HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS + []
        # self.__model_params_model_tags = HEADER_MODEL_PARAMS_MODEL_TAGS
        # self.__model_params_engine_tags = []
        # self.__model_params_compression_tags = []
        self.tags = []
        self.tags.extend(self.__pot_params_tags)
        self.tags.extend(self.__model_params_tags)
        # self.tags.extend(self.__model_params_model_tags)
        # self.tags.extend(self.__model_params_engine_tags)
        # self.tags.extend(self.__model_params_compression_tags)
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
