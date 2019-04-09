from JR_Data import JRData
import os
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pandas as pd
import h5py
import numpy as np
jrdata = JRData(os.path.join('Z:',os.sep,'QuailKit','data','SM304472_0+1_20181219$100000.h5'))
jrdata('c1','spgram')
t, s, f= jrdata[120,130]
fig = plt.figure()
plt.pcolormesh(t,f, s)
plt.show()
