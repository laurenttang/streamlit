import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import streamlit as st
import plotly.graph_objects as go

# 通过 Streamlit 提供的文件上传功能上传 CSV 文件
uploaded_file = st.file_uploader("上传 CSV 文件", type=['csv'])

if uploaded_file is not None:
    # 读取上传的 CSV 文件
    #history_data = pd.read_csv(uploaded_file, index_col="Date", parse_dates=True)

    # 模組化 將訊號運算獨立成檔案 先運算後 吐回df供系統吃買賣訊號
    import df_test
    t1,t2=2,10
    history_data=df_test.one_df(t1,t2)
    
    #print(history_data)
    # 初始化 ===============================================================================================
    # history_data = pd.read_csv("history_data.csv", index_col="Date", parse_dates=True)

    # 設定起始資金
    cash = 100000

    # 設定各項初始參數及列表
    # 計算策略賺錢的次數
    wincounts ,wintotal , losscounts , losstotal = 0,0,0,0
    # 紀路起始資金與每次賣出後的現金數
    cashlist = [cash]
    # 買進日期及價格 # 賣出日期及價格    # 投資報酬率    # 買進賣出訊號點
    buy_date, buyprice , sell_date, sellprice, ROI , up_markers , down_markers = [],[],[],[],[],[],[]
    # 設定tick倍率 / 設定手續費 / 是否持倉，0代表沒有，1則是有持倉
    tick_price , fees ,  pos = 200,50,0

    # 資料處理邏輯 ===============================================================================================

    #globals()['sma_' + str(t1)] = talib.SMA(history_data["Close"], timeperiod=t1)
    #globals()['sma_' + str(t2)] = talib.SMA(history_data["Close"], timeperiod=t2)
    # 計算短期均線減長期均線的值
    #diff = globals()['sma_' + str(t1)] - globals()['sma_' + str(t2)]

    # 紀錄交易矩陣: return 進出場時間、價格、訊號marker、出場算ROI、
    for i in range(len(history_data["Close"])):
        if 1 < i < len(history_data["Close"]):
            
            
            # 進出場條件的控制
            condition_in = history_data["condition1"][i] and history_data["condition2"][i] and pos == 0
            condition_out = history_data["condition3"][i] and history_data["condition4"][i] and pos == 1
            
            if condition_in:
                #buy_date.append(history_data.index[i])
                buy_date.append(history_data["Date"][i])
                buyprice.append(history_data["Open"][i])

                # 開盤價-200的位置紀錄買入訊號點 (改成低點的0.95)
                up_markers.append(history_data["Low"][i]*0.95)
                # 投資報酬率及賣出點增加nan值
                ROI.append(np.nan)
                down_markers.append(np.nan)
                # 紀錄買入時的價格
                tick = history_data["Open"][i]
                # 買入後有持倉設為1
                pos = 1

            
            elif condition_out:
                sell_date.append(history_data["Date"][i])
                sellprice.append(history_data["Open"][i])
                # 買進點增加nan
                up_markers.append(np.nan)
                # 開盤價+200的位置紀錄賣出訊號點 (改成高點的1.05)
                down_markers.append(history_data["High"][i] *1.05)
                # 賣出後計算當前資金，1tick=200元，再扣掉買入及賣出各50元手續費
                cash += (history_data["Open"][i] - tick) * tick_price - 2 * fees
                # 將賣出後的現金數紀錄到cashlist列表中
                cashlist.append(cash)
                # 投資報酬率增加賣出價格減買入價格除以初始資金
                ROI.append((cashlist[-1] - cashlist[-2]) / cashlist[0])
                # 賣出後沒有持倉，將pos設為0
                pos = 0
            else:
                # 其餘情況增加nan值
                ROI.append(np.nan)
                up_markers.append(np.nan)
                down_markers.append(np.nan)
        else:
            # 其餘情況增加nan值
            ROI.append(np.nan)
            up_markers.append(np.nan)
            down_markers.append(np.nan)

    # 統計勝率 迴圈
    for i in range(len(sellprice)):
        if sellprice[i] > buyprice[i]:
            wincounts += 1
            wintotal += sellprice[i] - buyprice[i]
        else:
            losscounts += 1
            losstotal += buyprice[i] - sellprice[i]
    
    # 合併資料 for 分頁設計  
    ROI_value = [x for x in ROI if np.isnan(x) == False]
    equity = [x for x in cashlist][1:] # 取Cashlist初始值之外的序列
    d = [buy_date, buyprice, sell_date, sellprice, ROI_value,equity]
    df = pd.DataFrame(d, index=["買進日期", "買進價格", "賣出日期", "賣出價格", "投資報酬率","權益數"])
    transposed_df = df.transpose()
    history_data['up_markers']=up_markers
    history_data['down_markers']=down_markers
    history_data['ROI']=ROI

    # 分頁設計 ==========================================================================================================
    dates = history_data.index  # Assuming the index contains dates
    num_dates = len(dates)
    first_not_nan_index = next((index for index, value in enumerate(ROI) if not pd.isnull(value)), None)
    dates_per_page = min(max(60,first_not_nan_index+1),num_dates/2)  # Change this to set the number of dates per page
    num_pages = (num_dates // dates_per_page) + 1  # Calculate the total number of pages
    page_number = st.slider("Page Number", 1, num_pages, 1)  # Slider to select page number
    start_idx = (page_number - 1) * dates_per_page
    end_idx = min(page_number * dates_per_page, num_dates)

    # 繪圖 資料源開始 ===================================================================================================
    history_data_page = history_data.iloc[start_idx:end_idx]
    print(history_data_page)
    # 計算均線

    #globals()['sma_' + str(t1)] = talib.SMA(history_data_page["GSratio"], timeperiod=t1)
    #globals()['sma_' + str(t2)] = talib.SMA(history_data_page["GSratio"], timeperiod=t2)

    # panel 可以決定畫在哪個子圖
    added_plots = {
                #"SMA" + str(t1): mpf.make_addplot(globals()['sma_' + str(t1)],panel=3),
                #"SMA" + str(t2): mpf.make_addplot(globals()['sma_' + str(t2)],panel=3),
                "Buy": mpf.make_addplot(history_data_page["up_markers"], type='scatter', marker='^', markersize=10, panel=0),
                "Sell": mpf.make_addplot(history_data_page["down_markers"], type='scatter', marker='v', markersize=10, panel=0),
                "ROI": mpf.make_addplot(history_data_page["ROI"], type='scatter', panel=2)
                }
    # 設定圖表的顏色與網狀格格式
    style = mpf.make_mpf_style(marketcolors=mpf.make_marketcolors(up="r", down="g", inherit=True),
                            gridcolor="gray")
    
    
    #history_data_page.index = pd.to_datetime(history_data_page.index)
    history_data_page.index = pd.to_datetime(history_data_page["Date"])
    print(history_data_page)
    # 畫K線和均線圖
    # Set the figure size when creating the figure
    fig, axes = mpf.plot(history_data_page, type="candle", style=style,
                        addplot=list(added_plots.values()),
                        volume=True,
                        returnfig=True)
    
    #line_sma_t1 = axes.lines[0]  # Assuming the SMA line is the first line plotted
    #line_sma_t1.set_linewidth(2)
    # 設定圖例
    axes[0].legend([None] * (len(added_plots) + 2))
    handles = axes[0].get_legend().legendHandles
    axes[0].legend(handles=handles[2:], labels=list(added_plots.keys()))

    axes[0].set_ylabel("Price")
    axes[2].set_ylabel("Volume")
    axes[4].set_ylabel("ROI")
    axes[6].set_ylabel("GSratio")
    
    plt.show()

    # 显示图表在 Streamlit 页面上 ==================================================================================
    st.pyplot(fig)
    # 将结果输出到新的 CSV 文件
    st.write('交易結果:')
    st.write("最終投資報酬率:", round(sum(ROI_value),2))
    st.write("最終持有資金:", round(cash,2))
    st.write("勝率:", round(wincounts / len(sellprice)*100,2),"%")
    st.write("賺賠比:", round( wintotal * losscounts / (wincounts * losstotal) ,2))

    st.write('交易結果:')
    st.write(transposed_df)  # 显示生成的数据
    st.write('交易明細:')
    st.write(history_data)  # 显示生成的数据