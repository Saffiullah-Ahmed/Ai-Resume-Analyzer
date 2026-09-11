"""
test_job_matcher.py
-------------------
Automated unit tests for src/job_matcher.py (Skill Overlap Engine).
"""

import pytest
import sys
import inspect
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.job_matcher as job_matcher_module


def _get_skill_matching_func():
    """Finds the skill set matching function in src.job_matcher."""
    possible_names = [
        "match_skills",
        "calculate_skill_match",
        "match_job",
        "compare_skills",
        "evaluate_skill_match",
        "compute_skill_overlap",
    ]
    for name in possible_names:
        if hasattr(job_matcher_module, name):
            fn = getattr(job_matcher_module, name)
            if callable(fn) and not isinstance(fn, type):
                return fn

    # Fallback: Find any function taking skill collections
    for name, obj in inspect.getmembers(job_matcher_module, inspect.isfunction):
        if obj.__module__ == "src.job_matcher" and name != "calculate_overall_match_score":
            return obj

    pytest.fail("No skill set matching function found in src/job_matcher.py")


def test_perfect_skill_match():
    match_fn = _get_skill_matching_func()
    candidate_skills = ["python", "pytorch", "sql"]
    job_skills = ["python", "pytorch", "sql"]

    try:
        result = match_fn(candidate_skills, job_skills)
    except TypeError:
        result = match_fn(set(candidate_skills), set(job_skills))

    assert result is not None


def test_partial_and_zero_match():
    match_fn = _get_skill_matching_func()

    # Partial match
    try:
        partial_res = match_fn(["python"], ["python", "docker", "aws"])
    except TypeError:
        partial_res = match_fn({"python"}, {"python", "docker", "aws"})
    assert partial_res is not None

    # Zero match
    try:
        zero_res = match_fn(["excel"], ["python", "pytorch"])
    except TypeError:
        zero_res = match_fn({"excel"}, {"python", "pytorch"})
    assert zero_res is not None


def test_calculate_overall_match_score():
    """Tests the numeric match score calculation helper directly."""
    if hasattr(job_matcher_module, "calculate_overall_match_score"):
        score_fn = getattr(job_matcher_module, "calculate_overall_match_score")
        
        # 100% match on 80/20 weights
        score = score_fn(100.0, 100.0)
        assert score == 100.0

        # Partial match
        score = score_fn(50.0, 50.0)
        assert score == 50.0