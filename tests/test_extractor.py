"""
test_extractor.py
------------------
Automated unit tests for src/extractor.py (Resume Parsing).
"""

import pytest
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.extractor as extractor_module


def _get_extraction_function():
    """Dynamically fetch the primary extraction function from src.extractor."""
    possible_names = [
        "extract_resume_data",
        "extract_resume_info",
        "parse_resume",
        "extract_skills",
        "extract_fields",
    ]
    for name in possible_names:
        if hasattr(extractor_module, name):
            return getattr(extractor_module, name)

    # Fallback to class if implemented as a parser class
    if hasattr(extractor_module, "ResumeExtractor"):
        instance = extractor_module.ResumeExtractor()
        for method in ["extract", "parse", "run"]:
            if hasattr(instance, method):
                return getattr(instance, method)

    pytest.fail("No valid extraction function or class found in src/extractor.py")


def test_synthetic_resume_a_extraction():
    extract_fn = _get_extraction_function()
    resume_path = PROJECT_ROOT / "data" / "raw" / "eval_resumes" / "resume_a_ml.txt"

    with open(resume_path, "r", encoding="utf-8") as f:
        text = f.read()

    extracted = extract_fn(text)

    # Validate output structure (handles list or dict returns)
    if isinstance(extracted, dict):
        skills = extracted.get("skills", extracted.get("extracted_skills", []))
    elif isinstance(extracted, (list, set)):
        skills = list(extracted)
    else:
        skills = []

    skills_lower = [str(s).lower() for s in skills]

    # Core assertion checks
    assert any("python" in s for s in skills_lower)
    assert any("pytorch" in s for s in skills_lower)


def test_empty_resume_extraction():
    extract_fn = _get_extraction_function()
    extracted = extract_fn("")
    assert extracted is not None