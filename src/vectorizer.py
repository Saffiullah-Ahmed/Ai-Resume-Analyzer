"""
src/vectorizer.py
-----------------
TF-IDF vectorizer utility for computing text similarity scores.
"""

from typing import Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Constants
DEFAULT_MATCH_SCORE_SCALE = 100.0


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculates cosine similarity percentage between two raw text documents using TF-IDF.

    Args:
        text1: Raw text input (e.g., candidate resume text).
        text2: Raw text input (e.g., job description text).

    Returns:
        float: Bounded similarity percentage score between 0.0 and 100.0.
    """
    if not text1 or not text2 or not text1.strip() or not text2.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        raw_score = float(sim_matrix[0][0]) * DEFAULT_MATCH_SCORE_SCALE
        return round(max(0.0, min(DEFAULT_MATCH_SCORE_SCALE, raw_score)), 2)
    except Exception:
        # Fallback for edge cases (e.g., documents containing only stop words)
        return 0.0