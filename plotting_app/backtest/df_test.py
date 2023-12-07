import pandas as pd
import talib

def one_df():

    df=pd.read_csv('history_data.csv')
    df['GSratio']=df['Close_gc']/df['Close']
    df['5MA']=talib.SMA(df["GSratio"], timeperiod=5)
    df['10MA']=talib.SMA(df["GSratio"], timeperiod=10)
    df['diff']=df['5MA']-df['10MA']
    df['condition1']=df['diff']>0
    df['condition2']=df['diff'].shift(1)<0
    df['condition3']=df['diff']<0
    df['condition4']=df['diff'].shift(1)>0

    #df['5MAasc']=df['5MA'].gt(df['5MA'].shift(-1))
    print(df.head(20))

    return df
