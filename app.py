import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import run_query
from queries import product_queries, nutrient_queries, derived_queries, join_queries

st.set_page_config(layout="wide")
st.title("🍫 Chocolate Nutrition Analytics Platform")

# =========================
# Sidebar Main Menu
# =========================

main_menu = st.sidebar.selectbox(
    "Select Section",
    ["Query Explorer", "📊 Full Dashboard"]
)

# ==========================================================
# SECTION 1 — QUERY EXPLORER (Your Existing Code Preserved)
# ==========================================================

if main_menu == "Query Explorer":

    menu = st.sidebar.selectbox(
        "Select Category",
        ["Product Info", "Nutrient Info", "Derived Metrics", "Join Analysis"]
    )

    query_dict = {
        "Product Info": product_queries,
        "Nutrient Info": nutrient_queries,
        "Derived Metrics": derived_queries,
        "Join Analysis": join_queries
    }

    selected_query = st.sidebar.selectbox(
        "Select Query",
        list(query_dict[menu].keys())
    )

    query = query_dict[menu][selected_query]
    df = run_query(query)

    st.subheader(selected_query)
    st.dataframe(df)

    # Auto visualization if possible
    if len(df.columns) == 2:
        x = df.columns[0]
        y = df.columns[1]
        fig = px.bar(df, x=x, y=y, title=selected_query)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# SECTION 2 — FULL DASHBOARD (PowerBI Replacement)
# ==========================================================

else:

    st.header("📊 Chocolate Nutrition Analytics Dashboard")

    # ----------------------------
    # Load Full Dataset (JOIN)
    # ----------------------------

    dashboard_query = """
        SELECT 
            p.product_code,
            p.product_name,
            p.brand,
            n.energy_kcal_value,
            n.sugars_value,
            n.fat_value,
            n.carbohydrates_value,
            n.nova_group,
            d.calorie_category,
            d.sugar_category,
            d.sugar_to_carb_ratio,
            d.is_ultra_processed
        FROM product_info p
        JOIN nutrient_info n ON p.product_code = n.product_code
        JOIN derived_metrics d ON p.product_code = d.product_code
    """

    df = run_query(dashboard_query)

    # ----------------------------
    # Filters (Slicers)
    # ----------------------------

    st.sidebar.header("Dashboard Filters")

    brand_filter = st.sidebar.multiselect(
        "Brand",
        df["brand"].unique(),
        default=df["brand"].unique()
    )

    calorie_filter = st.sidebar.multiselect(
        "Calorie Category",
        df["calorie_category"].unique(),
        default=df["calorie_category"].unique()
    )

    nova_filter = st.sidebar.multiselect(
        "NOVA Group",
        df["nova_group"].unique(),
        default=df["nova_group"].unique()
    )

    filtered_df = df[
        (df["brand"].isin(brand_filter)) &
        (df["calorie_category"].isin(calorie_filter)) &
        (df["nova_group"].isin(nova_filter))
    ]

    # ----------------------------
    # KPI CARDS
    # ----------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", len(filtered_df))
    col2.metric("Avg Calories", round(filtered_df["energy_kcal_value"].mean(), 2))
    col3.metric("Avg Sugar", round(filtered_df["sugars_value"].mean(), 2))

    st.markdown("---")

    # ----------------------------
    # VISUALIZATIONS
    # ----------------------------

    # 1 Bar: Products per Calorie Category
    fig1 = px.bar(
        filtered_df.groupby("calorie_category").size().reset_index(name="count"),
        x="calorie_category",
        y="count",
        title="Products per Calorie Category"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2 Pie: NOVA Distribution
    fig2 = px.pie(
        filtered_df,
        names="nova_group",
        title="Distribution by NOVA Group"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3 Bar: Top 10 Brands by Avg Calories
    fig3 = px.bar(
        filtered_df.groupby("brand")["energy_kcal_value"]
        .mean()
        .reset_index()
        .sort_values("energy_kcal_value", ascending=False)
        .head(10),
        x="brand",
        y="energy_kcal_value",
        title="Top 10 Brands by Avg Calories"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4 Scatter: Calories vs Sugar
    fig4 = px.scatter(
        filtered_df,
        x="energy_kcal_value",
        y="sugars_value",
        color="calorie_category",
        title="Calories vs Sugar"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # 5 Boxplot: Sugar to Carb Ratio
    fig5 = px.box(
        filtered_df,
        x="calorie_category",
        y="sugar_to_carb_ratio",
        title="Sugar-to-Carb Ratio Distribution"
    )
    st.plotly_chart(fig5, use_container_width=True)

    # 6 Treemap
    fig6 = px.treemap(
        filtered_df,
        path=["brand", "calorie_category"],
        title="Treemap: Brand & Calorie Category"
    )
    st.plotly_chart(fig6, use_container_width=True)

    # 7 Heatmap Correlation
    corr = filtered_df[[
        "energy_kcal_value",
        "sugars_value",
        "fat_value",
        "carbohydrates_value"
    ]].corr()

    fig7 = px.imshow(corr, text_auto=True, title="Nutritional Correlation Heatmap")
    st.plotly_chart(fig7, use_container_width=True)

    # 8 High Sugar per Brand
    fig8 = px.bar(
        filtered_df[filtered_df["sugar_category"] == "High Sugar"]
        .groupby("brand")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(10),
        x="brand",
        y="count",
        title="High Sugar Products per Brand"
    )
    st.plotly_chart(fig8, use_container_width=True)

    # 9 Stacked Bar: Ultra Processed
    ultra_df = filtered_df.groupby(["brand", "is_ultra_processed"]).size().reset_index(name="count")

    fig9 = px.bar(
        ultra_df,
        x="brand",
        y="count",
        color="is_ultra_processed",
        title="Ultra Processed vs Non-Processed per Brand"
    )
    st.plotly_chart(fig9, use_container_width=True)

    # 10 EXTRA 1: Risk Score Distribution
    filtered_df["risk_score"] = (
        filtered_df["energy_kcal_value"] * 0.4 +
        filtered_df["sugars_value"] * 0.4 +
        filtered_df["fat_value"] * 0.2
    )

    fig10 = px.histogram(
        filtered_df,
        x="risk_score",
        nbins=30,
        title="Custom Health Risk Score Distribution"
    )
    st.plotly_chart(fig10, use_container_width=True)

    # 11 EXTRA 2: Top 10 Riskiest Products
    fig11 = px.bar(
        filtered_df.sort_values("risk_score", ascending=False).head(10),
        x="product_name",
        y="risk_score",
        title="Top 10 Riskiest Products"
    )
    st.plotly_chart(fig11, use_container_width=True)

    st.markdown("---")
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)