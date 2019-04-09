from JRData import JRData
import os
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import urllib
import scipy as sp
conn_str = (
    r'DSN=QuailKit;'
    )

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn_str)
det=pd.read_sql(
    r'SELECT data.name, detection.start_t as [start], detection.end_t as [end] '
    r'FROM detection inner join data on detection.data_id=data.stream_id',engine)

for i in range(det.shape[0]):
    jrdata = JRData(os.path.join('Z:',os.sep,'QuailKit','data',det['name'][i])) 
    fig, ax = plt.subplots(2,1)
    t, f, s = jrdata('c1','spgram')[det['start'][i],det['end'][i]]
    ax[0].pcolormesh(t,f, np.log10(s))
    t, f, s = jrdata('c1','spgram')[det['start'][i],det['end'][i]]
    ax[1].pcolormesh(t,f, np.log10(s))
    plt.show()