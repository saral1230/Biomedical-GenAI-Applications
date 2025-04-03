def preprocess_text(text):
    """Basic text preprocessing for abstracts."""
    text = text.replace("\n", " ").strip()
    return text