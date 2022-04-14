import os
from PyQt5 import QtWidgets, QtGui, QtCore
from ops import Ops
import pyqtgraph as pg
import yaml

class Config(QtWidgets.QWidget):
    def __init__(self, ops):
        super(Config, self).__init__()
        self.fname = 'config.yml'
        self.ops = ops
        self.config = None
        self.config_labels = []
        self.cam_ids = []
        self.cam_pos = []
        self.cam_inttime = []
        self.cam_refday = []
        self.conf_indices = []
        self.cam_filepath = []
        self.c_axis_val = []
        self.serial_number = []
        self.maindatatdir = 'data'
        self._init_ui()


    def _init_ui(self):
        self.hbox = QtWidgets.QHBoxLayout()
        self.setLayout(self.hbox)
        self.headline = QtGui.QFont('Arial', 12, QtGui.QFont.Bold)
        self.init_cameras()
        self.load_config()

    def load_config(self):
        with open(self.fname, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        vbox_cam = QtWidgets.QVBoxLayout()
        vbox_id = QtWidgets.QVBoxLayout()
        vbox_pos = QtWidgets.QVBoxLayout()
        vbox_status = QtWidgets.QVBoxLayout()

        label_cam = QtWidgets.QLabel()
        label_id = QtWidgets.QLabel()
        label_pos = QtWidgets.QLabel()
        label_status = QtWidgets.QLabel()
        label_cam.setText('Camera')
        label_cam.setAlignment(QtCore.Qt.AlignCenter)
        label_cam.setFont(self.headline)
        label_id.setText('Camera ID')
        label_id.setFont(self.headline)
        label_id.setAlignment(QtCore.Qt.AlignCenter)
        label_pos.setText('Camera postion')
        label_pos.setFont(self.headline)
        label_pos.setAlignment(QtCore.Qt.AlignCenter)
        label_status.setText('Camera status')
        label_status.setFont(self.headline)
        label_status.setAlignment(QtCore.Qt.AlignCenter)
        vbox_cam.addWidget(label_cam)
        vbox_id.addWidget(label_id)
        vbox_pos.addWidget(label_pos)
        vbox_status.addWidget(label_status)
        vbox_cam.addStretch(1)
        vbox_id.addStretch(1)
        vbox_pos.addStretch(1)
        vbox_status.addStretch(1)
        counter = 0
        for cam, _ in self.config.items():
            label_cam = QtWidgets.QLabel()
            label_id = QtWidgets.QLabel()
            label_pos = QtWidgets.QLabel()
            label_status = QtWidgets.QLabel()
            keys = dict(self.config[cam].items())
            serial_number = keys['SerialNumber']
            cam_pos = keys['Position']
            cam_inttime = keys['inttime']
            cam_filepath = keys['filepath']
            cam_refday = keys['refday']
            c_axis_val= keys["caxisval"]
            self.cam_ids.append(serial_number)
            self.cam_pos.append(cam_pos)
            self.cam_inttime.append(cam_inttime)
            self.cam_filepath.append(cam_filepath)
            self.cam_refday.append(cam_refday)
            self.c_axis_val.append(c_axis_val)
            self.serial_number.append(serial_number)
            label_cam.setText(str(cam))
            label_cam.setAlignment(QtCore.Qt.AlignCenter)
            label_id.setText(str(serial_number))
            label_id.setAlignment(QtCore.Qt.AlignCenter)
            label_pos.setText(cam_pos)
            label_pos.setAlignment(QtCore.Qt.AlignCenter)
            #print('self.ops.serial_numbers: ', self.ops.serial_numbers)
            if str(serial_number) in self.ops.serial_numbers:
                status = 'on'
                label_status.setStyleSheet('background-color: green')
                self.conf_indices.append(counter)
            else:
                status = 'off'
                label_status.setStyleSheet('background-color: red')

            label_status.setText(status)
            label_status.setAlignment(QtCore.Qt.AlignCenter)
            vbox_cam.addWidget(label_cam)
            vbox_id.addWidget(label_id)
            vbox_pos.addWidget(label_pos)
            vbox_status.addWidget(label_status)
            vbox_cam.addStretch(1)
            vbox_id.addStretch(1)
            vbox_pos.addStretch(1)
            vbox_status.addStretch(1)
            counter += 1
        self.hbox.addLayout(vbox_cam)
        self.hbox.addLayout(vbox_id)
        self.hbox.addLayout(vbox_pos)
        self.hbox.addLayout(vbox_status)
        #print('cam indices: ', self.conf_indices)
    def init_cameras(self):
        self.ops.load_cameras()
        self.ops.init_directories()
        self.ops.load_integrationtime()


