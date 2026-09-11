import os
import re
from typing import Dict, Any, List, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text: str) -> str:
    """Cleans and standardizes raw text strings."""
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'[^a-z0-9\s#\+\.]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def calculate_tfidf_similarity(text1: str, text2: str) -> float:
    """Calculates cosine similarity score between two raw text inputs."""
    clean_t1 = clean_text(text1)
    clean_t2 = clean_text(text2)

    if not clean_t1 or not clean_t2:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([clean_t1, clean_t2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity * 100.0)
    except Exception:
        return 0.0


def calculate_skill_match_score(resume_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
    """Evaluates direct skill alignment and identifies gaps."""
    r_skills = {str(s).strip().lower() for s in resume_skills if s}
    q_skills = {str(s).strip().lower() for s in required_skills if s}

    if not q_skills:
        return {
            "score": 100.0,
            "matched_skills": list(r_skills),
            "missing_skills": []
        }

    matched = r_skills.intersection(q_skills)
    missing = q_skills.difference(r_skills)

    score = (len(matched) / len(q_skills)) * 100.0

    return {
        "score": float(score),
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing))
    }


def match_resume_to_job(
    resume_input: Union[str, Dict[str, Any]], 
    job_input: Union[str, Dict[str, Any]], 
    skill_weight: float = 0.6, 
    tfidf_weight: float = 0.4
) -> Dict[str, Any]:
    """Matches parsed or raw resume data to a job description."""
    # 1. Safely resolve resume data structure and text content
    if isinstance(resume_input, dict):
        resume_data = resume_input
    elif isinstance(resume_input, str):
        if os.path.exists(resume_input):
            # Fallback for file path strings
            with open(resume_input, "r", encoding="utf-8", errors="ignore") as f:
                resume_data = {"raw_text": f.read()}
        else:
            resume_data = {"raw_text": resume_input}
    else:
        resume_data = {}

    # 2. Safely resolve job data structure and text content
    if isinstance(job_input, dict):
        job_data = job_input
    elif isinstance(job_input, str):
        if os.path.exists(job_input):
            # Fallback for file path strings
            with open(job_input, "r", encoding="utf-8", errors="ignore") as f:
                job_data = {"raw_text": f.read()}
        else:
            job_data = {"raw_text": job_input}
    else:
        job_data = {}

    # Extract text and skill structures reliably
    resume_text = str(resume_data.get("raw_text") or resume_data.get("text") or "")
    job_text = str(job_data.get("raw_text") or job_data.get("text") or "")

    resume_skills = resume_data.get("skills", [])
    required_skills = job_data.get("required_skills") or job_data.get("skills", [])

    # Compute individual scores
    skill_match_res = calculate_skill_match_score(resume_skills, required_skills)
    similarity_score = calculate_tfidf_similarity(resume_text, job_text)

    # Calculate weighted composite score
    skill_score = skill_match_res["score"]
    overall_match_score = (skill_score * skill_weight) + (similarity_score * tfidf_weight)

    candidate_name = (
        resume_data.get("name") or 
        resume_data.get("candidate_name") or 
        "Candidate"
    )

    return {
        "candidate_name": candidate_name,
        "overall_match_score": round(overall_match_score, 2),
        "required_skills_score": round(skill_score, 2),
        "similarity_score": round(similarity_score, 2),
        "matched_skills": skill_match_res["matched_skills"],
        "missing_skills": skill_match_res["missing_skills"]
    }


def run_job_matching_pipeline(
    resume_input: Union[str, Dict[str, Any]], 
    job_input: Union[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """Pipeline execution interface used by app.py."""
    return match_resume_to_job(resume_input, job_input)