import json
import os

DEFAULT_TAXONOMY = [
    {
        "role": "AI / Machine Learning Engineer",
        "required_skills": ["python", "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "scikit-learn", "sql"]
    },
    {
        "role": "Data Scientist",
        "required_skills": ["python", "sql", "data analysis", "statistics", "pandas", "numpy", "machine learning", "tableau"]
    },
    {
        "role": "Software Engineer",
        "required_skills": ["python", "java", "javascript", "git", "data structures", "algorithms", "sql", "rest api"]
    },
    {
        "role": "Data Analyst",
        "required_skills": ["excel", "sql", "tableau", "power bi", "python", "data visualization", "communication"]
    },
    {
        "role": "HR / Talent Acquisition Specialist",
        "required_skills": ["communication", "hris", "recruiting", "microsoft office", "employment law", "confidentiality"]
    }
]

def recommend_roles(candidate_skills, top_n=5):
    candidate_skills_set = {str(s).lower().strip() for s in candidate_skills if s} if candidate_skills else set()
    recommendations = []

    for role_entry in DEFAULT_TAXONOMY:
        role_name = role_entry.get("role", "Software Engineer")
        required_skills = role_entry.get("required_skills", [])
        
        req_set = {str(s).lower().strip() for s in required_skills if s}
        matched = candidate_skills_set.intersection(req_set) if candidate_skills_set else set()
        missing = req_set - candidate_skills_set if candidate_skills_set else req_set

        score = (len(matched) / len(req_set)) * 100.0 if (req_set and candidate_skills_set) else 35.0

        recommendations.append({
            "role": role_name,
            "match_score": round(score, 1),
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing))
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_n]