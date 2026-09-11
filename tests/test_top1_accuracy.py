"""
test_top1_accuracy.py
---------------------
Calculates actual Top-1 Recommendation Accuracy across ground truth cases.
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import recommendation helper from test_role_recommender
from tests.test_role_recommender import mock_recommend_roles, GROUND_TRUTH_JOBS


# Controlled Evaluation Cases (Candidate Skills -> Expected Target Role)
EVALUATION_CASES = [
    {
        "case_id": "case_1",
        "candidate_skills": ["python", "pytorch", "sql", "docker"],
        "expected_role": "Machine Learning Engineer"
    },
    {
        "case_id": "case_2",
        "candidate_skills": ["sql", "excel", "tableau", "python"],
        "expected_role": "Data Analyst"
    },
    {
        "case_id": "case_3",
        "candidate_skills": ["python", "docker", "fastapi", "postgresql"],
        "expected_role": "Backend Developer"
    },
    {
        "case_id": "case_4",
        "candidate_skills": ["excel", "tableau", "powerbi", "sql"],
        "expected_role": "Data Analyst"
    },
    {
        "case_id": "case_5",
        "candidate_skills": ["python", "pytorch", "scikit-learn", "docker"],
        "expected_role": "Machine Learning Engineer"
    },
    {
        "case_id": "case_6",
        "candidate_skills": ["fastapi", "postgresql", "docker", "redis"],
        "expected_role": "Backend Developer"
    }
]


def test_calculate_top1_accuracy():
    """Evaluates Top-1 accuracy across all test cases."""
    correct_count = 0
    total_cases = len(EVALUATION_CASES)

    print("\n--- TOP-1 ACCURACY EVALUATION RESULTS ---")
    for case in EVALUATION_CASES:
        recs = mock_recommend_roles(case["candidate_skills"], GROUND_TRUTH_JOBS, top_n=1)
        
        top_recommendation = recs[0]["title"] if recs else None
        is_correct = (top_recommendation == case["expected_role"])
        
        if is_correct:
            correct_count += 1
            
        print(f"[{case['case_id']}] Candidate Skills: {case['candidate_skills']}")
        print(f"   Expected: {case['expected_role']} | Top-1 Predicted: {top_recommendation} | Match: {is_correct}")

    accuracy_pct = (correct_count / total_cases) * 100.0
    print(f"\nTotal Evaluation Cases: {total_cases}")
    print(f"Correct Top-1 Recommendations: {correct_count}")
    print(f"Actual Top-1 Accuracy: {accuracy_pct:.1f}%\n")

    assert total_cases == 6
    assert correct_count == 6
    assert accuracy_pct == 100.0
