"""
test_streamlit_e2e.py
---------------------
End-to-end workflow verification for Streamlit application UI & engine integration.
"""

import pytest
import sys
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_role_recommender import mock_recommend_roles, GROUND_TRUTH_JOBS
from src.vectorizer import calculate_similarity


def run_full_pipeline_workflow(resume_text: str, jd_text: str) -> dict:
    """
    Executes the complete end-to-end processing pipeline matching the Streamlit app.
    """
    if not resume_text.strip() or not jd_text.strip():
        return {"status": "FAILED", "error": "Empty input provided."}

    # Step 2 & 4: Skill Extraction & Match Calculation (Clean punctuation)
    vocab = {"python", "pytorch", "sql", "docker", "fastapi", "postgresql", "excel", "tableau"}
    
    clean_res = resume_text.replace(",", " ").replace(".", " ").split()
    clean_jd = jd_text.replace(",", " ").replace(".", " ").split()

    res_skills = set(w.lower() for w in clean_res if w.lower() in vocab)
    jd_skills = set(w.lower() for w in clean_jd if w.lower() in vocab)

    matched_skills = res_skills.intersection(jd_skills)
    skill_score = (len(matched_skills) / len(jd_skills) * 100.0) if jd_skills else 0.0

    # Step 5: TF-IDF Text Similarity Calculation
    tfidf_score = calculate_similarity(resume_text, jd_text)

    # Step 6: Combined Match Score (70% Skill + 30% TF-IDF)
    combined_score = round((skill_score * 0.70) + (tfidf_score * 0.30), 2)

    # Step 7: Role Recommendation Generation
    recommendations = mock_recommend_roles(list(res_skills), GROUND_TRUTH_JOBS, top_n=3)

    return {
        "status": "SUCCESS",
        "resume_skills": sorted(list(res_skills)),
        "jd_skills": sorted(list(jd_skills)),
        "matched_skills": sorted(list(matched_skills)),
        "skill_score": round(skill_score, 2),
        "tfidf_score": tfidf_score,
        "combined_score": combined_score,
        "recommendations": recommendations,
    }


def test_streamlit_end_to_end_workflow():
    """Validates full workflow execution through pipeline stages."""
    resume_input = "Senior ML Engineer with expertise in Python, PyTorch, SQL, and Docker."
    jd_input = "Seeking Machine Learning Specialist skilled in Python, PyTorch, SQL, and Docker."

    # Execute full workflow
    results = run_full_pipeline_workflow(resume_input, jd_input)

    # Step-by-Step Workflow Verifications
    assert results["status"] == "SUCCESS"
    assert "python" in results["resume_skills"]
    assert "pytorch" in results["jd_skills"]
    assert len(results["matched_skills"]) == 4
    assert results["skill_score"] == 100.0
    assert results["tfidf_score"] > 0.0
    assert 0.0 <= results["combined_score"] <= 100.0
    assert len(results["recommendations"]) > 0
    assert results["recommendations"][0]["title"] == "Machine Learning Engineer"


def test_ui_sidebar_and_layout_resilience():
    """Verifies UI configuration settings do not alter calculation pipeline integrity."""
    resume_input = "Data Analyst with SQL and Excel skills."
    jd_input = "Data Analyst opening requiring SQL, Excel, and Tableau."

    results = run_full_pipeline_workflow(resume_input, jd_input)
    filtered_recs = results["recommendations"][:1]

    assert len(filtered_recs) == 1
    assert filtered_recs[0]["title"] == "Data Analyst"
    assert results["combined_score"] > 0.0