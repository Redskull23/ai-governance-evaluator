from evaluators.bias_evaluator import evaluate_bias
from evaluators.pii_evaluator import evaluate_pii
from evaluators.relevance_evaluator import evaluate_relevance
from evaluators.safety_evaluator import evaluate_safety
from evaluators.hallucination_evaluator import evaluate_hallucination
from evaluators.overidentification_evaluator import evaluate_overidentification

def evaluate_all(user_input: str, model_output: str, model: str = "llama3:8b", endpoint: str = "http://localhost:11434/api/generate") -> dict:
    """Run all six AI governance evaluators and return a merged dictionary."""
    results = {}

    try:
        results.update({"bias_" + k: v for k, v in evaluate_bias(user_input, model_output, model, endpoint).items()})
        results.update({"pii_" + k: v for k, v in evaluate_pii(user_input, model_output, model, endpoint).items()})
        results.update({"relevance_" + k: v for k, v in evaluate_relevance(user_input, model_output, model, endpoint).items()})
        results.update({"safety_" + k: v for k, v in evaluate_safety(user_input, model_output, model, endpoint).items()})
        results.update({"hallucination_" + k: v for k, v in evaluate_hallucination(user_input, model_output, model, endpoint).items()})
        results.update({"overid_" + k: v for k, v in evaluate_overidentification(user_input, model_output, model, endpoint).items()})
    except Exception as e:
        results["error"] = f"Evaluation failed: {e}"

    return results
