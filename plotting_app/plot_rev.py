import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import plotly.express as px
import numpy as np

# Streamlit 页面标题和描述
st.title('ATR 计算与可视化')
st.write('上传你的 CSV 文件，并生成收盘价和 ATR 的时间序列线图')
import download

# Streamlit 页面标题和描述
st.title('ATR 计算与可视化')
st.write('上传你的 CSV 文件，并生成收盘价和 ATR 的时间序列线图')

# 通过 Streamlit 提供的文件上传功能上传 CSV 文件
uploaded_file = st.file_uploader("上传 CSV 文件", type=['csv'])

if uploaded_file is not None:
    try:
        
        data = pd.read_csv(uploaded_file, encoding='utf-8')
        #st.write('生成的数据:')
        #st.write(data)  # 显示生成的数据

        # 假设投資損益的欄位名稱是 'gainloss'，你需要根据具体的数据来修改该列名称
        # 获取損益金額的分位数
        percentiles = np.percentile(data['gainloss'], [10, 50, 90])

        # 创建損益金額的範圍和对应的标签
        bins = [-float('inf'), *percentiles, float('inf')]
        labels = [f'<{percentiles[0]}', f'{percentiles[0]} to {percentiles[1]}',
                  f'{percentiles[1]} to {percentiles[2]}', f'>{percentiles[2]}']

        data['GLrange'] = pd.cut(data['gainloss'], bins=bins, labels=labels)

        # 根据損益範圍进行分组统计
        grouped_data = data.groupby('GLrange').size().reset_index(name='amount')
        grouped_data1 = data.groupby('GLrange')['gainloss'].sum().reset_index(name='cumulative_sum')

        # 创建条形图
        fig1 = px.bar(grouped_data, x='GLrange', y='amount', labels={'GLrange': 'GLrange', 'amount': 'amount'}, 
                     title='投資損益 - 依照百分位數(10,50,90)統計分組筆數')
        fig2 = px.bar(grouped_data1, x='GLrange', y='cumulative_sum', labels={'GLrange': 'GLrange', 'cumulative_sum': 'cumulative_sum'}, 
                     title='投資損益 - 依照百分位數(10,50,90)統計分組損益')
        
        # 显示条形图，并在每个柱状图上显示累计值
        fig1.update_traces(text=grouped_data['amount'], textposition='outside')
        fig2.update_traces(text=grouped_data1['cumulative_sum'], textposition='outside')

        # 显示条形图
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

        # Filter data for the '<' label
        data_lt_label = data[data['GLrange'] == f'<{percentiles[0]}']

        # Displaying only the data for '<' label
        st.write("Data for '<' label:")
        st.write(data_lt_label)

    except Exception as e:
        st.write("出现了读取文件时的错误:", e)

