"""
text_similarity.py
------------------
Provides statistical vectorization (TF-IDF), cosine similarity calculation,
and weighted composite scoring for resume and job description matching.
"""

from typing import List, Tuple, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def vectorize_texts(texts: List[str]) -> Tuple[Any, TfidfVectorizer]:
    """
    Converts a list of text strings into a TF-IDF sparse matrix.

    :param texts: List of raw or cleaned text strings.
    :return: A tuple containing (tfidf_matrix, fitted_vectorizer).
    :raises ValueError: If input is not a non-empty list.
    """
    if not isinstance(texts, list) or not texts:
        raise ValueError("Input 'texts' must be a non-empty list of strings.")

    cleaned_texts = [str(text).strip() if text else "" for text in texts]

    # Custom token pattern to preserve technical terms like C++, C#, .NET, etc.
    # Standard token pattern r'(?u)\b\w+\b' strips out special symbols entirely.
    token_pattern = r"(?u)\b\w[\w\+\#\.]*\b|\b\w+\b"

    # Return empty matrix if all input strings are blank
    if not any(cleaned_texts):
        vectorizer = TfidfVectorizer(
            token_pattern=token_pattern,
            ngram_range=(1, 2),
            stop_words="english",
        )
        return vectorizer.fit_transform(["", ""]), vectorizer

    try:
        vectorizer = TfidfVectorizer(
            token_pattern=token_pattern,
            ngram_range=(1, 2),
            stop_words="english",
            min_df=1,
        )
        tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
    except ValueError:
        # Fallback if stop_words="english" strips all words in a very short input
        vectorizer = TfidfVectorizer(
            token_pattern=token_pattern,
            ngram_range=(1, 2),
            min_df=1,
        )
        tfidf_matrix = vectorizer.fit_transform(cleaned_texts)

    return tfidf_matrix, vectorizer


def calculate_cosine_similarity(vec1: Any, vec2: Any) -> float:
    """
    Calculates cosine similarity between two 2D sparse/dense feature vectors.

    :param vec1: Vector 1 (1xN array).
    :param vec2: Vector 2 (1xN array).
    :return: Cosine similarity score as a float rounded to 4 decimal places (0.0 to 1.0).
    """
    if vec1 is None or vec2 is None:
        return 0.0

    try:
        sim = cosine_similarity(vec1, vec2)[0][0]
        if np.isnan(sim):
            return 0.0
        return float(round(max(0.0, min(1.0, sim)), 4))
    except (IndexError, ValueError):
        return 0.0


def compute_text_similarity(resume_text: str, job_text: str) -> Dict[str, Any]:
    """
    Computes TF-IDF vector similarity between a resume and job description.

    :param resume_text: Candidate resume text string.
    :param job_text: Target job description text string.
    :return: Dictionary containing method name, raw float score, and percentage score.
    """
    if not isinstance(resume_text, str) or not isinstance(job_text, str):
        return {
            "method": "TF-IDF + Cosine Similarity",
            "similarity_score": 0.0,
            "similarity_percentage": 0.0,
        }

    # Guard clause: return 0.0 directly for empty or whitespace-only strings
    if not resume_text.strip() or not job_text.strip():
        return {
            "method": "TF-IDF + Cosine Similarity",
            "similarity_score": 0.0,
            "similarity_percentage": 0.0,
        }

    try:
        tfidf_matrix, _ = vectorize_texts([resume_text, job_text])
        score = calculate_cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        percentage = round(score * 100.0, 2)
    except Exception:
        score = 0.0
        percentage = 0.0

    return {
        "method": "TF-IDF + Cosine Similarity",
        "similarity_score": score,
        "similarity_percentage": percentage,
    }


def calculate_composite_score(
    skill_score: float,
    tfidf_score: float,
    skill_weight: float = 0.60,
    tfidf_weight: float = 0.40,
) -> Dict[str, Any]:
    """
    Combines Skill Match Score and TF-IDF Similarity Score using weighted aggregation.

    :param skill_score: Skill match percentage (0.0 - 100.0).
    :param tfidf_score: TF-IDF similarity percentage (0.0 - 100.0).
    :param skill_weight: Weight allocated to skill match (default 0.60).
    :param tfidf_weight: Weight allocated to TF-IDF similarity (default 0.40).
    :return: Dictionary containing weights and the final composite match score percentage.
    """
    s_score = max(0.0, min(100.0, float(skill_score)))
    t_score = max(0.0, min(100.0, float(tfidf_score)))

    total_weight = skill_weight + tfidf_weight
    if total_weight > 0 and not np.isclose(total_weight, 1.0):
        skill_weight = skill_weight / total_weight
        tfidf_weight = tfidf_weight / total_weight

    composite = (s_score * skill_weight) + (t_score * tfidf_weight)

    return {
        "skill_match_score": round(s_score, 2),
        "tfidf_similarity_score": round(t_score, 2),
        "skill_weight": round(skill_weight, 2),
        "tfidf_weight": round(tfidf_weight, 2),
        "composite_score": round(composite, 2),
    }