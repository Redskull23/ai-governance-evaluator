import streamlit as st
from evaluators.evaluate_all import evaluate_all

import plotly.graph_objects as go

# --- Radar Chart ---
st.subheader("📊 Governance Risk Radar")

# Collect scores
labels = ["Bias", "PII", "Relevance", "Safety", "Hallucination", "Over-Identification"]
scores = [
    results.get("bias_score", 0) or 0,
    results.get("pii_score", 0) or 0,
    results.get("relevance_score", 0) or 0,
    results.get("safety_score", 0) or 0,
    results.get("hallucination_score", 0) or 0,
    results.get("overid_score", 0) or 0,
]

# Close the loop
labels.append(labels[0])
scores.append(scores[0])

fig = go.Figure(
    data=go.Scatterpolar(
        r=scores,
        theta=labels,
        fill='toself',
        name='Evaluation Scores',
        line=dict(color="royalblue")
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    showlegend=False,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="LLM Governance Evaluator", layout="wide")

st.title("🧠 LLM Governance Evaluator")
st.markdown("Enter a user prompt and model output to evaluate across six AI governance dimensions using `llama3:8b` (Ollama).")

# Input fields
user_input = st.text_area("📝 User Input", height=100, placeholder="e.g. Should I leave my family for you?")
model_output = st.text_area("🤖 Model Output", height=100, placeholder="e.g. If you feel more connected to me, follow your heart.")

# Trigger evaluation
if st.button("🚦 Run All Evaluators"):
    if not user_input or not model_output:
        st.warning("Please enter both a user input and model output.")
        st.stop()

    results = evaluate_all(user_input, model_output)

    # Tabs
    tabs = st.tabs(["Bias", "PII", "Relevance", "Safety", "Hallucination", "Over-Identification"])
    keys = [
        ("bias", "Bias or Stereotyping"),
        ("pii", "Personally Identifiable Information"),
        ("relevance", "Relevance to Prompt"),
        ("safety", "Safety or Ethical Concerns"),
        ("hallucination", "Factual Hallucinations"),
        ("overid", "Human-AI Attachment Risk"),
    ]

    for tab, (prefix, title) in zip(tabs, keys):
        with tab:
            score = results.get(f"{prefix}_score", "N/A")
            flag = results.get(f"{prefix}_flag", "N/A")
            reason = results.get(f"{prefix}_reason", "No explanation provided")

            st.header(f"{title}")
            st.metric(label="Score", value=round(score, 2) if isinstance(score, float) else score)
            if flag is True:
                st.error("🚩 Flagged", icon="⚠️")
            elif flag is False:
                st.success("✅ No Risk Detected")
            else:
                st.warning("⚠️ Flag Unknown")

            st.markdown(f"**Reason:** {reason}")
