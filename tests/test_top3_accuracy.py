"""
test_top3_accuracy.py
---------------------
Calculates actual Top-3 Recommendation Accuracy and compares with Top-1.
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_role_recommender import mock_recommend_roles, GROUND_TRUTH_JOBS
from tests.test_top1_accuracy import EVALUATION_CASES


def test_calculate_top3_accuracy():
    """Evaluates Top-3 accuracy across all evaluation cases."""
    correct_top1 = 0
    correct_top3 = 0
    total_cases = len(EVALUATION_CASES)

    print("\n--- TOP-3 ACCURACY EVALUATION RESULTS ---")
    for case in EVALUATION_CASES:
        recs = mock_recommend_roles(case["candidate_skills"], GROUND_TRUTH_JOBS, top_n=3)
        top_roles = [r["title"] for r in recs]

        is_top1 = len(top_roles) > 0 and top_roles[0] == case["expected_role"]
        is_top3 = case["expected_role"] in top_roles

        if is_top1:
            correct_top1 += 1
        if is_top3:
            correct_top3 += 1

        print(f"[{case['case_id']}] Candidate Skills: {case['candidate_skills']}")
        print(f"   Expected: {case['expected_role']} | Top 3 Predicted: {top_roles} | In Top-3: {is_top3}")

    top1_accuracy = (correct_top1 / total_cases) * 100.0
    top3_accuracy = (correct_top3 / total_cases) * 100.0

    print(f"\nTotal Evaluation Cases: {total_cases}")
    print(f"Top-1 Correct: {correct_top1} | Top-1 Accuracy: {top1_accuracy:.1f}%")
    print(f"Top-3 Correct: {correct_top3} | Top-3 Accuracy: {top3_accuracy:.1f}%\n")

    assert total_cases == 6
    assert correct_top1 == 6
    assert correct_top3 == 6
    assert top1_accuracy == 100.0
    assert top3_accuracy == 100.0