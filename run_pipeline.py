import os
import sys

# Ensure project root is in Python module search path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json
from src.pdf_extractor import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.extractor import parse_resume, save_parsed_resume_to_json


def run_resume_pipeline(pdf_path: str, output_json_path: str = "data/processed/parsed_resume.json"):
    """
    Executes the full resume processing pipeline from PDF input to JSON output.
    """
    print("=" * 60)
    print("      AI RESUME ANALYZER — PROCESSING PIPELINE")
    print("=" * 60)

    # Step 1: Check PDF Existence
    if not os.path.exists(pdf_path):
        print(f"[ERROR] Resume PDF not found at path: {pdf_path}")
        sys.exit(1)

    # Step 2: PDF Text Extraction
    print(f"\n[1/4] Extracting raw text from: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)
    print(f"      -> Extracted {len(raw_text)} characters.")

    # Step 3: Text Preprocessing
    print("\n[2/4] Preprocessing resume text...")
    cleaned_text = clean_text(raw_text)
    print(f"      -> Cleaned text length: {len(cleaned_text)} characters.")

    # Step 4: Structured Information Extraction
    print("\n[3/4] Extracting structured metadata and skills...")
    parsed_data = parse_resume(cleaned_text)

    # Step 5: Export to JSON
    print("\n[4/4] Saving structured output to JSON...")
    json_path = save_parsed_resume_to_json(parsed_data, output_json_path)
    print(f"      -> Output saved to: {json_path}")

    # Display Clean Summary
    print("\n" + "=" * 60)
    print("               EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Name:          {parsed_data.get('name')}")
    print(f"Email:         {parsed_data.get('email')}")
    print(f"Phone:         {parsed_data.get('phone')}")
    print(f"Education:     {len(parsed_data.get('education', []))} entry(ies) found")
    print(f"Skills:        {', '.join(parsed_data.get('skills', [])) if parsed_data.get('skills') else 'None'}")
    print(f"Experience:    {len(parsed_data.get('experience', []))} entry(ies) found")
    print(f"Projects:      {len(parsed_data.get('projects', []))} entry(ies) found")
    print(f"Certifications:{len(parsed_data.get('certifications', []))} entry(ies) found")
    print(f"Languages:     {len(parsed_data.get('languages', []))} entry(ies) found")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    sample_pdf = os.path.join("data", "raw", "sample_resume.pdf")
    run_resume_pipeline(sample_pdf)