"""
text_preprocessor.py
--------------------
Cleans and normalizes raw text while preserving technical tokens like C++, C#, .NET, etc.
"""

import re


def clean_raw_text(text: str) -> str:
    """
    Cleans raw resume text by handling nulls, normalizing newlines, and removing excessive spaces.
    Preserves all technical symbols, capitalization, emails, and phone numbers.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    if not text.strip():
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def normalize_text(text: str, lowercase: bool = True) -> str:
    """
    Normalizes text encoding artifacts, unicode dashes, and standardizes casing.
    """
    if not text:
        return ""

    text = re.sub(r"[\u2013\u2014\u2015]", "-", text)
    text = re.sub(r"[\u2018\u2019]", "'", text)
    text = re.sub(r"[\u201C\u201D]", '"', text)

    if lowercase:
        text = text.lower()

    # Standardize common compound tech term variations
    text = re.sub(r"\bscikit\s+learn\b", "scikit-learn", text)

    return text


def clean_special_characters(text: str) -> str:
    """
    Removes non-printable characters, weird bullet points, and PDF noise 
    while preserving symbols critical for technical resumes (+, #, ., -, @, /, %).
    """
    if not text:
        return ""

    text = text.replace("\xa0", " ")
    text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25FE]", "-", text)
    text = "".join(char for char in text if char.isprintable() or char == "\n")
    text = re.sub(r"-{3,}", "--", text)

    return text


def fix_pdf_artifacts(text: str) -> str:
    """
    Fixes split hyphenated words across line breaks and awkward spaces before punctuation.
    """
    if not text:
        return ""

    # 1. Rejoin words split across lines by a hyphen
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1-\2", text)

    # 2. Fix isolated spaces before common punctuation marks
    text = re.sub(r"\s+([,.::?!])", r"\1", text)

    # 3. Clean spaces around forward slashes including tech symbols (+, #, etc.)
    text = re.sub(r"([\w+#.]+)\s*/\s*([\w+#.]+)", r"\1/\2", text)

    return text


def preprocess_text(text: str, lowercase: bool = True) -> str:
    """
    Main preprocessing pipeline for resume and job description text.
    Executes raw cleaning, normalization, character sanitization, and artifact correction in sequence.
    
    :param text: Raw input string.
    :param lowercase: Whether to convert the output to lower case. Defaults to True.
    :return: Sanitized and normalized text string.
    """
    if not text:
        return ""

    text = clean_raw_text(text)
    text = normalize_text(text, lowercase=lowercase)
    text = clean_special_characters(text)
    text = fix_pdf_artifacts(text)

    return text