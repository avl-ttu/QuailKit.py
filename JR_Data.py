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
        self.h5File = h5py.File(self.filepath,'r')
        self.audioDS = self.h5File['c1/audio']
        self.spgramDS = self.h5File['c1/spgram']
        self.sizeDS = len(self.h5File['/'])
        self.spgramfs = self.spgramDS.attrs["props"][0]
        self.finalTimeSpgram = self.spgramDS.attrs["props"][1]
        self.fBegin = self.spgramDS.attrs["props"][2]
        self.fEnd = self.spgramDS.attrs["props"][3]
        self.scale = self.spgramDS.attrs["props"][4]
        self.datetime = self.h5File['/'].attrs["props"]
        self.audiofs = self.audioDS.attrs["audiofs"][0]
        
    def __call__(self, channel, setting):
        if setting == 'spgram' and int(channel[1]) <= self.sizeDS:
            self.set = setting
            self.spgramDS = self.h5File[channel+'/'+setting]
            self.spgramfs = self.spgramDS.attrs["props"][0]
            self.finalTimeSpgram = self.spgramDS.attrs["props"][1]
            self.fBegin = self.spgramDS.attrs["props"][2]
            self.fEnd = self.spgramDS.attrs["props"][3]
            self.scale = self.spgramDS.attrs["props"][4]
        elif setting == 'audio' and int(channel[1]) <= self.sizeDS:
            self.set = setting 
            self.audioDS = self.h5File[channel+'/audio']
        else:
            print("Can't do.")
        return self
        
    
    def __getitem__(self, interval):
        s = []
        t = []
        if self.set == "spgram":
            startIn = int(interval[0]*self.spgramfs)
            endIn = int(interval[1]*self.spgramfs)
            step=1/self.spgramfs
            t = np.arange(interval[0],interval[1],step)
            s = self.spgramDS[:, startIn:endIn]
            step=(self.fEnd-self.fBegin)/1000
            f = np.arange(self.fBegin,self.fEnd+1,step)
            return t, f, s
        elif self.set == "audio":
            startIn = int(interval[0]/(1/self.audiofs))
            endIn = int(interval[1]/(1/self.audiofs) - startIn)
            step = 1/self.audiofs
            t = np.arange(interval[0],interval[1],step)
            s = self.audioDS[:, startIn:endIn]
            return t, s
    
    def close(self):
        self.h5File.close()

if __name__ == "__main__":
    DataObj = JRData("C:\\Users\\joggl\\Texas Tech University\\Quail Call - Joel\\QuailKit\\JR_QuailKit\\SM304472_0+1_20181219$100000.h5")
    # #Long way
    DataObj('c2','spgram')
    t,f,s = DataObj[0,100]
    print(t.shape,f.shape, s.shape)
    print(1)
    #Short hand
    t,s = DataObj('audio')[0,10]
    print(2)
    #Meaning, If I wanted to do a proccess over the spectrogram, I could do this
    DataObj('spgram1')
    for i in range(0,10):
        t, f, s = DataObj[0,10]
    print(3)
    #And it doesn't require me to do the short hand. It essentially sets which one
    # to work with when "DataObj('spgram')" is stated.
    DataObj.close()