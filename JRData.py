# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:45:14 2019

@author: jreznick
"""

import scipy.io as sio
import h5py 
import numpy as np

class JRData:
    def __init__(self,filepath, setting = 'spgram'):
        #Loading in data from .mat file
        self.set = setting
        self.filepath = filepath
        self.h5File = h5py.File(self.filepath,'r')
        self.audioDS = self.h5File['audio']
        self.spgramDS = self.h5File['spgrams/spgram1']
        self.sizeDS = len(self.h5File['spgrams'])
        self.spgramfs = self.spgramDS.attrs["props"][0]
        self.finalTimeSpgram = self.spgramDS.attrs["props"][1]
        self.fBegin = self.spgramDS.attrs["props"][2]
        self.fEnd = self.spgramDS.attrs["props"][3]
        self.scale = self.spgramDS.attrs["props"][4]
        self.audiofs = self.audioDS.attrs["audiofs"][0]
        
    def __call__(self, setting):
        if setting[0:6] == 'spgram' and int(setting[6]) <= self.sizeDS:
            self.set = setting[0:6]
            self.spgramDS = self.h5File['spgrams/'+setting]
            self.spgramfs = self.spgramDS.attrs["props"][0]
            self.finalTimeSpgram = self.spgramDS.attrs["props"][1]
            self.fBegin = self.spgramDS.attrs["props"][2]
            self.fEnd = self.spgramDS.attrs["props"][3]
            self.scale = self.spgramDS.attrs["props"][4]
        elif setting == 'audio':
            self.set = setting
        else:
            print("Can't do.")
        return self
    
    def __getitem__(self, index):
        s = []
        t = []
        if self.set == "spgram":
            startIn = int(index[0]/(1/self.spgramfs))
            endIn = int(index[1]/(1/self.spgramfs) - startIn -1)
            t = self.spgramDS[0,startIn:endIn]
            s = self.spgramDS[1:, startIn:endIn]
            f = np.arange(self.fBegin,self.fEnd+self.spgramfs,self.spgramfs)
            return t, f, s
        elif self.set == "audio":
            startIn = int(index[0]/(1/self.audiofs))
            endIn = int(index[1]/(1/self.audiofs) - startIn - 1)
            t = self.audioDS[0,startIn:endIn]
            s = self.audioDS[1:, startIn:endIn]
            return t, s
    
    def close(self):
        self.h5File.close()

# DataObj = JRData("","SM304472_0+1_20181219$100000")

# #Long way
# DataObj('audio')
# t,s = DataObj[0,10]
# print(1)
# #Short hand
# t,s = DataObj('audio')[0,10]
# print(2)
# #Meaning, If I wanted to do a proccess over the spectrogram, I could do this
# DataObj('spgram1')
# for i in range(0,10):
#     t, f, s = DataObj[0,10]
# print(3)
# #And it doesn't require me to do the short hand. It essentially sets which one
# # to work with when "DataObj('spgram')" is stated.
# DataObj.close()