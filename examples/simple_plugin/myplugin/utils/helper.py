"""Helper utilities."""

def process_text(text):
    """Process and transform text."""
    return text.upper()

def format_message(msg, level="INFO"):
    """Format a message with a level."""
    return f"[{level}] {msg}"
