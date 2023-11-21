import streamlit as st
import pandas as pd
import base64

# Creating a sample DataFrame
sample_data = {
    'srno': [1],
    'date': ['2023/11/21'],
    'stockno': [2330],
    'name': ['please clean Chinese words'],
    'tradetype': ['please clean Chinese words'],
    'amount': [1000],
    'buy_avg': [580],
    'sell_avg': [590],
    'cost': [580500],
    'gainloss': [100000],
    'return': ['2.35%']
}
sample_df = pd.DataFrame(sample_data)

# Displaying the sample DataFrame
st.write("Sample DataFrame:")
st.write(sample_df)

# Create a link for users to download the sample CSV file
def download_sample_csv():
    csv = sample_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sample_data.csv">Download Sample CSV File</a>'
    return href

st.markdown(download_sample_csv(), unsafe_allow_html=True)