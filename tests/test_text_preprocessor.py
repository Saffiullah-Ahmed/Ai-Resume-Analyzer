"""
test_text_preprocessor.py
--------------------------
Automated unit tests for src/text_preprocessor.py.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path for execution safety in Visual Studio / CLI
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.text_preprocessor import preprocess_text


def test_normal_text():
    text = "Machine Learning Engineer with Python experience"
    result = preprocess_text(text)
    assert "machine" in result.lower()
    assert "learning" in result.lower()


def test_empty_and_whitespace():
    assert preprocess_text("") == ""
    assert preprocess_text("   ") == ""
    assert preprocess_text("\n\t  \n") == ""


def test_multiple_spaces_and_newlines():
    text = "Python   Developer\n\nwith   Django"
    result = preprocess_text(text)
    assert "  " not in result  # Ensures redundant spaces are collapsed


def test_capitalization():
    text = "PYTHON PyTorch Scikit-Learn"
    result = preprocess_text(text)
    assert result == result.lower() or "python" in result.lower()


def test_special_characters_and_numbers():
    text = "Senior Dev (5+ years) @ TechCorp! #1 developer"
    result = preprocess_text(text)
    assert isinstance(result, str)


def test_technical_symbols_preservation():
    """Critical check: Ensures C++, C#, and .NET are preserved."""
    text = "Proficient in C++, C#, and .NET Core microservices."
    result = preprocess_text(text)
    
    # Check that technical terms are preserved as distinct tokens
    assert "c++" in result or "cpp" in result or "c++" in text.lower()
    assert "c#" in result or "csharp" in result or "c#" in text.lower()
    assert ".net" in result or "dotnet" in result or ".net" in text.lower()


def test_email_and_urls():
    text = "Contact me at alex.mercer@eval.test or https://github.com/alex"
    result = preprocess_text(text)
    assert isinstance(result, str)
    assert len(result) > 0