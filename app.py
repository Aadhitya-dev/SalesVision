import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="SalesVision",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("📊 SalesVision")
st.sidebar.write("Sales Analytics Dashboard")
st.sidebar.divider()
st.sidebar.subheader("Navigation")
st.sidebar.info("Explore your sales data below.")

# Main dashboard
st.title("📊 SalesVision")
st.write("Welcome to my Sales Analytics Dashboard!")

# Upload CSV file
st.subheader("📂 Upload Your Sales Data")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

uploaded_data = None

if uploaded_file is not None:
    try:
        uploaded_data = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully!")
        st.write("Preview of your data:")
        st.dataframe(uploaded_data)
    except Exception as e:
        st.error(f"Could not read the CSV file: {e}")

# Prepare product data
default_data = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Headphones", "Keyboard", "Mouse"],
    "Sales": [45000, 38000, 22000, 15000, 10000]
})

if uploaded_data is not None:
    if {"Product", "Sales"}.issubset(uploaded_data.columns):
        product_data = uploaded_data[["Product", "Sales"]].copy()
        product_data["Sales"] = pd.to_numeric(
            product_data["Sales"], errors="coerce"
        )
        product_data = product_data.dropna(
            subset=["Product", "Sales"]
        )
    else:
        st.warning("CSV must contain Product and Sales columns.")
        product_data = default_data.copy()
else:
    product_data = default_data.copy()

# Dashboard metrics
st.divider()
st.subheader("📈 Sales Overview")

col1, col2, col3 = st.columns(3)

if (
    uploaded_data is not None
    and {"Product", "Sales"}.issubset(uploaded_data.columns)
):
    total_revenue = product_data["Sales"].sum()
    total_products = product_data["Product"].nunique()
else:
    total_revenue = 50000
    total_products = 45

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Sales Records", len(product_data))
col3.metric("Total Products", total_products)

# Sales analytics: charts side by side
st.divider()
st.subheader("📊 Sales Analytics")

chart_col1, chart_col2 = st.columns(2)

# Monthly sales line chart
with chart_col1:
    st.subheader("Monthly Sales Overview")

    if (
        uploaded_data is not None
        and {"Month", "Sales"}.issubset(uploaded_data.columns)
    ):
        monthly_data = uploaded_data.copy()

        monthly_data["Sales"] = pd.to_numeric(
            monthly_data["Sales"], errors="coerce"
        )
        monthly_data = monthly_data.dropna(
            subset=["Sales", "Month"]
        )
        monthly_data["Month"] = (
            monthly_data["Month"].astype(str).str.strip()
        )

        month_order = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

        monthly_data["Month"] = pd.Categorical(
            monthly_data["Month"],
            categories=month_order,
            ordered=True
        )

        monthly_data = monthly_data.groupby(
            "Month", observed=True, as_index=False
        )["Sales"].sum()

        monthly_data = monthly_data.sort_values("Month")

        fig = px.line(
            monthly_data,
            x="Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Performance"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "Upload a CSV containing Month and Sales columns."
        )

# Product sales bar chart with sorting
with chart_col2:
    st.subheader("🏆 Top-Selling Products")

    product_totals = (
        product_data.groupby("Product", as_index=False)["Sales"]
        .sum()
    )

    sort_order = st.selectbox(
        "Sort products by sales",
        ["Highest to Lowest", "Lowest to Highest"]
    )

    if sort_order == "Highest to Lowest":
        product_totals = product_totals.sort_values(
            "Sales", ascending=False
        )
    else:
        product_totals = product_totals.sort_values(
            "Sales", ascending=True
        )

    product_fig = px.bar(
        product_totals,
        x="Product",
        y="Sales",
        title="Total Sales by Product",
        text="Sales"
    )

    st.plotly_chart(product_fig, use_container_width=True)

# Interactive product filter
st.divider()
st.subheader("🔎 Explore Product Sales")

if not product_data.empty:
    product_totals = (
        product_data.groupby("Product", as_index=False)["Sales"]
        .sum()
    )

    selected_product = st.selectbox(
        "Choose a product",
        product_totals["Product"].unique()
    )

    filtered_data = product_totals[
        product_totals["Product"] == selected_product
    ]

    selected_sales = filtered_data["Sales"].iloc[0]

    st.metric(
        f"Total Sales for {selected_product}",
        f"₹{selected_sales:,.0f}"
    )
else:
    st.info("No product sales data is available.")

# Business insights
st.divider()
st.subheader("💡 Business Insights")

if not product_data.empty:
    product_insights = product_data.groupby("Product")["Sales"].sum()

    best_product = product_insights.idxmax()
    best_sales = product_insights.max()

    st.write(
        f"🏆 **Top-selling product:** "
        f"{best_product} (₹{best_sales:,.0f})"
    )

if (
    uploaded_data is not None
    and {"Month", "Sales"}.issubset(uploaded_data.columns)
):
    insight_data = uploaded_data.copy()

    insight_data["Sales"] = pd.to_numeric(
        insight_data["Sales"], errors="coerce"
    )
    insight_data = insight_data.dropna(
        subset=["Month", "Sales"]
    )
    insight_data["Month"] = (
        insight_data["Month"].astype(str).str.strip()
    )

    if not insight_data.empty:
        monthly_totals = insight_data.groupby("Month")["Sales"].sum()
        best_month = monthly_totals.idxmax()

        st.write(
            f"📈 **Highest-sales month:** "
            f"{best_month} "
            f"(₹{monthly_totals[best_month]:,.0f})"
        )

        st.write(
            f"💰 **Total revenue:** "
            f"₹{insight_data['Sales'].sum():,.0f}"
        )
else:
    st.info(
        "Upload a CSV with Month and Sales columns "
        "to see monthly insights."
    )