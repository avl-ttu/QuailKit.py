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
        if setting != 'new':
            self.h5File = h5py.File(self.filepath, 'r+')
            self.audioDS = self.h5File['c1/audio']
            self.spgramDS = self.h5File['c1/spgram']
            self.sizeDS = len(self.h5File['/'])
            self.spgramfs = self.spgramDS.attrs["props"][0]
            self.fBegin = self.spgramDS.attrs["props"][1]
            self.fEnd = self.spgramDS.attrs["props"][2]
            self.scale = self.spgramDS.attrs["props"][3]
            self.datetime = self.h5File['/'].attrs["props"]
            self.audiofs = self.audioDS.attrs["audiofs"][0]
        else:
            self.set = setting
            self.h5File = h5py.File(self.filepath, 'w')
        
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
    DataObj = JRData("C:\\Users\\jreznick\\Texas Tech University\\Quail Call - Joel\\FakeSQLServer\\thing.h5",'new')
   
