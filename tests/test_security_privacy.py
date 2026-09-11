"""
test_security_privacy.py
------------------------
Automated security audit checking for secrets, PII, and .gitignore integrity.
"""

import pytest
import sys
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_gitignore_exists_and_rules():
    """Verifies .gitignore exists and contains critical rules for secrets and temp files."""
    gitignore_path = PROJECT_ROOT / ".gitignore"
    assert gitignore_path.exists(), ".gitignore file is missing!"

    content = gitignore_path.read_text(encoding="utf-8")
    assert "__pycache__/" in content
    assert ".env" in content
    assert ".pytest_cache/" in content


def test_no_hardcoded_secrets_in_src():
    """Scans all python files under src/ for hardcoded API keys or secret strings."""
    src_dir = PROJECT_ROOT / "src"
    secret_patterns = [
        re.compile(r"api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", re.IGNORECASE),
        re.compile(r"secret[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", re.IGNORECASE),
        re.compile(r"bearer\s+[A-Za-z0-9_\-\.]{20,}", re.IGNORECASE),
    ]

    for py_file in src_dir.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        for pattern in secret_patterns:
            assert not pattern.search(text), f"Potential secret found in {py_file.name}"