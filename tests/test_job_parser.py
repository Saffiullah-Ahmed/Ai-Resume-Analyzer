"""
test_job_parser.py
------------------
Automated unit tests for src/job_parser.py.
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.job_parser as job_parser_module


def _get_job_parse_function():
    """Dynamically fetch job parsing function from src.job_parser."""
    possible_names = ["parse_job_description", "parse_jd", "extract_job_skills", "parse_job"]
    for name in possible_names:
        if hasattr(job_parser_module, name):
            return getattr(job_parser_module, name)

    if hasattr(job_parser_module, "JobParser"):
        instance = job_parser_module.JobParser()
        for method in ["parse", "extract", "run"]:
            if hasattr(instance, method):
                return getattr(instance, method)

    pytest.fail("No valid parsing function found in src/job_parser.py")


def test_job_parser_eval_file():
    parse_fn = _get_job_parse_function()
    job_path = PROJECT_ROOT / "data" / "raw" / "eval_jobs" / "job_ml_engineer.txt"

    with open(job_path, "r", encoding="utf-8") as f:
        text = f.read()

    parsed = parse_fn(text)
    assert parsed is not None


def test_empty_job_description():
    parse_fn = _get_job_parse_function()
    parsed = parse_fn("")
    assert parsed is not None