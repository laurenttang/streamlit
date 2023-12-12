import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def generate_random_data():
    # 生成隨機資料
    x = np.linspace(0, 10, 100)
    y = np.random.randn(100)
    return x, y

def single_axis_plot(x, y):
    # 單軸曲線圖
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig)

def dual_axis_plot(x, y1, y2):
    # 雙軸曲線圖
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'g-')
    ax2.plot(x, y2, 'b-')
    st.pyplot(fig)

def main():
    st.title('九個視圖範例')
    # 配置3列，每列顯示3個視圖
    columns = st.columns(3)
    # 產生九個視圖
    for i in range(3):
        for j in range(3):
            with columns[j]:
                st.subheader(f'視圖 {i * 3 + j + 1}')

                # 生成隨機資料
                x, y = generate_random_data()

                # 判斷是單軸或雙軸曲線圖
                if (i * 3 + j + 1) % 2 == 0:
                    dual_axis_plot(x, y, y * np.random.uniform(0.5, 2))
                else:
                    single_axis_plot(x, y)

if __name__ == '__main__':
    main()
