"""
test_config.py
--------------
Validates integrity and consistency of centralized configuration settings.
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    WEIGHT_SKILL_MATCH,
    WEIGHT_TFIDF_SIMILARITY,
    DATA_DIR,
    ROLE_DEFINITIONS,
    DEFAULT_TOP_N_RECOMMENDATIONS,
)


def test_config_weights_and_paths():
    """Verifies score weights sum to 1.0 and required directories exist."""
    assert round(WEIGHT_SKILL_MATCH + WEIGHT_TFIDF_SIMILARITY, 2) == 1.00
    assert DATA_DIR.exists()
    assert DEFAULT_TOP_N_RECOMMENDATIONS > 0


def test_config_role_definitions():
    """Verifies role definitions contain required schema fields."""
    assert len(ROLE_DEFINITIONS) >= 3
    for role in ROLE_DEFINITIONS:
        assert "role_id" in role
        assert "title" in role
        assert "required_skills" in role
        assert isinstance(role["required_skills"], list)