import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    data['ATR'] = data['TrueRange'].rolling(window=time_period).mean()

    # 创建图表
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制收盘价到第一个轴
    ax1.plot(data['Close'], label='Close Price', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Close Price', color='blue')

    # 创建第二个轴用于 ATR
    ax2 = ax1.twinx()
    ax2.plot(data['ATR'], label='ATR', color='red', linestyle='--')
    ax2.set_ylabel('ATR', color='red')

    # 添加图例
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    lines = lines_1 + lines_2
    labels = labels_1 + labels_2
    ax1.legend(lines, labels, loc='upper left')

    # 显示图表在 Streamlit 页面上
    st.pyplot(fig)

    # 将结果输出到新的 CSV 文件
    st.write('生成的数据:')
    st.write(data)  # 显示生成的数据
