"""
job_recommender.py
------------------
Rule-based Career Role Recommendation Module for AI Resume Analyzer.
Analyzes candidate skills against a weighted role taxonomy to calculate
match percentages, identify skill gaps, and rank target career profiles.
"""

import os
import json
from typing import Dict, Any, List, Optional
from src.job_matcher import normalize_skill_list


def load_job_roles_database(file_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Loads and parses the standardized job roles database JSON file safely.
    
    Args:
        file_path (Optional[str]): Custom path to job roles JSON database.
        
    Returns:
        List[Dict[str, Any]]: List of parsed job role configurations.
    """
    if file_path is None:
        file_path = os.path.join("data", "job_roles.json")

    if not os.path.exists(file_path):
        print(f"[WARN] Job roles database not found at path: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data.get("roles", [])
            elif isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"[ERROR] Failed to load job roles database ({file_path}): {e}")
        return []


def calculate_role_match(
    candidate_skills: List[str], role_weighted_skills: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculates weighted match score, matched skills, and gap analysis for a single role.
    
    Args:
        candidate_skills (List[str]): List of candidate's raw or normalized skills.
        role_weighted_skills (Dict[str, float]): Role skills mapped to priority weights.
        
    Returns:
        Dict[str, Any]: Match metrics including score, matched skills, and high-priority gaps.
    """
    if not role_weighted_skills or not isinstance(role_weighted_skills, dict):
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "high_priority_gaps": [],
        }

    normalized_candidate = set(normalize_skill_list(candidate_skills))
    total_weight = sum(role_weighted_skills.values())

    if total_weight <= 0.0:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "high_priority_gaps": [],
        }

    matched = []
    missing = []
    high_priority_gaps = []
    earned_weight = 0.0

    for skill, weight in role_weighted_skills.items():
        clean_skill = skill.strip().lower()
        if clean_skill in normalized_candidate:
            matched.append(clean_skill)
            earned_weight += weight
        else:
            missing.append(clean_skill)
            if weight >= 0.7:
                high_priority_gaps.append(clean_skill)

    score = round((earned_weight / total_weight) * 100.0, 2)
    bounded_score = round(max(0.0, min(100.0, score)), 2)

    return {
        "score": bounded_score,
        "matched_skills": sorted(list(set(matched))),
        "missing_skills": sorted(list(set(missing))),
        "high_priority_gaps": sorted(list(set(high_priority_gaps))),
    }


def generate_recommendation_explanation(
    role_name: str,
    match_score: float,
    matched_skills: List[str],
    missing_gaps: List[str]
) -> str:
    """
    Generates a human-readable explanation string for a role recommendation.
    """
    if match_score >= 70.0:
        fit_level = "Strong Match"
    elif match_score >= 45.0:
        fit_level = "Moderate Match"
    else:
        fit_level = "Potential Growth Fit"

    matched_str = ", ".join(matched_skills[:3]) if matched_skills else "None"
    missing_str = ", ".join(missing_gaps[:2]) if missing_gaps else "None"

    return (
        f"{fit_level} ({match_score}%). Strong skill alignment in [{matched_str}]. "
        f"Focus on acquiring [{missing_str}] to boost compatibility."
    )


def recommend_job_roles(
    resume_data: Dict[str, Any],
    roles_db_path: Optional[str] = None,
    top_n: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Main API interface: Analyzes resume skills against all roles and returns ranked recommendations.
    
    Args:
        resume_data (Dict[str, Any]): Candidate profile payload containing skills.
        roles_db_path (Optional[str]): Custom path to job roles JSON database.
        top_n (Optional[int]): Number of top roles to return.
        
    Returns:
        List[Dict[str, Any]]: List of ranked role recommendation objects.
    """
    if not isinstance(resume_data, dict):
        return []

    raw_skills = (
        resume_data.get("skills")
        or resume_data.get("extracted_skills")
        or resume_data.get("key_skills")
        or []
    )
    if not isinstance(raw_skills, list):
        raw_skills = []

    candidate_skills = normalize_skill_list(raw_skills)
    roles = load_job_roles_database(roles_db_path)

    if not roles:
        return []

    recommendations = []

    for role in roles:
        role_id = role.get("role_id", "ROLE_UNK")
        role_name = role.get("role_name", "Unknown Role")
        category = role.get("category", "General")
        weighted_skills = role.get("weighted_skills", {})

        analysis = calculate_role_match(candidate_skills, weighted_skills)
        explanation = generate_recommendation_explanation(
            role_name,
            analysis["score"],
            analysis["matched_skills"],
            analysis["high_priority_gaps"]
        )

        recommendations.append(
            {
                "role_id": role_id,
                "role_name": role_name,
                "category": category,
                "match_score": analysis["score"],
                "matched_skills": analysis["matched_skills"],
                "missing_skills": analysis["missing_skills"],
                "high_priority_gaps": analysis["high_priority_gaps"],
                "explanation": explanation
            }
        )

    # Sort stably descending by match score, ties sorted alphabetically by role name
    recommendations.sort(key=lambda x: (-x["match_score"], x["role_name"]))

    if isinstance(top_n, int) and top_n > 0:
        return recommendations[:top_n]

    return recommendations


def get_top_n_recommendations(
    resume_data: Dict[str, Any],
    top_n: int = 3,
    roles_db_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Convenience wrapper function to retrieve top-N recommendations formatted with explanations.
    """
    return recommend_job_roles(resume_data, roles_db_path=roles_db_path, top_n=top_n)