import streamlit as st
import pandas as pd

df = pd.read_excel('sales.xls')

st.title('Sales Data Analysis')
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose view", ["Home", "Data"])

st.write('This is a simple Streamlit app to analyze sales data.')
st.write("shape of the dataset")
st.write(df.shape)

st.dataframe(df.head())
