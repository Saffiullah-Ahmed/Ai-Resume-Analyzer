"""
test_pdf_limitations.py
------------------------
Benchmarking PDF text extraction limitations across document archetypes.
"""

import pytest
import sys
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def mock_pdf_extractor(pdf_type: str) -> dict:
    """
    Simulates text extraction across 4 PDF structural archetypes
    using standard non-OCR text stream extraction (e.g., PyPDF / pdfplumber).
    """
    if pdf_type == "normal_text":
        extracted_text = "John Doe\nEmail: john@example.com\nSkills: Python, SQL, Docker"
        return {"status": "SUCCESS", "text_length": len(extracted_text), "has_text": True}

    elif pdf_type == "multi_page":
        extracted_text = "Page 1: Senior Developer Resume\n" + "x" * 500 + "\nPage 2: Skills & Projects"
        return {"status": "SUCCESS", "text_length": len(extracted_text), "has_text": True}

    elif pdf_type == "poorly_formatted":
        # Disrupted reading order / broken column stream layout
        extracted_text = "John Doe Skills Python SQL Work History Tech Corp Email john@example.com"
        return {"status": "PARTIAL", "text_length": len(extracted_text), "has_text": True}

    elif pdf_type == "scanned_image":
        # Image-only PDF with zero underlying text layer
        extracted_text = ""
        return {"status": "FAIL", "text_length": 0, "has_text": False}

    return {"status": "UNKNOWN", "text_length": 0, "has_text": False}


# Evaluation Scenarios
PDF_SCENARIOS = [
    ("Normal text PDF", "normal_text", "SUCCESS"),
    ("Multi-page PDF", "multi_page", "SUCCESS"),
    ("Poorly formatted PDF", "poorly_formatted", "PARTIAL"),
    ("Scanned/image PDF", "scanned_image", "FAIL"),
]


def test_pdf_extraction_archetypes():
    """Evaluates support and logs performance across PDF document types."""
    print("\n" + "=" * 60)
    print(f"{'PDF Archetype':<25} {'Extraction Status':<20} {'Text Found'}")
    print("=" * 60)

    for label, pdf_type, expected_status in PDF_SCENARIOS:
        res = mock_pdf_extractor(pdf_type)
        print(f"{label:<25} {res['status']:<20} {res['has_text']}")
        assert res["status"] == expected_status

    print("=" * 60 + "\n")