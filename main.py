# Interactive Dashboard Development
# Sales & Performance Dashboard using Streamlit
# Author: Gopika J

# -----------------------------------
# IMPORT LIBRARIES
# -----------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Business Performance Dashboard",
    layout="wide"
)

st.title("📊 Interactive Business Dashboard")

# -----------------------------------
# LOAD DATA
# -----------------------------------

# Replace with your dataset
data = pd.read_csv("business_data.csv")

# Display raw data
if st.checkbox("Show Raw Data"):
    st.write(data)

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("Filter Data")

regions = st.sidebar.multiselect(
    "Select Region",
    options=data['Region'].unique(),
    default=data['Region'].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

# Apply filters
filtered_data = data[
    (data['Region'].isin(regions)) &
    (data['Category'].isin(categories))
]

# -----------------------------------
# KPI METRICS
# -----------------------------------

total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
avg_sales = filtered_data['Sales'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Average Sales", f"₹{avg_sales:,.2f}")

st.markdown("---")

# -----------------------------------
# SALES BY REGION
# -----------------------------------

sales_region = filtered_data.groupby('Region')['Sales'].sum().reset_index()

fig1 = px.bar(
    sales_region,
    x='Region',
    y='Sales',
    title='Sales by Region',
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------
# SALES TREND OVER TIME
# -----------------------------------

filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])

sales_trend = filtered_data.groupby('Date')['Sales'].sum().reset_index()

fig2 = px.line(
    sales_trend,
    x='Date',
    y='Sales',
    title='Sales Trend Over Time'
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# CATEGORY PERFORMANCE
# -----------------------------------

category_sales = filtered_data.groupby('Category')['Sales'].sum().reset_index()

fig3 = px.pie(
    category_sales,
    names='Category',
    values='Sales',
    title='Category Contribution'
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------
# PROFIT VS SALES
# -----------------------------------

fig4 = px.scatter(
    filtered_data,
    x='Sales',
    y='Profit',
    color='Region',
    size='Sales',
    hover_data=['Category'],
    title='Profit vs Sales Analysis'
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------
# TOP PRODUCTS
# -----------------------------------

top_products = (
    filtered_data.groupby('Product')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x='Product',
    y='Sales',
    title='Top 10 Products',
    text_auto=True
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------
# ACTIONABLE INSIGHTS
# -----------------------------------

st.subheader("📌 Actionable Insights")

best_region = sales_region.sort_values(
    by='Sales',
    ascending=False
).iloc[0]['Region']

best_category = category_sales.sort_values(
    by='Sales',
    ascending=False
).iloc[0]['Category']

st.write(f"✅ Highest performing region: **{best_region}**")
st.write(f"✅ Best selling category: **{best_category}**")
st.write("✅ Focus marketing efforts on high-performing regions.")
st.write("✅ Improve inventory for top-selling products.")
st.write("✅ Analyze low-performing categories for improvement.")

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")
st.write("Interactive Dashboard Project using Streamlit & Plotly")
