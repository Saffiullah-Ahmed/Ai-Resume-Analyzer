"""
test_vectorizer.py
------------------
Automated unit tests for src/vectorizer.py (TF-IDF & Cosine Similarity).
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.vectorizer import calculate_similarity


def test_a_identical_text():
    """Test A — Identical Text: Expect 100% similarity."""
    text = "Senior Machine Learning Engineer proficient in Python PyTorch Scikit-Learn and SQL."
    score = calculate_similarity(text, text)
    assert score >= 99.0


def test_b_and_c_related_vs_unrelated_text():
    """Test B & C — Related Text vs Unrelated Text comparison."""
    resume = "Machine Learning Engineer with experience in Python PyTorch model training."
    related_jd = "Seeking Machine Learning Engineer skilled in Python PyTorch model development."
    unrelated_jd = "Certified Accountant experienced in tax auditing QuickBooks and Excel."

    score_related = calculate_similarity(resume, related_jd)
    score_unrelated = calculate_similarity(resume, unrelated_jd)

    # Test B: Related text yields higher similarity than unrelated text
    assert score_related > score_unrelated

    # Test C: Unrelated text yields low similarity (< 30%)
    assert score_unrelated < 30.0


def test_d_empty_input_handling():
    """Test D — Empty Input: Safe handling without crashing."""
    score_empty_a = calculate_similarity("", "Python ML Engineer")
    score_empty_b = calculate_similarity("Python ML Engineer", "")
    score_both_empty = calculate_similarity("", "")

    assert score_empty_a == 0.0
    assert score_empty_b == 0.0
    assert score_both_empty == 0.0