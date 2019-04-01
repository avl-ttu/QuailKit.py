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
from sklearn import preprocessing
from scipy import stats
conn_str = (
    r'DSN=QuailKit;'
    )

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn_str)
det=pd.read_sql(
    r'SELECT [name], DATEDIFF(millisecond,an.[start], detection.[start])/1000.0 as [start], DATEDIFF(millisecond,an.[start], detection.[end])/1000.0 as [end] '
    r'FROM detection inner join data on detection.data_id=data.stream_id inner join audio_data ad on detection.data_id=ad.data_id inner join audio_node an on ad.audio_id=an.audio_id '
    r'WHERE DATEDIFF(millisecond,an.[start], detection.[start])/1000.0>120',engine)

for i in range(det.shape[0]):
    jrdata = JRData(os.path.join('Z:',os.sep,'QuailKit','data',det['name'][i])) 
    fig, ax = plt.subplots(2,1)
    t, s, f = jrdata('c1','spgram')[det['start'][i]-1,det['end'][i]+1]
    ax[0].pcolormesh(t, f, s)
    model=mixture.GaussianMixture(2)
    g=np.stack((np.tile(t[None,:],[len(f),1]),np.tile(f[:,None],[1,len(t)]),s),axis=2)
    ng=preprocessing.normalize(np.reshape(g,(len(f)*len(t),3)),axis=0)
    ss=model.fit_predict(ng)
    ax[1].pcolormesh(t,f, np.reshape(ss,(s.shape[0],-1)))
    plt.show()