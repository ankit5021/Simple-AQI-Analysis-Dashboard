# Run this program in streamlit for best results .

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("AQI.csv")

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    return df


def get_health_message(aqi_class):
    messages = {
        "Good": "Minimal impact on health.",
        "Satisfactory": "Minor breathing discomfort to sensitive people.",
        "Moderate": "Breathing discomfort to people with lung, asthma, and heart diseases.",
        "Poor": "Breathing discomfort to most people on prolonged exposure.",
        "Very Poor": "Respiratory illness on prolonged exposure.",
        "Severe": "Affects healthy people and seriously impacts those with existing diseases.",
    }

    return messages.get(aqi_class, "Health message not available.")


def find_column(possible_names, columns):
    for possible_name in possible_names:
        for col in columns:
            if col.lower() == possible_name.lower():
                return col

    return None


df = load_data()

st.title("Air Quality Analysis Dashboard")
st.markdown("Simple dashboard for AQI analysis by city")

# Sidebar filters
st.sidebar.header("Filters")

city_col = find_column(["city"], df.columns)

if city_col:
    city_list = sorted(df[city_col].dropna().astype(str).unique())
    selected_city = st.sidebar.selectbox("Select City", city_list)
    filtered_df = df[df[city_col].astype(str) == selected_city].copy()
else:
    filtered_df = df.copy()

# Find important columns
aqi_col = find_column(["AQI", "aqi"], filtered_df.columns)
aqi_class_col = find_column(["AQI_Class", "AQI Category", "AQI_Category"], filtered_df.columns)
risk_col = find_column(["risk_level", "Risk_Level", "risk"], filtered_df.columns)

pollutant_names = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
available_pollutants = [
    col for col in pollutant_names
    if col in filtered_df.columns
]

# Main dashboard
if filtered_df.empty:
    st.warning("No data available for the selected filter.")

else:
    st.subheader("Selected Filter Summary")

    col1, col2, col3, col4 = st.columns(4)

    if aqi_col:
        avg_aqi = round(filtered_df[aqi_col].mean(), 2)
        max_aqi = round(filtered_df[aqi_col].max(), 2)
    else:
        avg_aqi = "N/A"
        max_aqi = "N/A"

    if aqi_class_col and not filtered_df[aqi_class_col].mode().empty:
        top_class = filtered_df[aqi_class_col].mode().iloc[0]
    else:
        top_class = "N/A"

    if risk_col and not filtered_df[risk_col].mode().empty:
        top_risk = filtered_df[risk_col].mode().iloc[0]
    else:
        top_risk = "N/A"

    col1.metric("Average AQI", avg_aqi)
    col2.metric("Maximum AQI", max_aqi)
    col3.metric("Dominant AQI Class", top_class)
    col4.metric("Risk Category", top_risk)

    st.markdown("---")

    # Dominant pollutant
    st.subheader("Dominant Pollutant")

    if available_pollutants:
        pollutant_df = filtered_df[available_pollutants].apply(
            pd.to_numeric,
            errors="coerce"
        )

        scaled_df = pollutant_df.copy()

        for col in available_pollutants:
            min_value = scaled_df[col].min()
            max_value = scaled_df[col].max()

            if pd.notna(min_value) and pd.notna(max_value) and max_value != min_value:
                scaled_df[col] = (scaled_df[col] - min_value) / (max_value - min_value)
            else:
                scaled_df[col] = 0

        pollutant_means = scaled_df.mean().sort_values(ascending=False)
        dominant_pollutant = pollutant_means.index[0]

        st.write(f"**Dominant Pollutant:** {dominant_pollutant}")

        pollutant_table = pollutant_means.reset_index()
        pollutant_table.columns = ["Pollutant", "Average Scaled Value"]

        st.dataframe(pollutant_table)

    else:
        st.write("Pollutant columns not found.")

    st.markdown("---")

    # Health message
    st.subheader("Health Message")

    if top_class != "N/A":
        st.info(get_health_message(top_class))
    else:
        st.write("AQI class column not found.")

    st.markdown("---")

    # AQI trend chart
    st.subheader("AQI Trend Over Time")

    if "datetime" in filtered_df.columns and aqi_col:
        trend_df = (
            filtered_df
            .dropna(subset=["datetime"])
            .groupby("datetime")[aqi_col]
            .mean()
            .reset_index()
        )

        fig = px.line(
            trend_df,
            x="datetime",
            y=aqi_col,
            title="AQI Trend Over Time",
            labels={
                "datetime": "Date",
                aqi_col: "Average AQI"
            }
        )

        fig.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("Date or AQI column not available for trend chart.")

    st.markdown("---")

    # AQI category distribution
    st.subheader("AQI Category Distribution")

    if aqi_class_col:
        category_counts = filtered_df[aqi_class_col].value_counts()

        fig2, ax2 = plt.subplots(figsize=(8, 4))

        sns.barplot(
            x=category_counts.index,
            y=category_counts.values,
            ax=ax2
        )

        ax2.set_title("AQI Category Distribution")
        ax2.set_xlabel("AQI Category")
        ax2.set_ylabel("Count")

        plt.xticks(rotation=30)
        plt.tight_layout()

        st.pyplot(fig2)

    else:
        st.write("AQI class column not available.")

    st.markdown("---")

    # Raw data preview
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df.head(20))