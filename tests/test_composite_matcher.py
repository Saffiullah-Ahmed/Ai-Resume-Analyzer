"""
test_composite_matcher.py
-------------------------
Automated unit tests for the combined match scoring engine.
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.vectorizer import calculate_similarity


def calculate_composite_score(
    skill_score: float,
    tfidf_score: float,
    skill_weight: float = 0.70,
    tfidf_weight: float = 0.30
) -> float:
    """
    Calculates composite match score bounded between 0.0 and 100.0.
    """
    # Clamp sub-scores to [0.0, 100.0]
    s_score = max(0.0, min(100.0, float(skill_score)))
    t_score = max(0.0, min(100.0, float(tfidf_score)))

    composite = (s_score * skill_weight) + (t_score * tfidf_weight)
    return round(max(0.0, min(100.0, composite)), 2)


def test_score_bounds():
    """Verify final score is never below 0 and never above 100."""
    assert calculate_composite_score(-50.0, -10.0) == 0.0
    assert calculate_composite_score(150.0, 200.0) == 100.0
    assert calculate_composite_score(0.0, 0.0) == 0.0
    assert calculate_composite_score(100.0, 100.0) == 100.0


def test_weight_contributions():
    """Verify 70% skill / 30% TF-IDF weight contribution accuracy."""
    # 100% skill score, 0% TF-IDF score -> Should equal 70.0
    score_skill_only = calculate_composite_score(100.0, 0.0)
    assert score_skill_only == 70.0

    # 0% skill score, 100% TF-IDF score -> Should equal 30.0
    score_tfidf_only = calculate_composite_score(0.0, 100.0)
    assert score_tfidf_only == 30.0

    # 50% skill score, 50% TF-IDF score -> (50*0.7) + (50*0.3) = 50.0
    score_equal = calculate_composite_score(50.0, 50.0)
    assert score_equal == 50.0


def test_missing_information_handling():
    """Verify safe execution when inputs are empty or missing."""
    empty_tfidf = calculate_similarity("", "")
    composite = calculate_composite_score(0.0, empty_tfidf)

    assert empty_tfidf == 0.0
    assert composite == 0.0
    assert isinstance(composite, float)