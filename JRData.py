# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:45:14 2019

@author: jreznick
"""

import h5py 
import numpy as np
import math

class JRData:
    def __init__(self,filepath, setting = 'spgram'):
        self.set = setting
        self.filepath = filepath
        self.h5File = h5py.File(self.filepath, 'r+')
        self.audioDS = self.h5File['c1/audio']
        self.spgramDS = self.h5File['c1/spgram']
        self.sizeDS = len(self.h5File['/'])

        self.datetime = self.h5File['/'].attrs["props"]
        
    def __call__(self, channel, setting):
        if setting == 'spgram' and int(channel[1]) <= self.sizeDS:
            self.set = setting
            self.spgramDS = self.h5File[channel+'/spgram']
            self.scale = self.spgramDS.attrs['scale']
            self.overlap = self.spgramDS.attrs['overlap']
            self.fs = self.spgramDS.attrs['fs']
            self.freqs = self.spgramDS.attrs["freqs"]
            self.t0 = self.spgramDS.attrs['t0']
            self.data = self.spgramDS.attrs['data']
            self.window = self.spgramDS.attrs['window']
        elif setting == 'audio' and int(channel[1]) <= self.sizeDS:
            self.set = setting 
            self.audioDS = self.h5File[channel+'/audio']
            self.fs = self.audioDS.attrs['fs']
        else:
            print("Can't do.")
        return self
        
    
    def __getitem__(self, interval):
        s = []
        t = []
        f = []
        startIn = math.floor((interval[0]-self.t0)*self.fs)
        endIn = math.ceil((interval[1]-self.t0)*self.fs-1)
        startT= startIn/self.fs+self.t0
        endT= endIn/self.fs+self.t0
        t = np.arange(startT,endT+0.1/self.fs,1/self.fs)        
        if self.set == "spgram":
            s = self.spgramDS[:, startIn:endIn+1]
            f = np.arange(self.freqs[0],self.freqs[1]+self.freqs[2]*0.1,self.freqs[2])

        elif self.set == "audio":
            s = self.audioDS[:, startIn:endIn+1]

        return t,f,s
    
    def close(self):
        self.h5File.close()

if __name__ == "__main__":
    DataObj = JRData("C:\\Users\\joggl\\Desktop\\Academics\\test h5\\SM304472_0+1_20181004$110000.h5")
    [t,s,f] = DataObj('c1','spgram')[1760,1800]
    print(t.shape,s.shape,f.shape)