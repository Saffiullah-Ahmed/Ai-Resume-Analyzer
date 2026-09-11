"""
src/config.py
-------------
Centralized application configuration settings and pipeline constants.
"""

from pathlib import Path

# Project Root Directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data & Output Directories
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure runtime directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Composite Match Score Weights (Must sum to 1.0)
WEIGHT_SKILL_MATCH = 0.70
WEIGHT_TFIDF_SIMILARITY = 0.30

# Recommendation Engine Defaults
DEFAULT_TOP_N_RECOMMENDATIONS = 3
MAX_TOP_N_RECOMMENDATIONS = 10
MATCH_THRESHOLD_HIGH = 50.0

# Supported Skill Extraction Taxonomy / Vocabulary
DEFAULT_SKILL_VOCABULARY = {
    "python", "pytorch", "sql", "docker", "fastapi", 
    "postgresql", "excel", "tableau", "powerbi", 
    "scikit-learn", "pandas", "numpy", "aws", 
    "javascript", "react", "nodejs", "git", "redis"
}

# Default Ground Truth Target Roles
ROLE_DEFINITIONS = [
    {
        "role_id": "ml_eng",
        "title": "Machine Learning Engineer",
        "required_skills": ["python", "pytorch", "sql", "docker"],
    },
    {
        "role_id": "data_analyst",
        "title": "Data Analyst",
        "required_skills": ["sql", "excel", "tableau", "python"],
    },
    {
        "role_id": "backend_dev",
        "title": "Backend Developer",
        "required_skills": ["python", "docker", "fastapi", "postgresql"],
    },
]

# UI & Application Settings
APP_TITLE = "AI Resume Analyzer & Job Matcher"
APP_ICON = "📄"
MAX_FILE_SIZE_MB = 5