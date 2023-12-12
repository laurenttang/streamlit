import pandas as pd

def one_df(ma_s,ma_l):

    df=pd.read_csv('history_data.csv')
    df['GSratio']=df['Close_gc']/df['Close']
    df['5MA']=df["GSratio"].rolling(window=ma_s).mean()
    df['10MA']=df["GSratio"].rolling(window=ma_l).mean()
    df['diff']=df['5MA']-df['10MA']
    df['condition1']=df['diff']<0
    df['condition2']=df['diff'].shift(1)>0
    df['condition3']=df['diff']>0
    df['condition4']=df['diff'].shift(1)<0

    #df['5MAasc']=df['5MA'].gt(df['5MA'].shift(-1))
    print(df.head(20))

    return df
'''
a=one_df()
for i in range(len(a["Close"])):
    print(a["condition1"][i],a["condition2"][i],a["condition1"][i] and a["condition2"][i])
'''