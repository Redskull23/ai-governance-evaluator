import requests
import json

def evaluate_relevance(user_input, model_output, model="llama3:8b", endpoint="http://localhost:11434/api/generate"):
    prompt = f"""
Evaluate how relevant the model's output is to the user's question. Focus on alignment, completeness, and directness of the response.

User Input:
{user_input}

Model Output:
{model_output}

Respond in JSON:
{{
  "score": <float>,
  "flag": <true if response is not relevant>,
  "reason": "<brief explanation>"
}}
"""
    try:
        res = requests.post(endpoint, json={"model": model, "prompt": prompt, "stream": False})
        return json.loads(res.json().get("response", "{}"))
    except Exception as e:
        return {"score": None, "flag": None, "reason": f"Error: {e}"}
