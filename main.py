from JRData import JRData
import os
import plotly.plotly as plotly
import plotly.graph_objs as go
import pandas as pd
import h5py
jrdata = JRData(os.path.join('Z:',os.sep,'QuailKit','data','SM304472_0+1_20181219$100000.h5'))
jrdata('spgram1')
t, f, s = jrdata[0,10]
d = [
    go.Surface(
        x=t,
        y=f,
        z=s
    )
]
l = go.Layout(
    title='Spectrogram',
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    )
)
fig=go.Figure(data=d,layout=l)

