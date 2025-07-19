import streamlit as st
import pandas as pd
from evaluators.relevance_evaluator import relevance_score

df = pd.read_csv("data/sample_prompts.csv")
df["relevance"] = df.apply(lambda row: relevance_score(row["user_input"], row["model_output"]), axis=1)

st.title("LLM Governance Dashboard")
st.dataframe(df)
