import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.text_preprocessor import preprocess_text

def calculate_tfidf_similarity(text1: str, text2: str) -> float:
    """Calculates TF-IDF cosine similarity between two raw or preprocessed texts."""
    clean1 = preprocess_text(text1) if text1 else ""
    clean2 = preprocess_text(text2) if text2 else ""
    
    if not clean1.strip() or not clean2.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([clean1, clean2])
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(sim * 100)

def calculate_job_match(resume_text: str, parsed_resume: dict, parsed_job: dict) -> dict:
    """
    Computes TF-IDF text similarity and skill gap match scores 
    between candidate resume and target job description.
    """
    # 1. TF-IDF Similarity
    tfidf_score = calculate_tfidf_similarity(resume_text, parsed_job.get("title", "") + " " + " ".join(parsed_job.get("required_skills", [])))
    
    # 2. Extract Skills
    resume_skills = set([s.lower() for s in parsed_resume.get("skills", [])])
    req_skills = set([s.lower() for s in parsed_job.get("required_skills", [])])
    pref_skills = set([s.lower() for s in parsed_job.get("preferred_skills", [])])
    
    # Fallback keyword extraction from JD if no structured skills parsed
    if not req_skills and not pref_skills:
        req_skills = resume_skills  # Fallback for empty skill lists
        
    # 3. Compute Matches
    matched_skills = resume_skills.intersection(req_skills.union(pref_skills))
    missing_skills = req_skills.difference(resume_skills)
    
    req_match_pct = (len(resume_skills.intersection(req_skills)) / len(req_skills) * 100) if req_skills else 100.0
    pref_match_pct = (len(resume_skills.intersection(pref_skills)) / len(pref_skills) * 100) if pref_skills else 100.0
    
    # 4. Overall Weighted Score
    overall_score = (0.4 * tfidf_score) + (0.4 * req_match_pct) + (0.2 * pref_match_pct)
    
    return {
        "overall_match_score": min(round(overall_score, 1), 100.0),
        "tfidf_similarity": round(tfidf_score, 1),
        "required_skill_match_pct": round(req_match_pct, 1),
        "preferred_skill_match_pct": round(pref_match_pct, 1),
        "matched_skills": [s.title() for s in matched_skills],
        "missing_skills": [s.title() for s in missing_skills]
    }