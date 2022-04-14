#!/usr/bin/env python
import sys
import os
import warnings
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import time as t
from .cam_controls import Cameras
from .conf_controls import Config
from .big_view import BigView
from .ops import Ops
from .howto import howto
from PyQt5.QtGui import QIcon



warnings.simplefilter('ignore', category=FutureWarning)

def resource_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, rel_path)

class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.settings = QtCore.QSettings('MPSD-CNI', 'IDIGui', self)

        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        #MainWindow.setWindowIcon(icon)




        self._init_ui()



    def _init_ui(self):
        self.setWindowTitle('BASLER BEAM PROFILE RECORDING')
        self.setWindowIcon(QIcon('logo.jpg'))
        geom = self.settings.value('geometry')
        self.resize(200,100)
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        # Options

        vbox = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        tab_conf = QtWidgets.QWidget()
        tab_cam = QtWidgets.QWidget()
        tab_bigview = QtWidgets.QWidget()
        tab_howto = QtWidgets.QWidget()
        self.tabs.addTab(tab_conf, 'Config')
        self.tabs.addTab(tab_cam, 'Cameras')
        self.tabs.addTab(tab_bigview, 'BigView')
        self.tabs.addTab(tab_howto, 'howto')
        vbox.addWidget(self.tabs)

        self.vbox_conf = QtWidgets.QVBoxLayout()
        self.vbox_cam = QtWidgets.QVBoxLayout()
        self.vbox_bigview = QtWidgets.QVBoxLayout()
        self.vbox_howto = QtWidgets.QVBoxLayout()
        tab_conf.setLayout(self.vbox_conf)
        tab_cam.setLayout(self.vbox_cam)
        tab_bigview.setLayout(self.vbox_bigview)
        tab_howto.setLayout(self.vbox_howto)

        self.ops = Ops(self)
        self.conf_controls = Config(self.ops)
        self.cam_controls = Cameras(self, self.ops)
        self.big_view = BigView(self, self.ops)
        self.how_to = howto(self, self.ops)
        self.vbox_conf.addWidget(self.conf_controls)
        self.vbox_conf.addStretch(1)
        self.vbox_cam.addWidget(self.cam_controls)
        self.vbox_bigview.addWidget(self.big_view)
        self.vbox_howto.addWidget(self.how_to)
        #layout.addWidget(self.controls)
        layout.addLayout(vbox)

        # Menu Bar
        self._init_menubar()
        self.theme = self.settings.value('theme')
        if self.theme is None:
            self.theme = 'none'
        self._set_theme(self.theme)
        self.show()

    def _init_menubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        action = QtWidgets.QAction('&Quit', self)
        action.triggered.connect(self.close)
        filemenu.addAction(action)

        # -- Theme menu
        thememenu = menubar.addMenu('&Theme')
        agroup = QtWidgets.QActionGroup(self)
        agroup.setExclusive(True)
        action = QtWidgets.QAction('None', self)
        action.triggered.connect(lambda: self._set_theme('none'))
        thememenu.addAction(action)
        agroup.addAction(action)
        action = QtWidgets.QAction('Dark', self)
        action.triggered.connect(lambda: self._set_theme('dark'))
        thememenu.addAction(action)
        agroup.addAction(action)
        action = QtWidgets.QAction('Solarized', self)
        action.triggered.connect(lambda: self._set_theme('solarized'))
        thememenu.addAction(action)
        agroup.addAction(action)

        self.show()

    def _set_theme(self, name):
        if name == 'none':
            self.setStyleSheet('')
        else:
            self.setStyleSheet('')
            if os.path.isdir(resource_path('styles/%s.qss'%name)):
                with open(resource_path('styles/%s.qss'%name), 'r') as f:
                    self.setStyleSheet(f.read())
            if name == 'solarized':
                c = (203, 76, 22, 80)
                bc = '#002b36'
            else:
                c = (0, 0, 255, 80)
                bc = (0, 0, 0)

        self.settings.setValue('theme', name)

    def keyPressEvent(self, event):
        key = event.key()
        mod = int(event.modifiers())

        if QtGui.QKeySequence(mod+key) == QtGui.QKeySequence('Ctrl+P'):
            self._prev_file()
        elif QtGui.QKeySequence(mod+key) == QtGui.QKeySequence('Ctrl+N'):
            self._next_file()
        elif QtGui.QKeySequence(mod+key) == QtGui.QKeySequence('Ctrl+W'):
            self.close()
        else:
            event.ignore()

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.geometry())
        self.cam_controls.timer.stop()
        self.cam_controls.timer2.stop()
        self.cam_controls.ops.cameras.Close()
        event.accept()

def main():
    app = QtWidgets.QApplication([])
    gui = GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
