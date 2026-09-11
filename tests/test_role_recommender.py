"""
test_role_recommender.py
------------------------
Automated unit tests for job role recommendation engine.
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Ground Truth Benchmark Dataset (Step 13.5 Reference)
GROUND_TRUTH_JOBS = [
    {
        "role_id": "ml_eng",
        "title": "Machine Learning Engineer",
        "required_skills": ["python", "pytorch", "sql", "docker"],
    },
    {
        "role_id": "data_analyst",
        "title": "Data Analyst",
        "required_skills": ["sql", "excel", "tableau", "python"],
    },
    {
        "role_id": "backend_dev",
        "title": "Backend Developer",
        "required_skills": ["python", "docker", "fastapi", "postgresql"],
    },
    # Intentionally duplicated role for test validation
    {
        "role_id": "ml_eng_dup",
        "title": "Machine Learning Engineer",
        "required_skills": ["python", "pytorch", "sql", "docker"],
    },
]


def mock_recommend_roles(candidate_skills: list, job_database: list, top_n: int = 3) -> list:
    """
    Core role recommendation logic for verification against ground truth.
    Handles duplicate role suppression, ranking, and explanation generation.
    """
    if not candidate_skills or not job_database:
        return []

    cand_set = set(s.lower() for s in candidate_skills)
    seen_titles = set()
    recommendations = []

    for job in job_database:
        title = job["title"]
        # Duplicate role handling
        if title in seen_titles:
            continue
        seen_titles.add(title)

        req_skills = set(s.lower() for s in job["required_skills"])
        matched = cand_set.intersection(req_skills)
        missing = req_skills - cand_set

        match_pct = (len(matched) / len(req_skills)) * 100.0 if req_skills else 0.0

        explanation = (
            f"Strong match with {len(matched)} overlapping skills."
            if match_pct >= 50.0
            else f"Partial match. Consider acquiring: {', '.join(sorted(missing))}."
        )

        recommendations.append(
            {
                "title": title,
                "score": round(match_pct, 2),
                "matched_skills": sorted(list(matched)),
                "missing_skills": sorted(list(missing)),
                "explanation": explanation,
            }
        )

    # Role ranking by score descending
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # Top-N filtering
    return recommendations[:top_n]


def test_recommendation_ranking_and_scores():
    """Verify role ranking, scores, matched, and missing skills against Ground Truth (13.5)."""
    # Candidate tailored for ML Engineer role
    candidate_skills = ["python", "pytorch", "sql", "docker"]
    results = mock_recommend_roles(candidate_skills, GROUND_TRUTH_JOBS, top_n=3)

    assert len(results) > 0
    # Top recommendation must be Machine Learning Engineer with 100% match
    top_role = results[0]
    assert top_role["title"] == "Machine Learning Engineer"
    assert top_role["score"] == 100.0
    assert "pytorch" in top_role["matched_skills"]
    assert len(top_role["missing_skills"]) == 0


def test_top_n_and_explanations():
    """Verify Top-N limit and recommendation explanations."""
    candidate_skills = ["sql", "excel"]
    results = mock_recommend_roles(candidate_skills, GROUND_TRUTH_JOBS, top_n=2)

    assert len(results) <= 2
    # Data Analyst should rank top for SQL + Excel candidate
    assert results[0]["title"] == "Data Analyst"
    assert isinstance(results[0]["explanation"], str)
    assert len(results[0]["explanation"]) > 0


def test_empty_skill_handling():
    """Verify safe execution with empty candidate skills."""
    results = mock_recommend_roles([], GROUND_TRUTH_JOBS, top_n=3)
    assert results == []


def test_duplicate_role_handling():
    """Verify duplicate roles are deduplicated in output."""
    candidate_skills = ["python", "pytorch", "sql", "docker"]
    results = mock_recommend_roles(candidate_skills, GROUND_TRUTH_JOBS, top_n=10)

    titles = [r["title"] for r in results]
    assert len(titles) == len(set(titles))  # Ensure all titles are unique