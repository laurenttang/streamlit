import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from mplfinance.original_flavor import candlestick_ohlc
# Streamlit 页面标题和描述
st.title('ATR計算與視覺化')
# ======================================================= download ==========
import base64
# Creating a sample DataFrame
sample_data = {'Date': ['20230703'],'Open': [673],'High': [709],'Low': [673],'Close': [709]}
sample_df = pd.DataFrame(sample_data)
# Displaying the sample DataFrame
st.write("""
         輸入限csv檔，內文、檔名不可包含中文，日期可吃 20231122 or 2023/11/22:
         \n=> 可從統一金贏島輸出EXCEL後，將數值貼到下載之範例檔再上傳
         """)
st.write(sample_df)

# Create a link for users to download the sample CSV file
def download_sample_csv():
    csv = sample_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sample_data.csv">Download Sample CSV File</a>'
    return href
st.markdown(download_sample_csv(), unsafe_allow_html=True)
# ======================================================= END ==========
st.write('上傳您的CSV文件，並產生收盤價和ATR的時間序列線圖')


# 通过 Streamlit 提供的文件上传功能上传 CSV 文件
uploaded_file = st.file_uploader("上传 CSV 文件", type=['csv'])

if uploaded_file is not None:
    # 读取上传的 CSV 文件
    data = pd.read_csv(uploaded_file)

    # 计算 True Range
    data['TrueRange1'] = data['High'] - data['Low']
    data['TrueRange2'] = abs(data['High'] - data['Close'].shift(1))
    data['TrueRange3'] = abs(data['Low'] - data['Close'].shift(1))
    data['TrueRange'] = data[['TrueRange1', 'TrueRange2', 'TrueRange3']].max(axis=1)

    # 创建两列布局
    left_column, right_column = st.columns([3, 1])

    # 在右列创建侧边栏滑动条
    with right_column:
        time_period = st.slider('选择ATR计算的时间周期', 1, 20, 8)

    # 计算 ATR
    data['ATR'] = data['TrueRange'].rolling(window=time_period).mean().apply(lambda x :round(x,2))
    data['MaxTR'] = data['TrueRange'].rolling(window=time_period).max().apply(lambda x :round(x,2))
    data['MaxATR'] = round((data['ATR']+data['MaxTR'])/2,2)
    data['MinTR'] = data['TrueRange'].rolling(window=time_period).min().apply(lambda x :round(x,2))
    data['MinATR'] = round((data['ATR']+data['MinTR'])/2,2)
    if isinstance(data['Date'].iloc[0], str) and '/' in data['Date'].iloc[0]:
        data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
    else:
        data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
    # data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

    # 创建图表和子图网格
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])  # 两个子图，高度比例为2:1

    # 第一个子图：Candlestick Chart
    ax1 = plt.subplot(gs[0])
    candlestick_ohlc(ax1, zip(mdates.date2num(data['Date']), data['Open'], data['High'], data['Low'], data['Close']), width=0.6,colorup='red', colordown='green')
    ax1.set_ylabel('Price')
    ax1.legend(['Candlestick'], loc='upper left')  # 添加图例

    # 第二个子图：ATR 和 True Range
    ax2 = plt.subplot(gs[1], sharex=ax1)  # 共享x轴
    ax2.plot(data['Date'], data['ATR'], label='ATR', color='red', linestyle='--')
    ax2.plot(data['Date'], data['MaxATR'], label='30% chance', color='pink', linestyle='--')
    ax2.plot(data['Date'], data['MaxTR'], label='maxTR', color='orange', linestyle='--')
    ax2.plot(data['Date'], data['MinATR'], label='70% chance', color='green', linestyle='--')
    ax2.plot(data['Date'], data['MinTR'], label='minTR', color='blue', linestyle='--')
    ax2.set_ylabel('ATR and TR', color='black')
    ax2.set_xlabel('Time')
    ax2.legend(loc='upper left')  # 添加图例
    # 在每条线的最后一个数据点上添加注释
    for series in [data['ATR'], data['MaxATR'], data['MaxTR'], data['MinATR'], data['MinTR']]:
        ax2.annotate(str(series.iloc[-1]), xy=(mdates.date2num(data['Date'].iloc[-1]), series.iloc[-1]),
                    xytext=(0, -5), textcoords='offset points')
        
    # 设置 x 轴的日期格式为 'YYYYMMDD'
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))

    plt.tight_layout()
    plt.show()

    # 显示图表在 Streamlit 页面上
    st.pyplot(fig)
    

    # 将结果输出到新的 CSV 文件
    st.write('輸入的數據:')
    st.write(data)  # 显示生成的数据
