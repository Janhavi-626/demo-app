import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Region Analysis",
    layout="wide"
)

@st.cache_data
def read_excel(file):
    df = pd.read_excel(file)
    return df

df = pd.read_excel(r'data\sales.xls')

df.columns = df.columns.str.strip()

if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Year"] = df["Order Date"].dt.year
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)

# -----------------------------
# Title
# -----------------------------
st.title("Region Analysis Dashboard")

st.write(
    "This dashboard analyzes sales and profit "
    "performance across regions."
)


st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    selected_region = st.multiselect(
        "Select Region",
        options=df["Region"].dropna().unique(),
        default=df["Region"].dropna().unique()
    )

with col2:
    selected_category = st.multiselect(
        "Select Category",
        options=df["Category"].dropna().unique(),
        default=df["Category"].dropna().unique()
    )

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_region)
]

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_category)
]

st.subheader("Region KPIs")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Total Sales",
        f"{filtered_df['Sales'].sum():,.2f}"
    )

with kpi2:
    st.metric(
        "Total Profit",
        f"{filtered_df['Profit'].sum():,.2f}"
    )

with kpi3:
    st.metric(
        "Total Quantity",
        int(filtered_df["Quantity"].sum())
    )

st.subheader("Region Wise Sales")

region_sales = filtered_df.groupby(
    "Region",
    as_index=False
)["Sales"].sum()

fig1 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    text_auto=True,
    title="Region Wise Sales"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Region Wise Profit")

region_profit = filtered_df.groupby(
    "Region",
    as_index=False
)["Profit"].sum()

fig2 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Region",
    text_auto=True,
    title="Region Wise Profit"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Region Wise Quantity")

region_quantity = filtered_df.groupby(
    "Region",
    as_index=False
)["Quantity"].sum()

fig3 = px.pie(
    region_quantity,
    names="Region",
    values="Quantity",
    title="Region Wise Quantity Share"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Monthly Region Sales Trend")

region_trend = filtered_df.groupby(
    ["Year Month", "Region"],
    as_index=False
)["Sales"].sum()

fig4 = px.line(
    region_trend,
    x="Year Month",
    y="Sales",
    color="Region",
    markers=True,
    title="Monthly Region Sales Trend"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Segment Wise Regional Sales")

segment_region = filtered_df.groupby(
    ["Region", "Segment"],
    as_index=False
)["Sales"].sum()

fig5 = px.bar(
    segment_region,
    x="Region",
    y="Sales",
    color="Segment",
    barmode="group",
    title="Segment Wise Regional Sales"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("Region Summary Table")

summary_table = filtered_df.groupby(
    "Region",
    as_index=False
).agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum",
    "Order ID": "nunique"
})

summary_table = summary_table.rename(
    columns={"Order ID": "Total Orders"}
)

st.dataframe(summary_table, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Region Data",
    data=csv,
    file_name="region_analysis.csv",
    mime="text/csv"
)