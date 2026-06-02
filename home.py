import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

### read excel
def read_excel(file):
    df = pd.read_excel(file)
    return df
import streamlit as st
import pandas as pd

st.title("Sales Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.write("Shape of dataset:")
    st.write(df.shape)

    st.write("Data Preview:")
    st.write(df)
st.title('Sales Data Analysis')
st.write('This is a simple Streamlit app to ' \
'analyze sales data.')
st.write("shape of the dataset")
st.write(df.shape)
st.dataframe(df.head())
