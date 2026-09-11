import os
import re
import json
from typing import Dict, List, Optional, Any
from src.text_cleaner import clean_text
from src.skills_db import get_flattened_skills

# Flexible regex dictionary for section heading detection
JOB_SECTION_PATTERNS = {
    "summary": [
        r"^job\s+summary$", r"^about\s+the\s+role$", r"^overview$", r"^role\s+overview$", r"^description$"
    ],
    "responsibilities": [
        r"^responsibilities$", r"^key\s+responsibilities$", r"^what\s+you\s+will\s+do$", r"^duties$", r"^essential\s+duties$"
    ],
    "requirements": [
        r"^requirements$", r"^qualifications$", r"^what\s+we\s+are\s+looking\s+for$", r"^minimum\s+qualifications$", r"^required\s+skills$"
    ],
    "preferred": [
        r"^preferred\s+qualifications$", r"^nice\s+to\s+have$", r"^bonus\s+points$", r"^plus$", r"^preferred\s+skills$"
    ],
    "education": [
        r"^education$", r"^academic\s+requirements$", r"^education\s+&\s+experience$"
    ],
    "experience": [
        r"^experience$", r"^work\s+experience$", r"^prior\s+experience$"
    ]
}

EDUCATION_PATTERNS = [
    r"\b(?:bachelor'?s|bachelor|b\.s\.|bs|b\.a\.|ba)\b(?:\s+degree)?",
    r"\b(?:master'?s|master|m\.s\.|ms|m\.a\.|ma)\b(?:\s+degree)?",
    r"\b(?:phd|ph\.d\.|doctorate)\b",
    r"\bcomputer\s+science\b",
    r"\bdata\s+science\b",
    r"\bartificial\s+intelligence\b",
    r"\bsoftware\s+engineering\b",
    r"\binformation\s+technology\b",
    r"\brelated\s+field\b"
]

EXPERIENCE_PATTERNS = [
    r"\b(?:\d+\+|\d+\s*-\s*\d+|\d+)\s*(?:years?|yrs?)\b(?:\s+of\s+experience)?",
    r"\bentry\s*-\s*level\b",
    r"\binternship\s+experience\b",
    r"\bminimum\s+(?:\d+)\s+years?\b"
]


def load_job_description(filepath: str) -> str:
    """Safely reads raw text from a job description text file."""
    if not filepath or not isinstance(filepath, str):
        print("[ERROR] Invalid filepath provided.")
        return ""

    if not os.path.exists(filepath):
        print(f"[ERROR] Job description file not found at: {filepath}")
        return ""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            if not text.strip():
                print(f"[WARNING] Job description file at {filepath} is empty.")
                return ""
            return text
    except Exception as e:
        print(f"[ERROR] Failed to read job description file: {e}")
        return ""


def preprocess_job_text(raw_text: str) -> str:
    """Preprocesses raw job description text by reusing the central clean_text function."""
    return clean_text(raw_text)


def get_job_schema_template() -> Dict[str, Any]:
    """Returns the standardized dictionary structure for parsed job postings."""
    return {
        "job_title": None,
        "company": None,
        "summary": None,
        "responsibilities": [],
        "required_skills": [],
        "preferred_skills": [],
        "education": [],
        "experience": [],
        "raw_text": ""
    }


