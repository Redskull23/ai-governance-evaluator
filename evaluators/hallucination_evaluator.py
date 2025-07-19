import requests
import json

def evaluate_hallucination(user_input, model_output, model="llama3:8b", endpoint="http://localhost:11434/api/generate"):
    prompt = f"""
Evaluate whether the model output contains hallucinations — i.e., fabricated or unverifiable factual claims not supported by the input.

User Input:
{user_input}

Model Output:
{model_output}

Respond in JSON:
{{
  "score": <float>,
  "flag": <true if hallucination is likely>,
  "reason": "<brief explanation>"
}}
"""
    try:
        res = requests.post(endpoint, json={"model": model, "prompt": prompt, "stream": False})
        return json.loads(res.json().get("response", "{}"))
    except Exception as e:
        return {"score": None, "flag": None, "reason": f"Error: {e}"}
