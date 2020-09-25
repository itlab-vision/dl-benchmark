from PyQt5.QtWidgets import *


class ModelDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = 'Information about model'
        self.tags = ['Task', 'Name', 'Presicion', 'SourceFramework', 'ModelPath', 'WeightsPath']
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
        values = []
        for tag in self.tags:
            values.append(self.edits[tag].text())
        return values

    def accept(self):
        check = False
        for tag in self.tags:
            if self.edits[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()


class DataDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = 'Information about dataset'
        self.tags = ['Name', 'Path']
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
        values = []
        for tag in self.tags:
            values.append(self.edits[tag].text())
        return values

    def accept(self):
        check = False
        for tag in self.tags:
            if self.edits[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()


class BenchmarkDialog(QDialog):
    def __init__(self, parent, models, data):
        super().__init__(parent)
        self.framework_independent_tags = ['FrameworkIndependent:', 'Model', 'Dataset', 'Framework', 'BatchSize',
                                            'Device', 'IterationCount', 'TestTimeLimit']
        self.openvino_tags = ['OpenVINO DLDT:', 'Mode', 'Extension', 'AsyncRequestCount', 'ThreadCount', 'StreamCount']
        self.caffe_tags = ['Caffe:', 'ChannelSwap', 'Mean', 'InputScale']
        self.__models_list = models
        self.__data_list = data
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about test')
        self.__create_labels()
        self.__create_edits()
        self.__create_layout()

    def __create_labels(self):
        self.__create_framework_independent_labels()
        self.__create_openvino_labels()
        self.__create_caffe_labels()

    def __create_framework_independent_labels(self):
        self.framework_independent_labels = dict.fromkeys(self.framework_independent_tags)
        for key in self.framework_independent_labels:
            self.framework_independent_labels[key] = QLabel(key)
        self.framework_independent_labels['FrameworkIndependent:'].setStyleSheet("font-weight: bold")

    def __create_openvino_labels(self):
        self.openvino_labels = dict.fromkeys(self.openvino_tags)
        for key in self.openvino_labels:
            self.openvino_labels[key] = QLabel(key)
        self.openvino_labels['OpenVINO DLDT:'].setStyleSheet("font-weight: bold")

    def __create_caffe_labels(self):
        self.caffe_labels = dict.fromkeys(self.caffe_tags)
        for key in self.caffe_labels:
            self.caffe_labels[key] = QLabel(key)
        self.caffe_labels['Caffe:'].setStyleSheet("font-weight: bold")

    def __create_edits(self):
        self.__create_framework_independent_edits()
        self.__create_openvino_edits()
        self.__create_caffe_edits()

    def __create_framework_independent_edits(self):
        self.framework_independent_edits = dict.fromkeys(self.framework_independent_tags[1:])
        self.framework_independent_edits['Model'] = QComboBox()
        for model in self.__models_list:
            self.framework_independent_edits['Model'].addItem(model)
        self.framework_independent_edits['Dataset'] = QComboBox()
        for data in self.__data_list:
            self.framework_independent_edits['Dataset'].addItem(data)
        self.framework_independent_edits['Framework'] = QComboBox()
        self.framework_independent_edits['Framework'].addItems(('OpenVINO DLDT', 'Caffe'))
        self.framework_independent_edits['Framework'].activated[str].connect(self.__framework_choice)
        self.framework_independent_edits['Framework'].currentTextChanged[str].connect(self.__framework_choice)
        for tag in self.framework_independent_tags[4:]:
            self.framework_independent_edits[tag] = QLineEdit(self)

    def __create_openvino_edits(self):
        self.openvino_edits = dict.fromkeys(self.openvino_tags[1:])
        for key in self.openvino_edits:
            self.openvino_edits[key] = QLineEdit(self)

    def __create_caffe_edits(self):
        self.caffe_edits = dict.fromkeys(self.caffe_tags[1:])
        for key in self.caffe_edits:
            self.caffe_edits[key] = QLineEdit(self)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        layout.addWidget(self.framework_independent_labels['FrameworkIndependent:'], idx, 0)
        idx += 1
        for tag in self.framework_independent_tags[1:]:
            layout.addWidget(self.framework_independent_labels[tag], idx, 0)
            layout.addWidget(self.framework_independent_edits[tag], idx, 1)
            idx += 1
        openvino_idx = idx
        layout.addWidget(self.openvino_labels['OpenVINO DLDT:'], openvino_idx, 0)
        openvino_idx += 1
        for tag in self.openvino_tags[1:]:
            layout.addWidget(self.openvino_labels[tag], openvino_idx, 0)
            layout.addWidget(self.openvino_edits[tag], openvino_idx, 1)
            openvino_idx += 1
        self.caffe_labels['Caffe:'].hide()
        layout.addWidget(self.caffe_labels['Caffe:'], idx, 0)
        idx += 1
        for tag in self.caffe_tags[1:]:
            layout.addWidget(self.caffe_labels[tag], idx, 0)
            layout.addWidget(self.caffe_edits[tag], idx, 1)
            self.caffe_labels[tag].hide()
            self.caffe_edits[tag].hide()
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, max(idx, openvino_idx), 0)
        layout.addWidget(cancel_btn, max(idx, openvino_idx), 1)
        self.setLayout(layout)

    def __framework_choice(self, framework):
        if framework == 'OpenVINO DLDT':
            self.openvino_labels['OpenVINO DLDT:'].show()
            self.caffe_labels['Caffe:'].hide()
            for tag in self.openvino_tags[1:]:
                self.openvino_labels[tag].show()
                self.openvino_edits[tag].show()
            for tag in self.caffe_tags[1:]:
                self.caffe_labels[tag].hide()
                self.caffe_edits[tag].hide()
        elif framework == 'Caffe':
            self.openvino_labels['OpenVINO DLDT:'].hide()
            self.caffe_labels['Caffe:'].show()
            for tag in self.openvino_tags[1:]:
                self.openvino_labels[tag].hide()
                self.openvino_edits[tag].hide()
            for tag in self.caffe_tags[1:]:
                self.caffe_labels[tag].show()
                self.caffe_edits[tag].show()

    def get_selected_framework(self):
        return self.framework_independent_edits['Framework'].currentText()

    def get_framework_independent_values(self):
        values = []
        values.append(self.framework_independent_edits['Model'].currentText())
        values.append(self.framework_independent_edits['Dataset'].currentText())
        values.append(self.framework_independent_edits['Framework'].currentText())
        for tag in self.framework_independent_tags[4:]:
            values.append(self.framework_independent_edits[tag].text())
        return values

    def get_openvino_values(self):
        values = []
        for tag in self.openvino_tags[1:]:
            values.append(self.openvino_edits[tag].text())
        return values

    def get_caffe_values(self):
        values = []
        for tag in self.caffe_tags[1:]:
            values.append(self.caffe_edits[tag].text())
        return values

    def accept(self):
        check = False
        for tag in self.framework_independent_tags[4:]:
            if self.framework_independent_edits[tag].text() == '':
                check = True
        framework = self.get_selected_framework()
        if framework == 'OpenVINO DLDT':
            for tag in self.openvino_tags[1:]:
                if self.openvino_edits[tag].text() == '':
                    check = True
        elif framework == 'Caffe':
            for tag in self.caffe_tags[1:]:
                if self.caffe_edits[tag].text() == '':
                    check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()


class RemoteDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.tags = ['IP', 'Login', 'Password', 'OS', 'FTPClientPath', 'BenchmarkConfig', 'LogFile', 'ResultFile']
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about computer')
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
        values = []
        for tag in self.tags:
            values.append(self.edits[tag].text())
        return values

    def accept(self):
        check = False
        for tag in self.tags:
            if self.edits[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()


class DeployDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.tags = ['IP', 'Login', 'Password', 'OS', 'Download folder']
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about computer')
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
        values = []
        for tag in self.tags:
            values.append(self.edits[tag].text())
        return values

    def accept(self):
        check = False
        for tag in self.tags:
            if self.edits[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()