def extract_job_title(text: str) -> Optional[str]:
    """Extracts job title using heading patterns and line positioning."""
    if not text or not isinstance(text, str):
        return None

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return None

    for line in lines[:5]:
        match = re.search(r"^(?:job\s+title|position|role)\s*:\s*(.+)$", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    first_line = lines[0]
    if len(first_line) < 80 and not re.search(r"\b(summary|overview|about)\b", first_line, re.IGNORECASE):
        return first_line

    return None


def extract_company(text: str) -> Optional[str]:
    """Extracts company name using explicit labels or top-line position markers."""
    if not text or not isinstance(text, str):
        return None

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return None

    for line in lines[:5]:
        match = re.search(r"^(?:company|organization|employer)\s*:\s*(.+)$", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    if len(lines) > 1:
        second_line = lines[1]
        parts = re.split(r"\s*[-|—]\s*", second_line)
        if parts:
            candidate = parts[0].strip()
            if 2 <= len(candidate) <= 60 and not re.search(r"\b(summary|overview|responsibilities)\b", candidate, re.IGNORECASE):
                return candidate

    return None


def detect_job_sections(text: str) -> Dict[str, str]:
    """Splits job description text into logical sections based on common headings."""
    sections: Dict[str, str] = {}
    if not text or not isinstance(text, str):
        return sections

    lines = text.split("\n")
    current_section = "header"
    buffer: List[str] = []

    for line in lines:
        clean_line = line.strip()
        matched_section = None

        if clean_line:
            line_clean_text = re.sub(r"[:\-\#\*]", "", clean_line).strip().lower()
            for sec_name, patterns in JOB_SECTION_PATTERNS.items():
                if any(re.match(pattern, line_clean_text, re.IGNORECASE) for pattern in patterns):
                    matched_section = sec_name
                    break

        if matched_section:
            if buffer:
                sections[current_section] = "\n".join(buffer).strip()
                buffer = []
            current_section = matched_section
        else:
            buffer.append(line)

    if buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections


def extract_responsibilities(sections: Dict[str, str]) -> List[str]:
    """Extracts responsibility items from the responsibilities section."""
    resp_text = sections.get("responsibilities", "")
    if not resp_text:
        return []

    responsibilities: List[str] = []
    lines = resp_text.split("\n")

    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        cleaned = re.sub(r"^[\-\*\•\–\—\>]\s*", "", cleaned).strip()
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", cleaned).strip()

        if cleaned and len(cleaned) > 3:
            responsibilities.append(cleaned)

    return responsibilities


def extract_required_skills(sections: Dict[str, str], full_text: str) -> List[str]:
    """Extracts mandatory/required technical skills."""
    target_text = sections.get("requirements", "")
    if not target_text:
        target_text = full_text

    if not target_text:
        return []

    all_skills = get_flattened_skills()
    found_skills: List[str] = []

    for skill in all_skills:
        escaped_skill = re.escape(skill)
        pattern = r"(?:\b|_)" + escaped_skill + r"(?:\b|_)"
        
        if re.search(pattern, target_text, re.IGNORECASE):
            if skill not in found_skills:
                found_skills.append(skill)

    return sorted(found_skills)


def extract_preferred_skills(sections: Dict[str, str], required_skills: List[str]) -> List[str]:
    """Extracts optional/preferred skills."""
    pref_text = sections.get("preferred", "")
    if not pref_text:
        return []

    all_skills = get_flattened_skills()
    found_preferred: List[str] = []

    for skill in all_skills:
        escaped_skill = re.escape(skill)
        pattern = r"(?:\b|_)" + escaped_skill + r"(?:\b|_)"
        
        if re.search(pattern, pref_text, re.IGNORECASE):
            if skill not in required_skills and skill not in found_preferred:
                found_preferred.append(skill)

    return sorted(found_preferred)


def extract_education_requirements(sections: Dict[str, str], full_text: str) -> List[str]:
    """Extracts education qualifications (degrees, majors)."""
    target_text = sections.get("education", "")
    if not target_text:
        target_text = sections.get("requirements", "")
    if not target_text:
        target_text = full_text

    if not target_text:
        return []

    found_education: List[str] = []
    lines = [line.strip() for line in target_text.split("\n") if line.strip()]

    for line in lines:
        for pattern in EDUCATION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                clean_line = re.sub(r"^[\-\*\•\–\—\>]\s*", "", line).strip()
                if clean_line and clean_line not in found_education:
                    found_education.append(clean_line)
                break

    return found_education


def extract_experience_requirements(sections: Dict[str, str], full_text: str) -> List[str]:
    """Extracts work experience requirements."""
    target_text = sections.get("experience", "")
    if not target_text:
        target_text = sections.get("requirements", "")
    if not target_text:
        target_text = full_text

    if not target_text:
        return []

    found_experience: List[str] = []
    lines = [line.strip() for line in target_text.split("\n") if line.strip()]

    for line in lines:
        for pattern in EXPERIENCE_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                clean_line = re.sub(r"^[\-\*\•\–\—\>]\s*", "", line).strip()
                if clean_line and clean_line not in found_experience:
                    found_experience.append(clean_line)
                break

    return found_experience


def parse_job_description(raw_text: str) -> Dict[str, Any]:
    """
    Main orchestrator that parses raw job description text into structured JSON data.
    """
    job_data = get_job_schema_template()
    if not raw_text or not raw_text.strip():
        return job_data

    cleaned_text = preprocess_job_text(raw_text)
    job_data["raw_text"] = cleaned_text

    # Extract metadata
    job_data["job_title"] = extract_job_title(cleaned_text)
    job_data["company"] = extract_company(cleaned_text)

    # Detect sections
    sections = detect_job_sections(cleaned_text)
    job_data["summary"] = sections.get("summary", None)

    # Extract structured fields
    job_data["responsibilities"] = extract_responsibilities(sections)
    job_data["required_skills"] = extract_required_skills(sections, cleaned_text)
    job_data["preferred_skills"] = extract_preferred_skills(sections, job_data["required_skills"])
    job_data["education"] = extract_education_requirements(sections, cleaned_text)
    job_data["experience"] = extract_experience_requirements(sections, cleaned_text)

    return job_data


def save_parsed_job(parsed_data: Dict[str, Any], output_path: str) -> bool:
    """
    Saves parsed job description dictionary to a JSON file on disk.
    """
    if not parsed_data or not isinstance(parsed_data, dict):
        print("[ERROR] Cannot save invalid or empty job data.")
        return False

    if not output_path or not isinstance(output_path, str):
        print("[ERROR] Invalid output path specified.")
        return False

    try:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=4, ensure_ascii=False)

        print(f"[SUCCESS] Parsed job description saved to: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save parsed job description to {output_path}: {e}")
        return False


def batch_parse_job_descriptions(input_dir: str, output_dir: str) -> List[Dict[str, Any]]:
    """
    Parses all text files in an input directory and saves the extracted JSON records to an output directory.
    """
    if not os.path.exists(input_dir):
        print(f"[ERROR] Input directory does not exist: {input_dir}")
        return []

    os.makedirs(output_dir, exist_ok=True)
    results: List[Dict[str, Any]] = []

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".txt")]
    if not files:
        print(f"[WARNING] No text files found in: {input_dir}")
        return []

    print(f"--- STARTING BATCH PARSING ({len(files)} files) ---")
    for filename in files:
        file_path = os.path.join(input_dir, filename)
        raw_text = load_job_description(file_path)
        
        if not raw_text:
            print(f"[WARNING] Skipping empty or unreadable file: {filename}")
            continue

        parsed = parse_job_description(raw_text)
        results.append(parsed)

        json_filename = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(output_dir, json_filename)
        save_parsed_job(parsed, json_path)

    print(f"--- COMPLETED BATCH PARSING: Successfully processed {len(results)} jobs ---")
    return results

def validate_parsed_job(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates parsed job dictionary content and returns a structure validation report.
    
    :param parsed_data: Dictionary returned by parse_job_description.
    :return: Dictionary containing validation status, score, and missing critical fields.
    """
    report = {
        "is_valid": True,
        "completeness_score": 0.0,
        "missing_fields": [],
        "warnings": []
    }

    if not parsed_data or not isinstance(parsed_data, dict):
        report["is_valid"] = False
        report["missing_fields"].append("all (invalid data object)")
        return report

    critical_fields = ["job_title", "required_skills"]
    optional_fields = ["company", "summary", "responsibilities", "preferred_skills", "education", "experience"]

    total_checks = len(critical_fields) + len(optional_fields)
    passed_checks = 0

    # Validate critical fields
    for field in critical_fields:
        val = parsed_data.get(field)
        if not val:
            report["missing_fields"].append(field)
            report["is_valid"] = False
        else:
            passed_checks += 1

    # Validate optional fields
    for field in optional_fields:
        val = parsed_data.get(field)
        if not val:
            report["warnings"].append(f"Optional field '{field}' is empty.")
        else:
            passed_checks += 1

    report["completeness_score"] = round((passed_checks / total_checks) * 100, 2)
    return report