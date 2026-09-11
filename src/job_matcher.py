import os
import json
from typing import Dict, Any, List


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Safely opens, reads, and parses a JSON file into a Python dictionary.
    
    :param file_path: Absolute or relative path to the JSON file.
    :return: Dictionary containing the parsed JSON data, or empty dict if invalid.
    """
    if not file_path or not isinstance(file_path, str):
        print(f"[ERROR] Invalid file path provided: {file_path}")
        return {}

    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"[WARNING] JSON content in '{file_path}' is not a dictionary/object.")
            return {}

        return data

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON from '{file_path}': {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] Unexpected error reading '{file_path}': {e}")
        return {}


def load_resume_json(file_path: str) -> Dict[str, Any]:
    """
    Loads and validates parsed resume JSON payload.
    
    :param file_path: Path to parsed resume JSON.
    :return: Parsed resume dictionary.
    """
    print(f"[INFO] Loading Resume JSON from: {file_path}")
    return load_json_file(file_path)


def load_job_json(file_path: str) -> Dict[str, Any]:
    """
    Loads and validates parsed job description JSON payload.
    
    :param file_path: Path to parsed job description JSON.
    :return: Parsed job description dictionary.
    """
    print(f"[INFO] Loading Job Description JSON from: {file_path}")
    return load_json_file(file_path)


def normalize_skill(skill: str) -> str:
    """
    Normalizes a single skill string by trimming whitespace and converting to lowercase,
    while keeping special characters intact (e.g., C++, C#, .NET).
    
    :param skill: Raw skill string.
    :return: Normalized skill string.
    """
    if not skill or not isinstance(skill, str):
        return ""
    
    # Strip leading/trailing whitespace and convert to lowercase
    normalized = skill.strip().lower()
    
    # Collapse internal multiple spaces (e.g., "machine   learning" -> "machine learning")
    normalized = " ".join(normalized.split())
    
    return normalized


def normalize_skill_list(skills: List[str]) -> List[str]:
    """
    Normalizes a list of skills and removes duplicates while maintaining relative order.
    
    :param skills: List of raw skill strings.
    :return: List of unique, normalized skill strings.
    """
    if not skills or not isinstance(skills, list):
        return []

    seen = set()
    normalized_list = []

    for item in skills:
        cleaned = normalize_skill(item)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            normalized_list.append(cleaned)

    return normalized_list

def compare_required_skills(resume_skills: List[str], required_job_skills: List[str]) -> Dict[str, List[str]]:
    """
    Compares resume skills against required job skills.
    
    :param resume_skills: List of candidate skills.
    :param required_job_skills: List of required skills from the job description.
    :return: Dictionary with lists of 'matched_skills' and 'missing_skills'.
    """
    normalized_resume = set(normalize_skill_list(resume_skills))
    normalized_required = normalize_skill_list(required_job_skills)

    matched = []
    missing = []

    for skill in normalized_required:
        if skill in normalized_resume:
            matched.append(skill)
        else:
            missing.append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }

def calculate_skill_score(matched_skills: List[str], total_job_skills: List[str]) -> float:
    """
    Calculates the match percentage based on matched skills vs total required/preferred job skills.
    
    :param matched_skills: List of matched skill strings.
    :param total_job_skills: List of total target job skill strings.
    :return: Match percentage rounded to 2 decimal places (0.0 to 100.0).
    """
    normalized_matched = normalize_skill_list(matched_skills)
    normalized_total = normalize_skill_list(total_job_skills)

    if not normalized_total:
        # If no skills are required/specified by the job, treat requirement as satisfied
        return 100.0

    if not normalized_matched:
        return 0.0

    score = (len(normalized_matched) / len(normalized_total)) * 100.0
    return round(score, 2)

def compare_preferred_skills(resume_skills: List[str], preferred_job_skills: List[str]) -> Dict[str, Any]:
    """
    Compares resume skills against preferred/optional job skills and calculates preferred score.
    
    :param resume_skills: List of candidate skills.
    :param preferred_job_skills: List of preferred skills from the job description.
    :return: Dictionary containing 'matched_skills', 'missing_skills', and 'preferred_score'.
    """
    normalized_resume = set(normalize_skill_list(resume_skills))
    normalized_preferred = normalize_skill_list(preferred_job_skills)

    matched = []
    missing = []

    for skill in normalized_preferred:
        if skill in normalized_resume:
            matched.append(skill)
        else:
            missing.append(skill)

    score = calculate_skill_score(matched, normalized_preferred)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "preferred_score": score
    }

def calculate_overall_match_score(
    required_score: float, 
    preferred_score: float, 
    has_preferred_skills: bool = True,
    required_weight: float = 0.80, 
    preferred_weight: float = 0.20
) -> float:
    """
    Calculates the overall weighted match score between 0.0 and 100.0.
    
    :param required_score: Required skill match percentage (0.0 - 100.0).
    :param preferred_score: Preferred skill match percentage (0.0 - 100.0).
    :param has_preferred_skills: Flag indicating whether the job specified preferred skills.
    :param required_weight: Weight given to required skills (default 0.80).
    :param preferred_weight: Weight given to preferred skills (default 0.20).
    :return: Bounded overall match score rounded to 2 decimal places.
    """
    # Safeguard inputs to range [0.0, 100.0]
    req = max(0.0, min(100.0, float(required_score)))
    pref = max(0.0, min(100.0, float(preferred_score)))

    # If the job specifies no preferred skills, delegate 100% weight to required score
    if not has_preferred_skills:
        return round(req, 2)

    # Normalize weights to sum to 1.0 if custom weights are passed
    total_weight = required_weight + preferred_weight
    if total_weight <= 0:
        norm_req_w, norm_pref_w = 0.80, 0.20
    else:
        norm_req_w = required_weight / total_weight
        norm_pref_w = preferred_weight / total_weight

    overall_score = (req * norm_req_w) + (pref * norm_pref_w)
    
    # Ensure final score remains clamped between 0.0 and 100.0
    return round(max(0.0, min(100.0, overall_score)), 2)

def match_resume_to_job(
    resume_input: Any, 
    job_input: Any, 
    required_weight: float = 0.80, 
    preferred_weight: float = 0.20
) -> Dict[str, Any]:
    """
    Orchestrates the complete match process between a resume and a job description.
    Accepts either file paths (str) or pre-loaded dictionaries.
    
    :param resume_input: File path (str) or dictionary of parsed resume.
    :param job_input: File path (str) or dictionary of parsed job description.
    :param required_weight: Weight given to required skills score (default 0.80).
    :param preferred_weight: Weight given to preferred skills score (default 0.20).
    :return: Comprehensive match result dictionary.
    """
    # 1. Resolve Resume Data
    if isinstance(resume_input, str):
        resume_data = load_resume_json(resume_input)
    elif isinstance(resume_input, dict):
        resume_data = resume_input
    else:
        print("[ERROR] Resume input must be a file path string or a dictionary.")
        resume_data = {}

    # 2. Resolve Job Data
    if isinstance(job_input, str):
        job_data = load_job_json(job_input)
    elif isinstance(job_input, dict):
        job_data = job_input
    else:
        print("[ERROR] Job input must be a file path string or a dictionary.")
        job_data = {}

    # Guard clause if either data payload is invalid or empty
    if not resume_data or not job_data:
        return {
            "candidate_name": resume_data.get("name", "Unknown"),
            "job_title": job_data.get("job_title", "Unknown"),
            "overall_match_score": 0.0,
            "required_skills_score": 0.0,
            "preferred_skills_score": 0.0,
            "required_skills": {"matched_skills": [], "missing_skills": []},
            "preferred_skills": {"matched_skills": [], "missing_skills": []},
            "error": "Failed to load resume or job description payload."
        }

    # 3. Extract Raw Skill Lists
    resume_skills = resume_data.get("skills", [])
    required_job_skills = job_data.get("required_skills", [])
    preferred_job_skills = job_data.get("preferred_skills", [])

    # 4. Perform Skill Comparisons
    req_comp = compare_required_skills(resume_skills, required_job_skills)
    pref_comp = compare_preferred_skills(resume_skills, preferred_job_skills)

    # 5. Calculate Sub-Scores
    req_score = calculate_skill_score(req_comp["matched_skills"], required_job_skills)
    pref_score = pref_comp["preferred_score"]

    # 6. Calculate Overall Match Score
    has_preferred = len(preferred_job_skills) > 0
    overall_score = calculate_overall_match_score(
        required_score=req_score,
        preferred_score=pref_score,
        has_preferred_skills=has_preferred,
        required_weight=required_weight,
        preferred_weight=preferred_weight
    )

    # 7. Construct Final Match Report Payload
    match_report = {
        "candidate_name": resume_data.get("name", "Unknown"),
        "job_title": job_data.get("job_title", "Unknown"),
        "overall_match_score": overall_score,
        "required_skills_score": req_score,
        "preferred_skills_score": pref_score if has_preferred else None,
        "required_skills": req_comp,
        "preferred_skills": {
            "matched_skills": pref_comp["matched_skills"],
            "missing_skills": pref_comp["missing_skills"]
        },
        "total_resume_skills_count": len(normalize_skill_list(resume_skills)),
        "total_job_required_count": len(normalize_skill_list(required_job_skills)),
        "total_job_preferred_count": len(normalize_skill_list(preferred_job_skills))
    }

    return match_report

def save_match_report(match_report: Dict[str, Any], output_filename: str = None, output_dir: str = None) -> str:
    """
    Saves the generated match report dictionary to a formatted JSON file.
    
    :param match_report: Dictionary generated by match_resume_to_job().
    :param output_filename: Custom JSON filename (optional).
    :param output_dir: Target directory for reports (optional).
    :return: Filepath where the report was saved, or empty string if failed.
    """
    if not match_report or not isinstance(match_report, dict):
        print("[ERROR] Cannot save invalid or empty match report.")
        return ""

    if output_dir is None:
        output_dir = os.path.join("data", "processed", "match_reports")

    os.makedirs(output_dir, exist_ok=True)

    if not output_filename:
        # Construct clean filename based on candidate and job title
        candidate = match_report.get("candidate_name", "candidate").lower().replace(" ", "_")
        job = match_report.get("job_title", "job").lower().replace(" ", "_")
        output_filename = f"match_{candidate}_{job}.json"

    if not output_filename.endswith(".json"):
        output_filename += ".json"

    file_path = os.path.join(output_dir, output_filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(match_report, f, indent=4)
        print(f"[INFO] Successfully saved match report to: {file_path}")
        return file_path
    except Exception as e:
        print(f"[ERROR] Failed to save match report to '{file_path}': {e}")
        return ""


def run_job_matching_pipeline(
    resume_input: Any, 
    job_input: Any, 
    output_filename: str = None
) -> Dict[str, Any]:
    """
    Master pipeline execution function: matches a resume to a job and saves the report.
    
    :param resume_input: File path (str) or dictionary of parsed resume.
    :param job_input: File path (str) or dictionary of parsed job description.
    :param output_filename: Custom JSON filename for saved output (optional).
    :return: Match report dictionary.
    """
    report = match_resume_to_job(resume_input, job_input)
    
    if "error" not in report:
        saved_path = save_match_report(report, output_filename=output_filename)
        report["saved_report_path"] = saved_path

    return report

def match_resume_against_job_folder(
    resume_input: Any, 
    jobs_dir: str = None
) -> List[Dict[str, Any]]:
    """
    Matches a single resume against all job description JSON files in a directory
    and returns a ranked list of job matches (sorted by overall match score descending).
    
    :param resume_input: File path (str) or dictionary of parsed resume.
    :param jobs_dir: Path to directory containing job description JSON files.
    :return: List of match report dictionaries sorted by overall match score.
    """
    if jobs_dir is None:
        jobs_dir = os.path.join("data", "processed", "job_descriptions")

    if not os.path.exists(jobs_dir):
        print(f"[ERROR] Job descriptions directory not found at: {jobs_dir}")
        return []

    job_files = [f for f in os.listdir(jobs_dir) if f.endswith(".json")]

    if not job_files:
        print(f"[WARNING] No job JSON files found in directory: {jobs_dir}")
        return []

    print(f"[INFO] Found {len(job_files)} job description(s) for batch matching.")
    
    match_results = []
    for filename in job_files:
        job_file_path = os.path.join(jobs_dir, filename)
        report = match_resume_to_job(resume_input, job_file_path)
        
        if "error" not in report:
            match_results.append(report)

    # Sort reports by overall match score descending
    match_results.sort(key=lambda x: x.get("overall_match_score", 0.0), reverse=True)

    return match_results