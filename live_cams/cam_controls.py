import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from .ops import Ops
import pyqtgraph as pg
from PIL import Image
import numpy as np
from . import ccmapp
from numpy import loadtxt
import pickle

class Cameras(QtWidgets.QWidget):
    def __init__(self, parent, ops):
        super(Cameras, self).__init__()
        self.parent = parent
        self.ops = ops
        self._init_ui()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_imviews)
        self.timer.start()
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(100000)
        self.timer2.timeout.connect(self.outputdata)
        self.timer2.start()
        self.ccmap = None






    def _init_ui(self):
        hbox = QtWidgets.QHBoxLayout()
        self.setLayout(hbox)

        self.vboxes = []
        self.sel_camera_btns = []
        self.sel_ref_btns = []
        self.id_labels = []
        self.pos_labels = []
        self.avg_labels = []
        self.ref_labels = []
        self.diffref_labels = []
        self.diffcur_labels = []
        self.live_imviews = []
        self.live_imviews_np = []
        self.avg_imviews = []
        self.diffcur_imviews = []
        self.ref_imviews = []
        self.diffref_imviews = []
        self.refday_btns = []
        self.averagefromsum = []
        self.refframe = []
        for i in range(self.ops.num_cams):
            vbox = QtWidgets.QVBoxLayout()
            self.vboxes.append(vbox)
            cam_sel_btn = QtWidgets.QComboBox()
            self.sel_camera_btns.append(cam_sel_btn)
            listview = QtWidgets.QListView(self)
            cam_sel_btn.setView(listview)
            cam_sel_btn.setMinimumWidth(100)
            vbox.addWidget(cam_sel_btn)
            for i in range(self.ops.num_cams):
                #print('self.ops.num_cams: ', self.ops.num_cams)
                #print('self.parent.conf_controls.conf_indices[i] :', self.ops.conf_indices[i])
                cam_sel_btn.addItem('Camera ' + str(self.ops.conf_indices[i]+1))
            #print('self.ops.num_cams: ', self.ops.num_cams)
            #print('self.parent.conf_controls :', self.ops.conf_indices)


            id_label = QtWidgets.QLabel()
            self.id_labels.append(id_label)
            pos_label = QtWidgets.QLabel()
            self.pos_labels.append(pos_label)
            vbox.addWidget(id_label)
            vbox.addWidget(pos_label)
            avg_label = QtWidgets.QLabel()
            self.avg_labels.append(avg_label)

            ref_label = QtWidgets.QLabel()
            self.ref_labels.append(ref_label)
            diffcur_label = QtWidgets.QLabel()
            self.diffcur_labels.append(diffcur_label)
            diffref_label = QtWidgets.QLabel()
            self.diffref_labels.append(diffref_label)


            imview_live = pg.ImageView()
            imview_live.ui.roiBtn.hide()
            imview_live.ui.menuBtn.hide()
            imview_avg = pg.ImageView()
            imview_avg.ui.roiBtn.hide()
            imview_avg.ui.menuBtn.hide()
            imview_diffcur = pg.ImageView()
            imview_diffcur.ui.roiBtn.hide()
            imview_diffcur.ui.menuBtn.hide()
            imview_ref = pg.ImageView()
            imview_ref.ui.roiBtn.hide()
            imview_ref.ui.menuBtn.hide()
            imview_diffref = pg.ImageView()
            imview_diffref.ui.roiBtn.hide()
            imview_diffref.ui.menuBtn.hide()

            self.live_imviews.append(imview_live)




            self.avg_imviews.append(imview_avg)
            self.diffcur_imviews.append(imview_diffcur)
            self.ref_imviews.append(imview_ref)
            self.diffref_imviews.append(imview_diffref)

            vbox.addWidget(imview_live)
            vbox.addWidget(avg_label)
            vbox.addWidget(imview_avg)
            vbox.addWidget(ref_label)
            vbox.addWidget(imview_ref)
            vbox.addWidget(diffcur_label)
            vbox.addWidget(imview_diffcur)
            vbox.addWidget(diffref_label)
            vbox.addWidget(imview_diffref)
            #ref_sel_btn = QtWidgets.QComboBox()
            #self.sel_ref_btns.append(ref_sel_btn)
            #listview = QtWidgets.QListView(self)
            #ref_sel_btn.setView(listview)
            #ref_sel_btn.setMinimumWidth(100)
            #vbox.addWidget(ref_sel_btn)
            #ref_sel_btn.addItem('ref ' + str(self.parent.conf_controls.conf_indices[i] + 1))


            hbox.addLayout(vbox)



        for i in range(len(self.sel_camera_btns)):
            self.sel_camera_btns[i].setCurrentIndex(i)
        for i in range(self.ops.num_cams):
            self.id_labels[i].setText('Serial Number: ' + str(self.parent.conf_controls.cam_ids[self.parent.ops.conf_indices[self.sel_camera_btns[i].currentIndex()]]))
            self.pos_labels[i].setText('Position: ' + self.parent.conf_controls.cam_pos[self.parent.ops.conf_indices[self.sel_camera_btns[i].currentIndex()]])
            self.avg_labels[i].setText('todays average')
            self.ref_labels[i].setText('reference day: '+ str(self.parent.conf_controls.cam_refday[self.parent.ops.conf_indices[self.sel_camera_btns[i].currentIndex()]]))
            self.diffcur_labels[i].setText('live frame - todays average')
            self.diffref_labels[i].setText('live frame - reference day average')
        for i in range(len(self.sel_camera_btns)):
            self.sel_camera_btns[i].currentIndexChanged.connect(lambda idx=cam_sel_btn.currentIndex(), tab=self.sel_camera_btns[i]: self.change_camera(tab, idx))

    def update_imviews(self):
        self.ops.calc_image()
        for i in range(len(self.live_imviews)):
            idx = self.sel_camera_btns[i].currentIndex()
            self.ops.get_live_cam(idx)
            levels = self.parent.conf_controls.c_axis_val[self.ops.conf_indices[i]]
            #print("caxis levels from: ",  self.parent.conf_controls.cam_pos[self.parent.conf_controls.conf_indices[i]], "and Serialnumber: ",self.parent.conf_controls.serial_number[self.parent.conf_controls.conf_indices[i]] )
            #print("levels of small live view: ", levels)
            #levels = [0, 30]
            self.live_imviews[i].setImage(self.ops.live_imgs[idx].T, levels = levels)
                    #self.ccmap = ccmapp.generatePgColormap('viridis')
            #with open('colormap1') as f:
            #    for line in f:
             #       coll = line.strip()
                    # Set a custom color map
            #colors = [(0, 0, 0),(4, 5, 61),(84, 42, 55),(15, 87, 60),(208, 17, 141),(255, 255, 255)]
            #text_file = open("colormap1", "r")
            #lines = text_file.readlines()
            #print("lines:: ",type(lines))
            #text_file.close()
            #colors = [line]
            pos = np.array([0., 1., 0.5, 0.25, 0.75])
            #color = np.array(colors,dtype=np.ubyte)
            #liness = loadtxt("colormap1", comments="#", delimiter=";", unpack=False)
            #colls = coll.split(";")
            #print((colls))
            #print(coll)
            #color = [(0, 255, 255, 255), (255, 255, 0, 255), (0, 0, 0, 255), (0, 0, 255, 255), (255, 0, 0, 255)]
            #print("colors :", color)
            #sample_list = colors



            #open_file = open(file_name, "rb")
            #loaded_list = pickle.load(open_file)
            #open_file.close()
            #print("pickle: ",type(loaded_list))


            #print("self.ops.loaded_list: ",self.ops.loaded_list)
            #x = np.linspace(0, 10, 1000)
            #I = np.sin(x) * np.cos(x[:, np.newaxis])
            self.cmap = pg.ColorMap(pos, self.ops.loaded_list)


                    # color map
            #self.cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
                    #cmap = greiner
                    # setting color map to the image view
            self.live_imviews[i].setColorMap(self.cmap)
                #else:
                 #   self.ops.avrg_frames(idx)
                  #  self.imviews[i][k].setImage(self.ops.cursum(idx), autoRange=None, autoLevels=None, autoHistogramRange=None)

    def update_imavrg(self):
        for i in range(len(self.avg_imviews)):
            if sum(sum(self.ops.live_imgs[i])) > self.ops.rec_trs[self.ops.conf_indices[i]] and self.ops.flag_rec == 1:
                print("above Threshold, frame saved", "current intensity: ", sum(sum(self.ops.live_imgs[i])), "Threshold intensity: ", self.ops.rec_trs[self.ops.conf_indices[i]])
                idx = self.sel_camera_btns[i].currentIndex()
                self.ops.avrg_frames(idx)
                self.averagefromsum = np.divide(self.ops.cursum[idx], self.ops.sumframes)
                # self.avg_imviews[i].setImage(self.averagefromsum.T, autoRange=None, autoLevels=None, autoHistogramRange=None)
                levels = self.parent.conf_controls.c_axis_val[self.ops.conf_indices[i]]
                self.avg_imviews[i].setImage(self.averagefromsum.T, levels = levels)

                self.avg_imviews[i].setColorMap(self.cmap)
            else:
                print("below Threshold, frame not saved", "current intensity: ", sum(sum(self.ops.live_imgs[i])), "Threshold intensity: ", self.ops.rec_trs[self.ops.conf_indices[i]])



    def update_refview(self):
        for i in range(len(self.avg_imviews)):
            if sum(sum(self.ops.live_imgs[i])) > self.ops.rec_trs[i] or self.ops.flag_rec == 1:
                idx = self.sel_camera_btns[i].currentIndex()
                self.ops.load_ref()
                #self.ops.avrg_frames(idx)
                self.refframe = np.divide(self.ops.refsum[idx], self.ops.refnoFrames[idx])
                #self.refframe = np.subtract(self.ops.live_imgs[i], self.averagefromsum)
                levels = self.parent.conf_controls.c_axis_val[self.ops.conf_indices[i]]
                self.ref_imviews[i].setImage(self.refframe.T, levels = levels)
                self.ref_imviews[i].setColorMap(self.cmap)

    def update_diffview(self):
        for i in range(len(self.avg_imviews)):
            if sum(sum(self.ops.live_imgs[i])) > self.ops.rec_trs[i] or self.ops.flag_rec == 1:
                idx = self.sel_camera_btns[i].currentIndex()
                self.ops.avrg_frames(idx)
                self.averagefromsum = np.divide(self.ops.cursum[idx], self.ops.sumframes)
                self.diffframe = np.subtract(self.ops.live_imgs[i], self.averagefromsum)
                self.diffcur_imviews[i].setImage(self.diffframe.T, levels = [-10, 10])
                self.diffcur_imviews[i].setColorMap(self.cmap)

    def update_diffrefview(self):
        for i in range(len(self.avg_imviews)):
            if sum(sum(self.ops.live_imgs[i])) > self.ops.rec_trs[i] or self.ops.flag_rec == 1:
                idx = self.sel_camera_btns[i].currentIndex()
                print("diffrefview from cam: ", self.ops.cam_filepath[self.ops.conf_indices[idx]], "with records in avrg: ",self.ops.refnoFrames[idx])
                self.ops.load_ref()
                self.refframe = np.divide(self.ops.refsum[idx], self.ops.refnoFrames[idx])
                self.diffrefframe = np.subtract(self.ops.live_imgs[idx], self.refframe)
                self.diffref_imviews[idx].setImage(self.diffrefframe.T, levels = [-10, 10])
                self.diffref_imviews[idx].setColorMap(self.cmap)




    def change_camera(self, tab, idx):
        tab_idx = None
        for i in range(len(self.sel_camera_btns)):
            if self.sel_camera_btns[i] == tab:
                tab_idx = i
        self.id_labels[tab_idx].setText('Serial Number: ' + str(self.parent.conf_controls.cam_ids[self.sel_camera_btns[idx].currentIndex()]))
        self.pos_labels[tab_idx].setText('Position: ' + self.parent.conf_controls.cam_pos[self.sel_camera_btns[idx].currentIndex()])
        print('type tab in change_camera',type(tab))
        self.live_imviews[tab].setImage(self.ops.live_imgs)
        self.avg_imviews[tab].setImage(self.ops.cursum)
        #self.ref_imviews[tab].setImage(self.ops._imgs)
        #self.dum_imviews[tab].setImage(self.ops.live_imgs)
        #self.imviews[tab_idx][0].setImage(self.ops.live_imgs[0])

    def outputdata(self):
        self.ops.save_frames()
        self.ops.loadandsave_sumofframes()
        self.update_imavrg()
        self.update_refview()
        self.update_diffview()
        self.update_diffrefview()



