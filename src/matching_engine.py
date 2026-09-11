"""
matching_engine.py
------------------
Main evaluation interface combining Step 9 (Deterministic Skill Matching)
and Step 10 (TF-IDF Similarity) into a unified matching payload and text report.
"""

from typing import Dict, Any, List
from src.job_matcher import (
    compare_required_skills,
    compare_preferred_skills,
    calculate_overall_match_score,
)
from src.text_similarity import compute_text_similarity, calculate_composite_score


def _extract_skill_list(data: Dict[str, Any], keys: List[str]) -> List[str]:
    """Helper utility to extract clean skill strings across varying JSON key structures."""
    for key in keys:
        val = data.get(key)
        if isinstance(val, list) and len(val) > 0:
            return [str(s).strip() for s in val]
        elif isinstance(val, dict):
            extracted = []
            for sub_list in val.values():
                if isinstance(sub_list, list):
                    extracted.extend([str(s).strip() for s in sub_list])
            if extracted:
                return extracted
    return []


def match_resume_to_job(
    resume_data: Dict[str, Any],
    job_data: Dict[str, Any],
    skill_weight: float = 0.60,
    tfidf_weight: float = 0.40,
) -> Dict[str, Any]:
    """
    Executes the full hybrid matching pipeline for a given candidate resume and job description.

    :param resume_data: Parsed candidate resume dictionary.
    :param job_data: Parsed job description dictionary.
    :param skill_weight: Weight assigned to skill matching score.
    :param tfidf_weight: Weight assigned to TF-IDF similarity score.
    :return: Comprehensive dictionary payload containing detailed scores and metadata.
    """
    if not isinstance(resume_data, dict) or not isinstance(job_data, dict):
        raise TypeError("Both resume_data and job_data must be valid dictionaries.")

    candidate_name = (
        resume_data.get("name")
        or resume_data.get("candidate_name")
        or "Unknown Candidate"
    )
    job_title = job_data.get("job_title", "Unknown Job Title")

    # Step 9 Integration: Skill Matching
    resume_skills = _extract_skill_list(
        resume_data, ["skills", "extracted_skills", "key_skills"]
    )
    req_skills = _extract_skill_list(
        job_data, ["required_skills", "mandatory_skills", "skills"]
    )
    pref_skills = _extract_skill_list(
        job_data, ["preferred_skills", "optional_skills", "nice_to_have"]
    )

    req_match = compare_required_skills(resume_skills, req_skills)
    pref_match = compare_preferred_skills(resume_skills, pref_skills)

    matched_req = req_match.get("matched_required") or req_match.get("matched_skills") or []
    missing_req = req_match.get("missing_required") or req_match.get("missing_skills") or []
    matched_pref = pref_match.get("matched_preferred") or pref_match.get("matched_skills") or []
    missing_pref = pref_match.get("missing_preferred") or pref_match.get("missing_skills") or []

    matched_skills = sorted(list(set(matched_req + matched_pref)))
    missing_skills = sorted(list(set(missing_req + missing_pref)))

    # Calculate Skill Match Score
    try:
        skill_score = calculate_overall_match_score(
            resume_skills, req_skills, pref_skills
        )
    except Exception:
        skill_score = 0.0

    # Fallback score calculation if calculate_overall_match_score returned 0.0 despite matches
    total_job_skills = len(set(req_skills + pref_skills))
    if skill_score == 0.0 and total_job_skills > 0:
        skill_score = round((len(matched_skills) / total_job_skills) * 100.0, 2)

    # Step 10 Integration: TF-IDF Text Similarity
    raw_resume_text = (
        resume_data.get("clean_text")
        or resume_data.get("raw_text")
        or resume_data.get("text")
        or ""
    )
    if not raw_resume_text.strip():
        summary = resume_data.get("summary", "")
        skills_str = " ".join(resume_skills) if isinstance(resume_skills, list) else str(resume_skills)
        resume_text = f"{summary} {skills_str}".strip()
    else:
        resume_text = raw_resume_text.strip()

    raw_job_text = (
        job_data.get("clean_text")
        or job_data.get("raw_text")
        or job_data.get("text")
        or ""
    )
    if not raw_job_text.strip():
        desc = job_data.get("description", "")
        all_job_skills = req_skills + pref_skills
        skills_str = " ".join(all_job_skills) if isinstance(all_job_skills, list) else str(all_job_skills)
        job_text = f"{desc} {skills_str}".strip()
    else:
        job_text = raw_job_text.strip()

    tfidf_result = compute_text_similarity(resume_text, job_text)
    tfidf_score = tfidf_result.get("similarity_percentage", 0.0)

    # Hybrid Composite Calculation
    composite = calculate_composite_score(
        skill_score=skill_score,
        tfidf_score=tfidf_score,
        skill_weight=skill_weight,
        tfidf_weight=tfidf_weight,
    )

    return {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "skill_matching": {
            "score_percentage": skill_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_matched": len(matched_skills),
        },
        "text_similarity": {
            "method": tfidf_result["method"],
            "raw_score": tfidf_result["similarity_score"],
            "score_percentage": tfidf_result["similarity_percentage"],
        },
        "composite_score": {
            "final_percentage": composite["composite_score"],
            "skill_weight": composite["skill_weight"],
            "tfidf_weight": composite["tfidf_weight"],
        },
    }


def generate_match_report(evaluation: Dict[str, Any]) -> str:
    """
    Formats the evaluation dict into a clean human-readable text summary.
    """
    candidate = evaluation.get("candidate_name", "N/A")
    job = evaluation.get("job_title", "N/A")

    skill_info = evaluation.get("skill_matching", {})
    text_info = evaluation.get("text_similarity", {})
    comp_info = evaluation.get("composite_score", {})

    matched = skill_info.get("matched_skills", [])
    missing = skill_info.get("missing_skills", [])

    matched_str = "\n".join([f"  - {s}" for s in matched]) if matched else "  - None"
    missing_str = "\n".join([f"  - {s}" for s in missing]) if missing else "  - None"

    s_weight = int(comp_info.get("skill_weight", 0.6) * 100)
    t_weight = int(comp_info.get("tfidf_weight", 0.4) * 100)

    return f"""
==================================================
                 JOB MATCH REPORT                 
==================================================

Candidate Name : {candidate}
Job Position   : {job}

SKILL MATCHING ANALYSIS
-----------------------
Matched Skills:
{matched_str}

Missing Skills:
{missing_str}

Skill Match Score: {skill_info.get('score_percentage', 0.0)}%

TEXT SIMILARITY ANALYSIS
------------------------
Method           : {text_info.get('method', 'TF-IDF + Cosine Similarity')}
Similarity Score : {text_info.get('score_percentage', 0.0)}%

FINAL EVALUATION
----------------
Overall Match    : {comp_info.get('final_percentage', 0.0)}%
Scoring Model    : Skill Match ({s_weight}%) + Text Similarity ({t_weight}%)
==================================================
""".strip()