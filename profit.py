import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Profit Analysis",
    layout="wide"
)

@st.cache_data
def read_excel(file):
    df = pd.read_excel(file)
    return df
df = pd.read_excel('data\sales.xls')

df.columns = df.columns.str.strip()

if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)

st.title("Profit Analysis Dashboard")

st.write(
    "This dashboard analyzes profit performance "
    "across categories, regions, and time."
)

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    if "Category" in df.columns:
        selected_category = st.multiselect(
            "Select Category",
            options=df["Category"].dropna().unique(),
            default=df["Category"].dropna().unique()
        )

with col2:
    if "Region" in df.columns:
        selected_region = st.multiselect(
            "Select Region",
            options=df["Region"].dropna().unique(),
            default=df["Region"].dropna().unique()
        )

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_category)
]

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_region)
]

st.subheader("Key Profit Metrics")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Total Profit",
        f"{filtered_df['Profit'].sum():,.2f}"
    )

with kpi2:
    st.metric(
        "Average Profit",
        f"{filtered_df['Profit'].mean():,.2f}"
    )

with kpi3:
    st.metric(
        "Maximum Profit",
        f"{filtered_df['Profit'].max():,.2f}"
    )


st.subheader("Category Wise Profit")

category_profit = filtered_df.groupby(
    "Category",
    as_index=False
)["Profit"].sum()

fig1 = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Category",
    text_auto=True,
    title="Category Wise Profit"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Sub-Category Wise Profit")

sub_profit = filtered_df.groupby(
    "Sub-Category",
    as_index=False
)["Profit"].sum()

fig2 = px.bar(
    sub_profit,
    x="Sub-Category",
    y="Profit",
    color="Sub-Category",
    text_auto=True,
    title="Sub-Category Wise Profit"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Region Wise Profit")

region_profit = filtered_df.groupby(
    "Region",
    as_index=False
)["Profit"].sum()

fig3 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Region Wise Profit Share"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Monthly Profit Trend")

monthly_profit = filtered_df.groupby(
    "Year Month",
    as_index=False
)["Profit"].sum()

fig4 = px.line(
    monthly_profit,
    x="Year Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Discount vs Profit")

fig5 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    title="Discount vs Profit"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("Profit Summary Table")

summary_table = filtered_df.groupby(
    ["Category", "Sub-Category"],
    as_index=False
).agg({
    "Profit": "sum",
    "Sales": "sum",
    "Quantity": "sum"
})

st.dataframe(summary_table, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Profit Data",
    data=csv,
    file_name="profit_analysis.csv",
    mime="text/csv"
)