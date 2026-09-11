import logging
import os

# Set up logging for debugging
logging.basicConfig(
    filename=os.path.join("data", "app_errors.log"),
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ResumeAnalyzer")

class ValidationError(Exception):
    """Custom exception for user-facing input validation errors."""
    pass

def validate_resume_upload(uploaded_file, max_size_mb=5):
    """Cases 1, 2, 3: Validates presence, format, size, and extracted content."""
    # Case 1: No resume uploaded
    if uploaded_file is None:
        raise ValidationError("Please upload a valid PDF resume.")

    # Case 2: Invalid extension
    if not uploaded_file.name.lower().endswith(".pdf"):
        raise ValidationError("Please upload a valid PDF resume. Only .pdf files are accepted.")

    # Check size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValidationError(f"Resume file size exceeds the limit ({max_size_mb} MB). Please upload a smaller PDF.")

def validate_extracted_text(text):
    """Case 3: PDF contains little/no extractable text (scanned image or empty)."""
    if not text or len(text.strip()) < 30:
        raise ValidationError("The uploaded PDF contains little or no extractable text. If it is a scanned image, please convert it to plain text or standard PDF text.")

def validate_parsed_profile(profile):
    """Case 4: Resume parser returns incomplete information."""
    if not isinstance(profile, dict):
        logger.error(f"Malformed parser output type: {type(profile)}")
        raise ValidationError("Failed to parse candidate profile. Please check your resume formatting.")
    
    # Return warnings or handle missing critical fields gracefully
    has_skills = bool(profile.get("skills"))
    has_contact = bool(profile.get("email") or profile.get("phone") or profile.get("name"))
    
    if not has_skills and not has_contact:
        logger.warning("Parser returned incomplete profile info (no skills or contact).")
        return "⚠️ Resume parser returned limited candidate information. Some metrics may be less accurate."
    return None

def validate_job_description(final_jd_text, min_length=20):
    """Cases 5 & 6: Missing or overly short job description."""
    # Case 5: No job description
    if not final_jd_text or not final_jd_text.strip():
        raise ValidationError("Please upload or paste a job description before running analysis.")

    # Case 6: Job description too short
    if len(final_jd_text.strip()) < min_length:
        raise ValidationError(f"Job description is too short ({len(final_jd_text.strip())} chars). Minimum required length is {min_length} characters.")

def sanitize_backend_output(output, expected_keys=None):
    """Case 8 & 9: Malformed backend output/JSON defense."""
    if output is None:
        logger.error("Backend function returned None.")
        raise ValidationError("Analysis engine returned an empty response. Please try again.")

    if expected_keys and isinstance(output, dict):
        for key in expected_keys:
            if key not in output:
                logger.warning(f"Missing expected key '{key}' in backend response.")

    return output