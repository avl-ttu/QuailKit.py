from JRData import JRData
import os
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pandas as pd
import h5py
import numpy as np
jrdata = JRData(os.path.join('Z:',os.sep,'QuailKit','data','SM304472_0+1_20181219$100000.h5'))
jrdata('c1','spgram')
t, f, s = jrdata[0,200]
fig = plt.figure()
plt.pcolormesh(t,f, s)
plt.show()
