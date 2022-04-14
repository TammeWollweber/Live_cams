import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from .ops import Ops
import pyqtgraph as pg
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton
import numpy as np
class BigView(QtWidgets.QWidget):

    def __init__(self, parent, ops):
        super(BigView, self).__init__()
        self.parent = parent
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.fname = self.path + '/config.yml'
        self.ops = ops
        self.config = None
        self.config_labels = []
        self.cam_ids = []
        self.cam_pos = []
        self.cam_inttime = []
        self.cam_refday = []
        self.conf_indices = []
        self.cam_filepath = []
        self.maindatatdir = 'data'
        self._init_ui()
        self.timer3 = QtCore.QTimer()
        self.timer3.setInterval(1000)
        self.timer3.timeout.connect(self.updatebigview)
        self.timer3.start()


    def _init_ui(self):
        self.vbox = QtWidgets.QVBoxLayout()
        self.vboxes = []
        self.big_imviews = []
        self.combos = []
        self.setLayout(self.vbox)
        self.headline = QtGui.QFont('Arial', 12, QtGui.QFont.Bold)
        self.bigview_live = []
        self.sel_btn = []
        #self.combo = QComboBox(self)


        #for i in range(self.ops.num_cams):
         #   self.combo.addItem('Camera ' + str(self.parent.conf_controls.conf_indices[i] + 1))


        #self.combo.currentIndexChanged.connect(self.updatebigview)

        vbox_sel = QtWidgets.QVBoxLayout()
        self.sel_btn = QtWidgets.QComboBox()
        #self.sel_camera_btns.append(cam_sel_btn)
        listview = QtWidgets.QListView(self)
        self.sel_btn.setView(listview)
        self.sel_btn.setMinimumWidth(100)
        vbox_sel.addWidget(self.sel_btn)
        for i in range(self.ops.num_cams):
            self.sel_btn.addItem('Camera ' + str(self.parent.ops.conf_indices[i] + 1))
        self.vbox.addLayout(vbox_sel)


        self.bigview_live = pg.ImageView()
        self.bigview_live.ui.roiBtn.hide()
        self.bigview_live.ui.menuBtn.hide()
        vbox_bigview = QtWidgets.QVBoxLayout()
        vbox_bigview.addWidget(self.bigview_live)
        self.vbox.addLayout(vbox_bigview)

    def updatebigview(self):
        index = self.sel_btn.currentIndex()
        self.ops.get_live_cam(index)
        #levels = [10, 200]
        levels = self.parent.conf_controls.c_axis_val[self.parent.ops.conf_indices[index]]
        #self.bigview_live.setImage(self.ops.live_imgs[index].T)
        self.bigview_live.setImage(self.ops.live_imgs[index].T, levels=levels)
        # Set a custom color map
        #colors = [
        #    (0, 0, 0),
        #    (4, 5, 61),
        #    (84, 42, 55),
        #    (15, 87, 60),
        #    (208, 17, 141),
        #    (255, 255, 255)
        #]
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        #color = np.array(
        #    [[0, 255, 255, 255], [255, 255, 0, 255], [0, 0, 0, 255], (0, 0, 255, 255), (255, 0, 0, 255)],
        #    dtype=np.ubyte)
        #self.cmap = pg.ColorMap(pos, color)
        self.cmap = pg.ColorMap(pos, self.ops.loaded_list)
        self.bigview_live.setColorMap(self.cmap)
