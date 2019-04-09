import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import os
import urllib
conn_str = (
    r'DSN=QuailKit;'
    )

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn_str)

li=os.listdir(r'Z:\QuailKit\log')
for f in li:
    n=str.split(f,'_')[0]
    f='Z:\\QuailKit\\log\\' + f
    df = pd.read_csv(f);
    df.rename(columns={'Unnamed: 3':'NS','Unnamed: 5':'EW','TEMP(C)':'temperature'},inplace=True)
    df=df[['DATE','TIME','LAT','LON','NS','EW','temperature']]
    df['node_id']=n
    df.to_sql('node_log',engine,index=False,if_exists='append')

# write to sql table... pandas will use default column names and dtypes
#df.to_sql('table_name',engine,index=True,index_label='id')