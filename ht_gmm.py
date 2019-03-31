from JR_Data import JRData
import os
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import urllib
from sklearn import mixture
conn_str = (
    r'DSN=QuailKit;'
    )

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn_str)
det=pd.read_sql(
    r'SELECT [name], DATEDIFF(millisecond,an.[start], detection.[start])/1000.0 as [start], DATEDIFF(millisecond,an.[start], detection.[end])/1000.0 as [end] '
    r'FROM detection inner join data on detection.data_id=data.stream_id inner join audio_data ad on detection.data_id=ad.data_id inner join audio_node an on ad.audio_id=an.audio_id '
    r'WHERE DATEDIFF(millisecond,an.[start], detection.[start])/1000.0>240',engine)

# for i in range(det.shape[0]):
i=0
jrdata = JRData(os.path.join('Z:',os.sep,'QuailKit','data',det['name'][i])) 
fig, ax = plt.subplots(2,1)
t, f, s = jrdata('c1','spgram1')[det['start'][i]-1,det['end'][i]+1]
ax[0].pcolormesh(t,f, s)
t, f, s = jrdata('c1','spgram1')[det['start'][i]-1,det['end'][i]+1]
ax[1].pcolormesh(t,f, s)
model=mixture.GaussianMixture(2)
ss=model.fit_predict(s)

plt.show()