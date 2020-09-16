from PyQt5.QtWidgets import *
from models.models import *
from PyQt5 import QtCore


class ModelDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self._title = 'Information about model'
        self._tags = ['Task', 'Name', 'Presicion', 'SourceFramework', 'ModelPath', 'WeightsPath']
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(self._title)
        self._create_labels()
        self._create_lines_edit()
        self._create_layout()

    def _create_labels(self):
        self._labels = dict.fromkeys(self._tags)
        for key in self._labels:
            self._labels[key] = QLabel(key)

    def _create_lines_edit(self):
        self._lines_edit = dict.fromkeys(self._tags)
        for key in self._lines_edit:
            self._lines_edit[key] = QLineEdit(self)

    def _create_layout(self):
        layout = QGridLayout()
        idx = 0
        for tag in self._tags:
            layout.addWidget(self._labels[tag], idx, 0)
            layout.addWidget(self._lines_edit[tag], idx, 1)
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, idx, 0)
        layout.addWidget(cancel_btn, idx, 1)
        self.setLayout(layout)

    def accept(self):
        check = False;
        for tag in self._tags:
            if self._lines_edit[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        for tag in self._tags:
            self._lines_edit[tag].clear()


class DataDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = QLineEdit(self)
        self.path = QLineEdit(self)
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about dataset')
        name_lb = QLabel('Name')
        path_lb = QLabel('Path')
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout = QGridLayout()
        layout.addWidget(name_lb, 0, 0)
        layout.addWidget(self.name, 0, 1)
        layout.addWidget(path_lb, 1, 0)
        layout.addWidget(self.path, 1, 1)
        layout.addWidget(ok_btn, 2, 0)
        layout.addWidget(cancel_btn, 2, 1)
        self.setLayout(layout)

    def accept(self):
        if ((self.name.text() == '') or (self.path.text() == '')):
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        self.name.clear()
        self.path.clear()


class BenchmarkDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__framework_independet_tags = ['FrameworkIndependent:', 'Model', 'Dataset', 'Framework', 'BatchSize',
                                            'Device', 'IterationCount', 'TestTimeLimit']
        self.__openvino_tags = ['OpenVINO DLDT:', 'Mode', 'Extension', 'AsyncRequestCount', 'ThreadCount', 'StreamCount']
        self.__caffe_tags = ['Caffe:', 'ChannelSwap', 'Mean', 'InputScale']
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about test')
        self.__create_labels()
        self.__create_lines_edit()
        self.__create_layout()

    def __create_labels(self):
        self.__create_framework_independet_labels()
        self.__create_openvino_labels()
        self.__create_caffe_labels()

    def __create_framework_independet_labels(self):
        self.__framework_independet_labels = dict.fromkeys(self.__framework_independet_tags)
        for key in self.__framework_independet_labels:
            self.__framework_independet_labels[key] = QLabel(key)
        self.__framework_independet_labels['FrameworkIndependent:'].setStyleSheet("font-weight: bold")

    def __create_openvino_labels(self):
        self.__openvino_labels = dict.fromkeys(self.__openvino_tags)
        for key in self.__openvino_labels:
            self.__openvino_labels[key] = QLabel(key)
        self.__openvino_labels['OpenVINO DLDT:'].setStyleSheet("font-weight: bold")

    def __create_caffe_labels(self):
        self.__caffe_labels = dict.fromkeys(self.__caffe_tags)
        for key in self.__caffe_labels:
            self.__caffe_labels[key] = QLabel(key)
        self.__caffe_labels['Caffe:'].setStyleSheet("font-weight: bold")

    def __create_lines_edit(self):
        self.__create_framework_independet_lines_edit()
        self.__create_openvino_lines_edit()
        self.__create_caffe_lines_edit()

    def __create_framework_independet_lines_edit(self):
        self.__framework_independet_lines_edit = dict.fromkeys(self.__framework_independet_tags[1:])
        for key in self.__framework_independet_lines_edit:
            if key is 'Framework':
                self.__framework_independet_lines_edit[key] = QComboBox()
                self.__framework_independet_lines_edit[key].addItems(('OpenVINO DLDT', 'Caffe'))
                self.__framework_independet_lines_edit[key].activated[str].connect(self.__framework_choice)
            else:
                self.__framework_independet_lines_edit[key] = QLineEdit(self)

    def __create_openvino_lines_edit(self):
        self.__openvino_lines_edit = dict.fromkeys(self.__openvino_tags[1:])
        for key in self.__openvino_lines_edit:
            self.__openvino_lines_edit[key] = QLineEdit(self)

    def __create_caffe_lines_edit(self):
        self.__caffe_lines_edit = dict.fromkeys(self.__caffe_tags[1:])
        for key in self.__caffe_lines_edit:
            self.__caffe_lines_edit[key] = QLineEdit(self)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        layout.addWidget(self.__framework_independet_labels['FrameworkIndependent:'], idx, 0)
        idx += 1
        for tag in self.__framework_independet_tags[1:]:
            layout.addWidget(self.__framework_independet_labels[tag], idx, 0)
            layout.addWidget(self.__framework_independet_lines_edit[tag], idx, 1)
            idx += 1
        openvino_idx = idx
        layout.addWidget(self.__openvino_labels['OpenVINO DLDT:'], openvino_idx, 0)
        openvino_idx += 1
        for tag in self.__openvino_tags[1:]:
            layout.addWidget(self.__openvino_labels[tag], openvino_idx, 0)
            layout.addWidget(self.__openvino_lines_edit[tag], openvino_idx, 1)
            openvino_idx += 1
        layout.addWidget(self.__caffe_labels['Caffe:'], idx, 0)
        idx += 1
        for tag in self.__caffe_tags[1:]:
            layout.addWidget(self.__caffe_labels[tag], idx, 0)
            layout.addWidget(self.__caffe_lines_edit[tag], idx, 1)
            self.__caffe_labels[tag].hide()
            self.__caffe_lines_edit[tag].hide()
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, max(idx, openvino_idx), 0)
        layout.addWidget(cancel_btn, max(idx, openvino_idx), 1)
        self.setLayout(layout)

    def __framework_choice(self, type):
        if type == 'OpenVINO DLDT':
            self.__openvino_labels['OpenVINO DLDT:'].show()
            self.__caffe_labels['Caffe:'].hide()
            for tag in self.__openvino_tags[1:]:
                self.__openvino_labels[tag].show()
                self.__openvino_lines_edit[tag].show()
            for tag in self.__caffe_tags[1:]:
                self.__caffe_labels[tag].hide()
                self.__caffe_lines_edit[tag].hide()
                self.__caffe_lines_edit[tag].clear()
        elif type == 'Caffe':
            self.__openvino_labels['OpenVINO DLDT:'].hide()
            self.__caffe_labels['Caffe:'].show()
            for tag in self.__openvino_tags[1:]:
                self.__openvino_labels[tag].hide()
                self.__openvino_lines_edit[tag].hide()
                self.__openvino_lines_edit[tag].clear()
            for tag in self.__caffe_tags[1:]:
                self.__caffe_labels[tag].show()
                self.__caffe_lines_edit[tag].show()

    def accept(self):
        if ((self.model.text() == '') or (self.dataset.text() == '') or (self.batch_size.text() == '') or
                (self.device.text() == '') or (self.iter_count.text() == '') or (self.test_time_limit.text() == '')):
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        self.__openvino_labels['OpenVINO DLDT:'].show()
        self.__caffe_labels['Caffe:'].hide()
        for tag in self.__framework_independet_tags[1:]:
            if tag is 'Framework':
                self.__framework_independet_lines_edit[tag].setCurrentIndex(0)
            else:
                self.__framework_independet_lines_edit[tag].clear()
        for tag in self.__openvino_tags[1:]:
            self.__openvino_labels[tag].show()
            self.__openvino_lines_edit[tag].show()
            self.__openvino_lines_edit[tag].clear()
        for tag in self.__caffe_tags[1:]:
            self.__caffe_labels[tag].hide()
            self.__caffe_lines_edit[tag].hide()
            self.__caffe_lines_edit[tag].clear()


class RemoteDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__tags = ['IP', 'Login', 'Password', 'OS', 'FTPClientPath', 'BenchmarkConfig', 'LogFile', 'ResultFile']
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about computer')
        self.__create_labels()
        self.__create_lines_edit()
        self.__create_layout()

    def __create_labels(self):
        self.__labels = dict.fromkeys(self.__tags)
        for key in self.__labels:
            self.__labels[key] = QLabel(key)

    def __create_lines_edit(self):
        self.__lines_edit = dict.fromkeys(self.__tags)
        for key in self.__lines_edit:
            self.__lines_edit[key] = QLineEdit(self)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        for tag in self.__tags:
            layout.addWidget(self.__labels[tag], idx, 0)
            layout.addWidget(self.__lines_edit[tag], idx, 1)
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, idx, 0)
        layout.addWidget(cancel_btn, idx, 1)
        self.setLayout(layout)

    def accept(self):
        check = False;
        for tag in self.__tags:
            if self.__lines_edit[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        for tag in self.__tags:
            self.__lines_edit[tag].clear()


class DeployDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__tags = ['IP', 'Login', 'Password', 'OS', 'Download folder']
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about computer')
        self.__create_labels()
        self.__create_lines_edit()
        self.__create_layout()

    def __create_labels(self):
        self.__labels = dict.fromkeys(self.__tags)
        for key in self.__labels:
            self.__labels[key] = QLabel(key)

    def __create_lines_edit(self):
        self.__lines_edit = dict.fromkeys(self.__tags)
        for key in self.__lines_edit:
            self.__lines_edit[key] = QLineEdit(self)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        for tag in self.__tags:
            layout.addWidget(self.__labels[tag], idx, 0)
            layout.addWidget(self.__lines_edit[tag], idx, 1)
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, idx, 0)
        layout.addWidget(cancel_btn, idx, 1)
        self.setLayout(layout)

    def accept(self):
        check = False
        for tag in self.__tags:
            if self.__lines_edit[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        for tag in self.__tags:
            self.__lines_edit[tag].clear()