else:
    
    #import streamlit as st
    #import os

    # Everything is accessible via the st.secrets dict:
    #st.write("DB username:", st.secrets["db_username"])
    #st.write("DB password:", st.secrets["db_password"])
    

    # And the root-level secrets are also accessible as environment variables:
    #st.write(
    #    "Has environment variables been set:",
    #    os.environ["db_username"] == st.secrets["db_username"],
    #)
    
    import pymysql
    from sqlalchemy import create_engine

    # 读取上传的 CSV 文件
    username=st.secrets["db_username"]
    password=st.secrets["db_password"]
    engine=create_engine(f'mysql+pymysql://{username}:{password}@103.17.9.213:3306/pricedata_day?charset=utf8')
    sql=f" select * from pricedata_day.twse order by Date desc limit 55"
    data = pd.read_sql(sql, engine)
    data.sort_values(by='Date', ascending=True, inplace=True)

    #data = pd.read_csv(uploaded_file)

    # 计算 True Range
    data['TrueRange1'] = data['High'] - data['Low']
    data['TrueRange2'] = abs(data['High'] - data['Close'].shift(1))
    data['TrueRange3'] = abs(data['Low'] - data['Close'].shift(1))
    data['TrueRange'] = data[['TrueRange1', 'TrueRange2', 'TrueRange3']].max(axis=1)

    # 创建两列布局
    left_column, right_column = st.columns([3, 1])

    # 在右列创建侧边栏滑动条
    with right_column:
        time_period = st.slider('选择ATR计算的时间周期', 1, 20, 8)

    # 计算 ATR
    data['ATR'] = data['TrueRange'].rolling(window=time_period).mean().apply(lambda x :round(x,2))
    data['MaxTR'] = data['TrueRange'].rolling(window=time_period).max().apply(lambda x :round(x,2))
    data['MaxATR'] = round((data['ATR']+data['MaxTR'])/2,2)
    data['MinTR'] = data['TrueRange'].rolling(window=time_period).min().apply(lambda x :round(x,2))
    data['MinATR'] = round((data['ATR']+data['MinTR'])/2,2)
    if isinstance(data['Date'].iloc[0], str) and '/' in data['Date'].iloc[0]:
        data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
    else:
        data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
    # data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

    # 创建图表和子图网格
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])  # 两个子图，高度比例为2:1

    # 第一个子图：Candlestick Chart
    ax1 = plt.subplot(gs[0])
    candlestick_ohlc(ax1, zip(mdates.date2num(data['Date']), data['Open'], data['High'], data['Low'], data['Close']), width=0.6,colorup='red', colordown='green')
    ax1.set_ylabel('Price')
    ax1.legend(['Candlestick'], loc='upper left')  # 添加图例

    # 第二个子图：ATR 和 True Range
    ax2 = plt.subplot(gs[1], sharex=ax1)  # 共享x轴
    ax2.plot(data['Date'], data['ATR'], label='ATR', color='red', linestyle='--')
    ax2.plot(data['Date'], data['MaxATR'], label='30% chance', color='pink', linestyle='--')
    ax2.plot(data['Date'], data['MaxTR'], label='maxTR', color='orange', linestyle='--')
    ax2.plot(data['Date'], data['MinATR'], label='70% chance', color='green', linestyle='--')
    ax2.plot(data['Date'], data['MinTR'], label='minTR', color='blue', linestyle='--')
    ax2.set_ylabel('ATR and TR', color='black')
    ax2.set_xlabel('Time')
    ax2.legend(loc='upper left')  # 添加图例
    # 在每条线的最后一个数据点上添加注释
    for series in [data['ATR'], data['MaxATR'], data['MaxTR'], data['MinATR'], data['MinTR']]:
        ax2.annotate(str(series.iloc[-1]), xy=(mdates.date2num(data['Date'].iloc[-1]), series.iloc[-1]),
                    xytext=(0, -5), textcoords='offset points')
        
    # 设置 x 轴的日期格式为 'YYYYMMDD'
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))

    plt.tight_layout()
    plt.show()

    # 显示图表在 Streamlit 页面上
    st.pyplot(fig)
    

    # 将结果输出到新的 CSV 文件
    st.write('輸入的數據:')
    st.write(data)  # 显示生成的数据