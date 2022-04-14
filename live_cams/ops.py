import sys
import os
from pypylon import pylon
from pypylon import genicam
import platform
import time
import numpy as np
import yaml
from datetime import date, timedelta
from numpy import savetxt
from numpy import loadtxt
from os import listdir
from re import search
import glob
import pickle



class Ops():
    def __init__(self, parent):
        self.parent = parent
        self.num_cams = None
        self.data = None
        self.live_imgs = []
        self.save_imgs = []
        self.cameras = []
        self.max_cams = 10
        self.serial_numbers = []
        self.cam_inttime = []
        self.rec_trs = []
        self.ref_day = []
        self.mainpath = 'data'
        self.curdir = []
        self.cam_filepath = []
        self.k = []
        self.img = pylon.PylonImage()
        self.fname = 'config.yml'
        self.load_config()
        self.converter = pylon.ImageFormatConverter()
        self.today = None
        self.is_dir = []
        self.list = []
        self.number_files = []
        self.pixmap = []
        self.filename = []
        self.fileformat = '.Tiff'
        self.fileformatsum = '.npy'
        self.newsum = []
        self.cursum = []
        self.refsum = []
        self.averagefromsum = []
        self.diffframe = []
        self.live_imgs_np = []
        self.refnoFrames = []
        self.refsumfilename = []
        self.conf_indices = []
        self.loaded_list = []
        self.flag_rec = 1
        self.camfpathloc = []





    def init_directories(self):
        self.today = date.today().strftime("%Y%m%d")
        self.k = np.zeros((self.num_cams))
        self.number_files  = np.zeros((self.num_cams))
        with open(self.fname, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        counters = 0

        self.conf_indices = [1]*self.num_cams
        for cam, _ in self.config.items():
            keys = dict(self.config[cam].items())
            serial_number = keys['SerialNumber']
            cam_identifier = keys['camident']
            print('cam_identifier', cam_identifier)
            print('serial_number', serial_number)
            print('self.serial_numbers: ', self.serial_numbers)
            if str(serial_number) in self.serial_numbers:
                indexx = self.serial_numbers.index(str(serial_number))
                print('indexx: ', indexx)
                self.conf_indices[indexx] = cam_identifier-1
                print('self.conf_indices: ', self.conf_indices)
                counters += 1


        for i in range(self.num_cams):
            self.curdir = os.path.join(self.mainpath, str(self.today), self.cam_filepath[self.conf_indices[i]]);
            self.is_dir = os.path.isdir(self.curdir);
            if self.is_dir == False:
                os.makedirs((self.curdir));
                print('no such dir yet')
            elif self.is_dir == True:
                self.list = os.listdir(self.curdir)
                self.number_files[i] = len(self.list)
                self.k[i] = self.number_files[i]-1
                print(self.number_files[i])
            self.number = '{:0>4}'.format(self.k[i]);

    def load_config(self):
        with open(self.fname, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        for cam, _ in self.config.items():
            keys = dict(self.config[cam].items())
            cam_inttime = keys['inttime']
            self.cam_inttime.append(cam_inttime)
            cam_filepath = keys['filepath']
            self.cam_filepath.append(cam_filepath)
            rec_trs = keys['rec_trs']
            self.rec_trs.append(rec_trs)
            ref_day = keys['refday']
            self.ref_day.append(ref_day)

    def load_cameras(self):
        favorite_color = pickle.load(open("colormap1.pkl", "rb"))
        self.loaded_list = favorite_color
        print("self.loaded_list: ", self.loaded_list)
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        self.num_cams = len(devices)
        self.live_imgs = [None] * self.num_cams
        self.live_imgs_np = [None] * self.num_cams
        self.cameras = pylon.InstantCameraArray(min(len(devices), self.max_cams))
        print('self.cameras: ', self.cameras)
        for i, cam in enumerate(self.cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))
            #cam.Attach(tlFactory.CreateDevice(devices[i]))
            print("Using device ", cam.GetDeviceInfo().GetModelName(), cam.GetDeviceInfo().GetSerialNumber())
            self.serial_numbers.append(cam.GetDeviceInfo().GetSerialNumber())
            #if search("g", cam.GetDeviceInfo().GetModelName()):
        if self.num_cams > 0:
            #self.cameras.StartGrabbing()
            self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            #if search("g", cam.GetDeviceInfo().GetModelName()):
            #print(self.cam_inttime)
            #self.cameras[i].ExposureTimeAbs.SetValue(self.cam_inttime[i])
            #print("This is a GigE Cam. Set integration time accordingly")
            #if search("u", cam.GetDeviceInfo().GetModelName()):
            #self.cameras[0].ExposureTime.SetValue(self.cam_inttime[i])
            #print("This is a USB Cam. Set integration time accordingly")
            #if search("g", cam.GetDeviceInfo().GetModelName()):
                #print("This is a GigE Cam. Set integration time accordingly")
                #self.cameras[i].ExposureTimeAbs.SetValue(self.cam_inttime[i])
                #self.cameras[i].ExposureTime.SetValue(self.cam_inttime[i])
            #else:
                #print("This is a USB Cam. Set integration time accordingly")
                #self.cameras[i].ExposureTime.SetValue(self.cam_inttime[i])

    def load_integrationtime(self):
        for i, cam in enumerate(self.cameras):
            #cam.Attach(tlFactory.CreateDevice(devices[i]))
            # cam.Attach(tlFactory.CreateDevice(devices[i]))
            print("test", self.cameras[i].GetDeviceInfo().GetModelName())
            if search("g", self.cameras[i].GetDeviceInfo().GetModelName()):
                print("This is a GigE Cam. Set integration time accordingly to: ", self.cam_inttime[self.conf_indices[i]])
                self.cameras[i].ExposureTimeAbs.SetValue(self.cam_inttime[self.conf_indices[i]])
            if search("u", self.cameras[i].GetDeviceInfo().GetModelName()):
                print("This is a USB Cam. Set integration time accordingly to: ", self.cam_inttime[self.conf_indices[i]])
                self.cameras[i].ExposureTime.SetValue(self.cam_inttime[self.conf_indices[i]])
            #print("Using device ", cam.GetDeviceInfo().GetModelName(), cam.GetDeviceInfo().GetSerialNumber())
            #self.serial_numbers.append(cam.GetDeviceInfo().GetSerialNumber())


    def calc_image(self):
        self.data = np.random.rand(128,128)

    def get_live_cam(self, i):
        try:
            #self.cameras[i].ExposureTime.SetValue(10000.0);
            #self.cameras[i].ExposureTime.SetValue(self.cam_inttime[i]);
            #print("using cam: ", self.cameras[i].GetDeviceInfo().GetModelName())
            self.live_imgs[i] = self.cameras[i].RetrieveResult(5000, pylon.TimeoutHandling_ThrowException).GetArray()
            self.live_imgs_np[i] = np.float32(self.live_imgs[i])

        except (genicam.GenericException, IndexError) as e:
            # Error handling.
            print("An exception occurred with camera:",self.cameras[i].GetDeviceInfo().GetModelName())
            print("An exception occurred with camera:",self.cameras[i].GetDeviceInfo().GetSerialNumber())
            #print(e.GetDescription())
            self.reset()

    def save_frames(self):
        today = date.today().strftime("%Y%m%d")
        if today != self.today:
            self.today = today
            self.init_directories()

        for i in range(self.num_cams):
            print('sum of frame: ', sum(sum(self.live_imgs[i])), 'for threshold: ', self.rec_trs[self.conf_indices[i]], 'of camera: ',self.cam_filepath[self.conf_indices[i]])
            if sum(sum(self.live_imgs[i])) > self.rec_trs[self.conf_indices[i]] and self.flag_rec == 1:
                self.number = '{:0>4}'.format(int(self.k[i]))
                self.curdir = os.path.join(self.mainpath, str(self.today), self.cam_filepath[self.conf_indices[i]]);
                self.filename = (self.curdir + '/' + str(self.number) + self.fileformat)
                img = Image.fromarray(self.live_imgs[i])
                img.save(self.filename)
                #np.save(self.filename, self.live_imgs[i])
                self.k[i] += 1

    def loadandsave_sumofframes(self):


        for i in range(self.num_cams):
            if sum(sum(self.live_imgs[i])) > self.rec_trs[self.conf_indices[i]] and self.flag_rec == 1:
                self.camfpathloc = os.path.join(self.mainpath, str(self.today), self.cam_filepath[self.conf_indices[i]]);
                #print("self.camfpathloc: ", self.camfpathloc)
                #if self.k[i] == 1:
                #if not any(fname.endswith('.npy') for fname in self.cam_filepath[self.conf_indices[i]]('.')):
                if not glob.glob(os.path.join(self.camfpathloc,'*.npy')):
                    #print("k: ", k)
                    #print('saving sum file of camera: ',self.cam_filepath[self.conf_indices[i]])
                    self.curdir = os.path.join(self.mainpath, str(self.today), self.cam_filepath[self.conf_indices[i]])
                    #print('cam filepath: ',self.cam_filepath[self.conf_indices[i]])
                    self.number = '{:0>4}'.format(int(self.k[i]))
                    self.sumfilename = (self.curdir + '/SUM_' + str(self.number) + self.fileformatsum)
                    #savetxt(self.sumfilename, self.live_imgs[i], delimiter=',')
                    np.save(self.sumfilename, self.live_imgs_np[i])
                    #cv2.imwrite(self.sumfilename, self.live_imgs[i])

                else:
                    self.curdir = os.path.join(self.mainpath, str(self.today), self.cam_filepath[self.conf_indices[i]]);
                    self.number = '{:0>4}'.format(int(self.k[i]))
                    self.sumfilename = (self.curdir + '/SUM_' + str(self.number) + self.fileformatsum)
                    #print('Number of frames: ',self.number)
                    self.numberprev = '{:0>4}'.format(int(self.k[i]-1))
                    self.sumfilenameprev = (self.curdir + '/SUM_' + str(self.numberprev) + self.fileformatsum)
                    #print('self.sumfilenameprev: ',self.sumfilenameprev)
                    prevsum = np.load(self.sumfilenameprev)
                    self.newsum = np.add(prevsum, self.live_imgs_np[i])
                    np.save(self.sumfilename, self.newsum)
                    os.remove(self.sumfilenameprev)


    def avrg_frames(self,i):
        number = np.zeros((self.num_cams))
        kk = np.zeros((self.num_cams))
        self.cursum = self.live_imgs_np
        self.averagefromsum = self.live_imgs_np
        self.diffframe = self.live_imgs_np
        for i in range(self.num_cams):
            if sum(sum(self.live_imgs[i])) > self.rec_trs[self.conf_indices[i]] and self.flag_rec == 1:
                self.curdir = os.path.join(self.mainpath, str(self.today), self.cam_filepath[self.conf_indices[i]]);
                kk[i] = self.k[i]
                number = '{:0>4}'.format(int(kk[i]))
                self.sumframes = int(kk[i])
                sumfilename = (self.curdir + '/SUM_' + str(number) + self.fileformatsum)
                self.cursum[i] = np.load(sumfilename)
                #print('self.cursum: ', sumfilename)
    def load_ref(self):
        self.refsum = self.live_imgs_np
        self.refnoFrames = np.zeros((self.num_cams))
        for i in range(self.num_cams):
            refdaypath = os.path.join(self.mainpath, str(self.ref_day[self.conf_indices[i]]), self.cam_filepath[self.conf_indices[i]])
            #print("refdaypath", refdaypath)
            for dirpath, dirs, files in os.walk(refdaypath):
                for filename in files:
                    ffname = os.path.join(dirpath, filename)
                    if ffname.endswith('.npy'):
                        self.refsumfilename = ffname
            self.refsum[i] = np.load(self.refsumfilename)
            #print("refsumfilename", self.refsumfilename)
            refnoFrames__ = (self.refsumfilename.split('_'))
            refnoFrames_ = refnoFrames__[-1].split('.')
            self.refnoFrames[i] = int(refnoFrames_[-2])

    def reset(self):
        [cam.Close() for cam in self.cameras]
        self.load_cameras()
