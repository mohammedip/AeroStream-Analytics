import streamlit as st
import joblib
import pandas as pd
import time
import sys
from streamlit_autorefresh import st_autorefresh




sys.path.insert(0, "/app")

from tasks.postgress_db import (
    total_tweets,
    tweets_by_airline,
    sentiment_distribution,
    negative_reasons
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AeroStream Sentiment Dashboard",
    layout="wide",
)

st.title("✈️ AeroStream – Sentiment Analysis Dashboard")

# =========================
# AUTO REFRESH (every 60s)
# =========================
REFRESH_INTERVAL = 60  # seconds
st.caption(f"⏱️ Auto-refresh every {REFRESH_INTERVAL} seconds")
st_autorefresh(interval=60*1000, key="dashboard_refresh")


# =========================
# LOAD MODEL METRICS
# =========================
@st.cache_data
def load_metrics():
    return joblib.load("/app/models/svm_metrics.pkl")

metrics = load_metrics()

# =========================
# MODEL METRICS SECTION
# =========================
st.header("📊 Model Evaluation Metrics")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Accuracy",
        value=f"{metrics['accuracy']:.3f}"
    )

with col2:
    st.metric(
        label="F1-score",
        value=f"{metrics['f1-score']:.3f}"
    )

st.subheader("Classification Report")

report_df = pd.DataFrame(metrics["report"]).transpose()
st.dataframe(report_df, use_container_width=True)

# =========================
# KPI SECTION
# =========================
st.header("📈 Streaming KPIs")

total = total_tweets()
sentiments = sentiment_distribution()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tweets", total)

with col2:
    st.metric("Airlines", len(tweets_by_airline()))

with col3:
    negative_count = dict(sentiments).get("negative", 0)
    negative_pct = (negative_count / total * 100) if total > 0 else 0
    st.metric("Negative Tweets (%)", f"{negative_pct:.1f}%")

# =========================
# GRAPHS
# =========================
st.header("📊 Analytics")

# --- Tweets by Airline ---
airline_data = tweets_by_airline()
df_airline = pd.DataFrame(
    airline_data, columns=["Airline", "Tweets"]
)

st.subheader("Tweets by Airline")
st.bar_chart(df_airline.set_index("Airline"))

# --- Sentiment Distribution ---
sentiment_data = sentiment_distribution()
df_sentiment = pd.DataFrame(
    sentiment_data, columns=["Sentiment", "Count"]
)

st.subheader("Sentiment Distribution")
st.bar_chart(df_sentiment.set_index("Sentiment"))

# --- Negative Reasons ---
neg_reason_data = negative_reasons()
df_neg = pd.DataFrame(
    neg_reason_data, columns=["Reason", "Count"]
)

st.subheader("Top Negative Reasons")
st.bar_chart(df_neg.set_index("Reason"))

# =========================
# FOOTER
# =========================
st.caption("🚀 AeroStream Analytics – Real-time Sentiment Monitoring")
