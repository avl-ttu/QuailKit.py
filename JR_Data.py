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
        self.spgramfs = self.spgramDS.attrs["props"][0]
        self.fBegin = self.spgramDS.attrs["props"][1]
        self.fEnd = self.spgramDS.attrs["props"][2]
        self.datetime = self.h5File['/'].attrs["props"]
        self.audiofs = self.audioDS.attrs["audiofs"][0]
        
    def __call__(self, channel, setting):
        if setting == 'spgram' and int(channel[1]) <= self.sizeDS:
            self.set = setting
            self.spgramDS = self.h5File[channel+'/'+setting]
            self.spgramfs = self.spgramDS.attrs["props"][0]
            self.fBegin = self.spgramDS.attrs["props"][1]
            self.fEnd = self.spgramDS.attrs["props"][2]
            self.scale = self.spgramDS.attrs["props"][3]
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
    DataObj = JRData("C:\\Users\\joggl\\Desktop\\Academics\\test h5\\SM304472_0+1_20181004$110000.h5",'new')
    [t,s,f] = DataObj('c1','spgram')[10,20]
    print(t.shape,s.shape,f.shape)