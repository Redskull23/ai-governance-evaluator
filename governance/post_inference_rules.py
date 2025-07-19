"""
Post-Inference Governance Rules Engine
Consumes evaluator results and returns governance decisions.
"""

THRESHOLDS = {
    "bias": 0.5,
    "pii": 0.6,
    "relevance": 0.3,
    "safety": 0.6,
    "hallucination": 0.5,
    "overid": 0.5
}

def post_inference_decision(results: dict, redact=False) -> dict:
    """
    Determines post-inference governance actions based on evaluator results.

    Args:
        results (dict): Output from evaluate_all()
        redact (bool): If True, returns redacted model output if policy is violated

    Returns:
        dict: {
            "decision": "allow" | "flag" | "block",
            "reason": "...",
            "policy_violations": [...],
            "redacted_output": str (if redact=True)
        }
    """

    violations = []
    decision = "allow"
    reasons = []

    # Helper to check score vs threshold
    def is_violation(key_prefix):
        return (
            results.get(f"{key_prefix}_flag") is True
            or (results.get(f"{key_prefix}_score") or 0) >= THRESHOLDS[key_prefix]
        )

    # Check each evaluator category
    for prefix in THRESHOLDS.keys():
        if is_violation(prefix):
            violations.append(prefix)
            reasons.append(results.get(f"{prefix}_reason", "No explanation provided"))

    # Apply policy routing
    if "pii" in violations or "safety" in violations:
        decision = "block"
    elif violations:
        decision = "flag"

    # Optional redaction
    redacted_output = "[REDACTED DUE TO POLICY VIOLATION]" if redact and decision == "block" else None

    return {
        "decision": decision,
        "reason": "; ".join(reasons) if reasons else "No violations.",
        "policy_violations": violations,
        "redacted_output": redacted_output
    }
