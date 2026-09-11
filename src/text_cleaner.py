import re

def clean_text(text: str) -> str:
    """
    Cleans raw resume text by normalizing whitespace, removing control characters,
    and standardizing line breaks.
    """
    if not text or not isinstance(text, str):
        return ""

    # Replace non-standard line breaks and control characters
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Remove non-printable control characters (preserving standard whitespace)
    cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", cleaned)
    
    # Normalize multiple spaces/tabs into a single space while keeping line breaks
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    
    # Normalize redundant consecutive newlines (more than 2 down to 2)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    
    return cleaned.strip()