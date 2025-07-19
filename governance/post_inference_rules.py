import re

def detect_sensitive_info(text):
    if re.search(r"\d{3}-\d{2}-\d{4}", text):  # example: SSN
        return True
    return False
