# AI Resume Analyzer & Job Recommendation System — Architecture Documentation

## Complete System Architecture Diagram

```text
User
 ↓
Streamlit UI (app/app.py)
 ↓
Resume / Job Input
 ↓
PDF Extraction (src/pdf_extractor.py)
 ↓
Text Preprocessing (src/text_preprocessor.py)
 ↓
Resume / Job Parsing (src/extractor.py & src/job_parser.py)
 ↓
Skill Extraction (src/skills_db.py)
 ↓
Skill Matching (src/job_matcher.py)
 ↓
TF-IDF Similarity (src/text_similarity.py)
 ↓
Combined Match Score (src/text_similarity.py)
 ↓
Job Role Recommendation (src/job_recommender.py)
 ↓
Results Dashboard (app/ui_components.py & app/app.py)