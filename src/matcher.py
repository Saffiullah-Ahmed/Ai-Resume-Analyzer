import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_tfidf_similarity(text1: str, text2: str) -> float:
    """Calculates TF-IDF cosine similarity between full resume and full job description."""
    if not text1 or not text2 or not text1.strip() or not text2.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words='english',
        token_pattern=r'(?u)\b\w+\b',
        ngram_range=(1, 2)
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(sim * 100)
    except Exception:
        return 0.0

def calculate_job_match(resume_text: str, parsed_resume: dict, job_text: str, parsed_job: dict = None) -> dict:
    """Computes TF-IDF against full job description text and calculates skill gaps."""
    parsed_job = parsed_job or {}
    
    # 1. Compare FULL resume text against FULL job description text
    tfidf_score = calculate_tfidf_similarity(resume_text, job_text)
    
    # 2. Skill Extraction & Set Analysis
    resume_skills = set([s.lower() for s in parsed_resume.get("skills", [])])
    req_skills = set([s.lower() for s in parsed_job.get("required_skills", [])])
    pref_skills = set([s.lower() for s in parsed_job.get("preferred_skills", [])])
    
    # Fallback skill extraction from raw text if parsed dictionary is empty
    if not req_skills:
        default_keywords = [
            "python", "sql", "java", "scikit-learn", "pandas", "numpy", 
            "tensorflow", "pytorch", "flask", "django", "streamlit", 
            "postgresql", "docker", "aws", "git", "nlp", "rest apis"
        ]
        job_lower = job_text.lower()
        req_skills = set([k for k in default_keywords if k in job_lower])

    # 3. Compute Skill Sets
    matched_skills = resume_skills.intersection(req_skills.union(pref_skills))
    missing_skills = req_skills.difference(resume_skills)
    
    req_match_pct = (len(resume_skills.intersection(req_skills)) / len(req_skills) * 100) if req_skills else 100.0
    pref_match_pct = (len(resume_skills.intersection(pref_skills)) / len(pref_skills) * 100) if pref_skills else 100.0
    
    # 4. Overall Weighted Score (70% Skill Overlap + 30% TF-IDF Similarity)
    skill_score = (0.7 * req_match_pct) + (0.3 * pref_match_pct)
    overall_score = (0.3 * tfidf_score) + (0.7 * skill_score)
    
    return {
        "overall_match_score": min(round(overall_score, 1), 100.0),
        "tfidf_similarity": round(tfidf_score, 1),
        "required_skill_match_pct": round(req_match_pct, 1),
        "preferred_skill_match_pct": round(pref_match_pct, 1),
        "matched_skills": [s.title() for s in matched_skills],
        "missing_skills": [s.title() for s in missing_skills]
    }