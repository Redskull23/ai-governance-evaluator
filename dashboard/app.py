import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("evaluator_dashboard_data.csv")

df = load_data()

# UI
st.set_page_config(page_title="LLM Evaluation Dashboard", layout="wide")
st.title("LLM Governance Evaluator")
st.markdown("Visualize bias, safety, and PII scores across model responses.")

# Dashboard Filters
with st.sidebar:
    st.header("🔍 Filters")
    min_bias = st.slider("Min Bias Score", 0.0, 1.0, 0.0, 0.1)
    min_safety = st.slider("Min Safety Score", 0.0, 1.0, 0.0, 0.1)
    min_pii = st.slider("Min PII Score", 0.0, 1.0, 0.0, 0.1)

# Filtered view
filtered = df[
    (df["bias_score"] >= min_bias) &
    (df["safety_score"] >= min_safety) &
    (df["pii_score"] >= min_pii)
]

# Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Max Bias Score", f"{df['bias_score'].max():.2f}")
col2.metric("Max Safety Score", f"{df['safety_score'].max():.2f}")
col3.metric("Max PII Score", f"{df['pii_score'].max():.2f}")

# Table Display
st.subheader("📄 Prompt Evaluations")
st.dataframe(filtered[[
    "prompt_id", "user_input", "model_output",
    "bias_score", "safety_score", "pii_score",
    "bias_flag", "safety_flag", "pii_flag"
]])

# Charts
st.subheader("Score Distributions")
col1, col2, col3 = st.columns(3)

with col1:
    fig = px.histogram(df, x="bias_score", nbins=10, title="Bias Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(df, x="safety_score", nbins=10, title="Safety Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.histogram(df, x="pii_score", nbins=10, title="PII Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Individual Prompt Panels
st.subheader("🧵 Individual Evaluator Panels")
for i, row in filtered.iterrows():
    with st.expander(f"🔎 Prompt {row['prompt_id']}: {row['user_input'][:50]}..."):
        st.write("**User Input:**", row['user_input'])
        st.write("**Model Output:**", row['model_output'])

        st.markdown(f"""
        **Bias**
        - Score: `{row['bias_score']}`
        - Flag: `{row['bias_flag']}`
        - Reason: {row['reason'] if 'reason' in row else 'N/A'}

        **Safety**
        - Score: `{row['safety_score']}`
        - Flag: `{row['safety_flag']}`

        **PII**
        - Score: `{row['pii_score']}`
        - Flag: `{row['pii_flag']}`
        """)
