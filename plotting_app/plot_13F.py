import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_comparison_chart(companies, values_period1, values_period2, porpotions_period1, porpotions_period2,title):
    fig, ax = plt.subplots()
    bar_width = 0.3
    index = np.arange(len(companies))

    #bar1 = ax.bar(index, values_period1, bar_width, label='former')
    #bar2 = ax.bar(index + bar_width, values_period2, bar_width, label='current', alpha=0.5)
    bar1 = ax.bar(index, porpotions_period1, bar_width, label='former')
    bar2 = ax.bar(index + bar_width, porpotions_period2, bar_width, label='current', alpha=0.5)
    
    for i, (bar, prop) in enumerate(zip(bar1, porpotions_period1)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{prop:.1f}%', ha='center', va='bottom', fontsize=6)

    for i, (bar, prop) in enumerate(zip(bar2, porpotions_period2)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{prop:.1f}%', ha='center', va='bottom', fontsize=6)

    ax.set_xlabel('Company')
    #ax.set_ylabel('Value')
    ax.set_ylabel('Porpotion')
    ax.set_title(f'{title}')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(companies,fontsize=6)
    ax.legend()

    return fig

st.title('比對持股分析')

# 選擇Seaborn的配色方案
import seaborn as sns
sns.set_palette('pastel')  # 使用Seaborn的'pastel'配色方案

uploaded_file = st.file_uploader("上傳您的 CSV 檔案", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data['Company'] = data['Company'].apply(lambda x: x.split(' ')[0] if isinstance(x, str) else x)
    # 假設你有兩個不同期的持股資料
    # Filtering data for period 1 and period 2
    df_period1 = data[data['date'] == 'former'].nlargest(10, 'porpotion').sort_values('Value', ascending=False)
    df_period2 = data[data['date'] == 'current'].nlargest(10, 'porpotion').sort_values('Value', ascending=False)
    print(df_period1)
    print(df_period2)

    # 轉換資料結構，使每個公司的數值分開
    companies = np.union1d(df_period1['Company'], df_period2['Company'])
    remaining_companies = set(companies) - set(df_period2['Company'])
    companies = list(df_period2['Company']) + list(remaining_companies)
    #companies = [ name.split(' ')[0] for name in companies]
    print(companies)

    values_period1 = [df_period1[df_period1['Company'] == company]['Value'].values[0] if company in df_period1['Company'].values else 0 for company in companies]
    values_period2 = [df_period2[df_period2['Company'] == company]['Value'].values[0] if company in df_period2['Company'].values else 0 for company in companies]
    porpotions_period1 = [df_period1[df_period1['Company'] == company]['porpotion'].values[0] if company in df_period1['Company'].values else 0 for company in companies]
    porpotions_period2 = [df_period2[df_period2['Company'] == company]['porpotion'].values[0] if company in df_period2['Company'].values else 0 for company in companies]

    # 在Streamlit中顯示圖表
    st.title('比對持股分析')

    # 分別繪製兩期持股的兩張圖表
    fig1 = plot_comparison_chart(companies, values_period1, values_period2, porpotions_period1, porpotions_period2,'Changes in Top 10 holdings')
    st.pyplot(fig1)
    
    # 假設你有兩個不同期的持股資料
    #data_period1 = {'Company': ['P', 'Q', 'R', 'S', 'T'],
    #                'Value': [1000, 800, 600, 500, 400],
    #                'porpotion': [3.73, 0.12, 0, .71, 0.9]}
    #data_period2 = {'Company': ['P', 'Q', 'R', 'W', 'Z'],
    #                'Value': [1200, 750, 700, 600, 450],
    #                'porpotion': [1.3, 1.2, 1, 0.71, 0.9]}
    df_period3 = data[data['date'] == 'former'].nsmallest(10, 'porpotion').sort_values('Value', ascending=False)
    df_period4 = data[data['date'] == 'current'].nsmallest(10, 'porpotion').sort_values('Value', ascending=False)
    print(df_period3)
    print(df_period4)
    # 轉換資料結構，使每個公司的數值分開
    companies = np.union1d(df_period3['Company'], df_period4['Company'])
    remaining_companies = set(companies) - set(df_period4['Company'])
    companies = list(df_period4['Company']) + list(remaining_companies)
    print(companies)

    
    values_period3 = [df_period3[df_period3['Company'] == company]['Value'].values[0] if company in df_period3['Company'].values else 0 for company in companies]
    values_period4 = [df_period4[df_period4['Company'] == company]['Value'].values[0] if company in df_period4['Company'].values else 0 for company in companies]
    porpotions_period3 = [df_period3[df_period3['Company'] == company]['porpotion'].values[0] if company in df_period3['Company'].values else 0 for company in companies]
    porpotions_period4 = [df_period4[df_period4['Company'] == company]['porpotion'].values[0] if company in df_period4['Company'].values else 0 for company in companies]

    fig2 = plot_comparison_chart(companies, values_period3, values_period4, porpotions_period3, porpotions_period4,'Changes in last 10 holdings')  # 修改成第二張圖的資料
    st.pyplot(fig2)
    
