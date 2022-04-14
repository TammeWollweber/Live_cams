import os
from PyQt5 import QtWidgets, QtGui, QtCore
import yaml

class howto(QtWidgets.QWidget):
    def __init__(self, parent, ops):
        super(howto, self).__init__()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.fname = self.path + '/manual.yml'
        self.ops = ops
        self.manual = None
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
        self.load_text()

    def load_text(self):
        with open(self.path + '/manual.txt') as f:
            contents = f.read()
        vbox_cam = QtWidgets.QVBoxLayout()
        label_cam = QtWidgets.QLabel()
        label_cam.setText(str(contents))
        #label_cam.setText('Camera')
        label_cam.setAlignment(QtCore.Qt.AlignLeft)

        label_cam.setFont(self.headline)
        vbox_cam.addWidget(label_cam)
        vbox_cam.addStretch(1)
        self.hbox.addLayout(vbox_cam)
