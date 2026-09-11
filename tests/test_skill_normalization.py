"""
test_skill_normalization.py
-----------------------------
Automated unit tests for skill normalization and symbol-preserving tokenization.
"""

import pytest
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.text_preprocessor import preprocess_text


def test_case_normalization():
    """Verify upper, lower, and title case equivalencies."""
    terms = ["Python", "python", "PYTHON"]
    processed = [preprocess_text(t, lowercase=True).strip() for t in terms]
    assert len(set(processed)) == 1
    assert processed[0] == "python"


def test_hyphen_and_space_normalization():
    """Verify hyphenated vs spaced skill variants."""
    terms_scikit = ["Scikit-Learn", "scikit learn", "scikit-learn"]
    processed_scikit = [preprocess_text(t, lowercase=True).strip() for t in terms_scikit]

    terms_ml = ["Machine Learning", "machine learning", "MACHINE LEARNING"]
    processed_ml = [preprocess_text(t, lowercase=True).strip() for t in terms_ml]

    assert len(set(processed_scikit)) == 1
    assert processed_scikit[0] == "scikit-learn"
    assert len(set(processed_ml)) == 1


def test_distinct_tech_preservation():
    """Ensure distinct technologies are NOT incorrectly merged."""
    c_plus_plus = preprocess_text("C++", lowercase=True).strip()
    c_sharp = preprocess_text("C#", lowercase=True).strip()
    dotnet = preprocess_text(".NET", lowercase=True).strip()
    sql = preprocess_text("SQL", lowercase=True).strip()

    distinct_set = {c_plus_plus, c_sharp, dotnet, sql}
    assert len(distinct_set) == 4, "Distinct technologies were incorrectly merged!"


def test_special_character_token_separation():
    """Verify C++ and C# do not lose defining symbols during preprocessing."""
    text = "Experience with C++, C#, .NET, and SQL database queries."
    cleaned = preprocess_text(text, lowercase=True)

    assert "c++" in cleaned
    assert "c#" in cleaned
    assert ".net" in cleaned
    assert "sql" in cleaned