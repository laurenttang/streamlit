import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

# Streamlit 页面标题和描述
st.title('ATR 计算与可视化')
st.write('上传你的 CSV 文件，并生成收盘价和 ATR 的时间序列线图')

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

    # 设置 ATR 计算的时间周期
    time_period = 14

    # 计算 ATR
    data['ATR'] = data['TrueRange'].rolling(window=time_period).mean().apply(lambda x :round(x,2))
    data['MaxTR'] = data['TrueRange'].rolling(window=time_period).max().apply(lambda x :round(x,2))
    data['MaxATR'] = round((data['ATR']+data['MaxTR'])/2,2)
    data['MinTR'] = data['TrueRange'].rolling(window=time_period).min().apply(lambda x :round(x,2))
    # Convert 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

    # 创建图表和子图网格
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])  # 两个子图，高度比例为2:1

    # 第一个子图：Close Price
    ax1 = plt.subplot(gs[0])
    ax1.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    ax1.set_ylabel('Close Price', color='blue')
    ax1.legend(loc='upper left')  # 添加图例

    # 第二个子图：ATR 和 True Range
    ax2 = plt.subplot(gs[1], sharex=ax1)  # 共享x轴
    ax2.plot(data['Date'], data['ATR'], label='ATR', color='red', linestyle='--')
    ax2.plot(data['Date'], data['MaxATR'], label='30% chance', color='yellow', linestyle='--')
    ax2.plot(data['Date'], data['MaxTR'], label='maxTR', color='orange', linestyle='--')
    ax2.plot(data['Date'], data['MinTR'], label='minTR', color='blue', linestyle='--')
    ax2.set_ylabel('ATR and TR', color='black')
    ax2.set_xlabel('Time')
    ax2.legend(loc='upper left')  # 添加图例
    # 在每条线的最后一个数据点上添加注释
    for series in [data['ATR'], data['MaxATR'], data['MaxTR'], data['MinTR']]:
        ax2.annotate(str(series.iloc[-1]), xy=(mdates.date2num(data['Date'].iloc[-1]), series.iloc[-1]),
                    xytext=(0, -5), textcoords='offset points')
        
    # 设置 x 轴的日期格式为 'YYYYMMDD'
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))

    plt.tight_layout()
    plt.show()

    # 显示图表在 Streamlit 页面上
    st.pyplot(fig)
    

    # 将结果输出到新的 CSV 文件
    st.write('生成的数据:')
    st.write(data)  # 显示生成的数据
