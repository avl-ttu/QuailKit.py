# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:45:14 2019

@author: jreznick
"""

import h5py 
import numpy as np

class JRData:
    def __init__(self,filepath, setting = 'spgram'):
        self.set = setting
        self.filepath = filepath
        self.h5File = h5py.File(self.filepath, 'r+')
        self.audioDS = self.h5File['c1/audio']
        self.spgramDS = self.h5File['c1/spgram']
        self.sizeDS = len(self.h5File['/'])
        self.scale = self.spgramDS.attrs['IntProps'][0]
        self.overlap = self.spgramDS.attrs['IntProps'][1]
        self.spgramfs = self.spgramDS.attrs["IntProps"][2]
        self.fBegin = self.spgramDS.attrs["IntProps"][3]
        self.fEnd = self.spgramDS.attrs["IntProps"][4]
        self.t0 = self.spgramDS.attrs['IntProps'][5]
        self.data = self.spgramDS.attrs['StrProps'][0]
        self.window = self.spgramDS.attrs['StrProps'][1]
        self.datetime = self.h5File['/'].attrs["props"]
        self.audiofs = self.audioDS.attrs["audiofs"][0]
        
    def __call__(self, channel, setting):
        if setting == 'spgram' and int(channel[1]) <= self.sizeDS:
            self.set = setting
            self.spgramDS = self.h5File[channel+'/'+setting]
            self.scale = self.spgramDS.attrs['IntProps'][0]
            self.overlap = self.spgramDS.attrs['IntProps'][1]
            self.spgramfs = self.spgramDS.attrs["IntProps"][2]
            self.fBegin = self.spgramDS.attrs["IntProps"][3]
            self.fEnd = self.spgramDS.attrs["IntProps"][4]
            self.data = self.spgramDS.attrs['StrProps'][0]
            self.window = self.spgramDS.attrs['StrProps'][1]
        elif setting == 'audio' and int(channel[1]) <= self.sizeDS:
            self.set = setting 
            self.audioDS = self.h5File[channel+'/audio']
        else:
            print("Can't do.")
        return self
        
    
    def __getitem__(self, interval):
        s = []
        t = []
        f = []
        if self.set == "spgram":
            startIn = int(interval[0]*self.spgramfs)
            endIn = int(interval[1]*self.spgramfs)
            startT= int(interval[0]*self.spgramfs)/self.spgramfs
            endT= int(interval[1]*self.spgramfs)/self.spgramfs

            step=1/self.spgramfs
            t = np.arange(startT,endT+0.1*step,step)
            s = self.spgramDS[:, startIn:endIn+1]
            s = np.transpose(s)

            step=(self.fEnd-self.fBegin)/1000
            f = np.arange(self.fBegin,self.fEnd+0.1*step,step)

        elif self.set == "audio":
            startIn = int(interval[0]*self.audiofs)
            endIn = int(interval[1]*self.audiofs)
            startT= int(interval[0]*self.audiofs)/self.audiofs
            endT= int(interval[1]*self.audiofs)/self.audiofs

            step=1/self.audiofs
            t = np.arange(startT,endT+0.1*step,step)
            s = self.audioDS[:, startIn:endIn+1]

        return t,s,f
    
    def close(self):
        self.h5File.close()

if __name__ == "__main__":
    DataObj = JRData("C:\\Users\\joggl\\Desktop\\Academics\\test h5\\SM304472_0+1_20181004$110000.h5")
    [t,s,f] = DataObj('c1','spgram')[1760,1800]
    print(t.shape,s.shape,f.shape)