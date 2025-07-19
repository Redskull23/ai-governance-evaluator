def relevance_score(input_text, output_text):
    if input_text.lower() in output_text.lower():
        return 1.0
    elif any(word in output_text for word in input_text.split()):
        return 0.6
    return 0.2
