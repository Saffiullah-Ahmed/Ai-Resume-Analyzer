import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

PHONE_REGEX = re.compile(
    r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
)
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def parse_resume(text):
    profile = {
        "name": "N/A",
        "email": "N/A",
        "phone": "N/A",
        "skills": []
    }
    if not text:
        return profile

    # Extract Email
    emails = EMAIL_REGEX.findall(text)
    if emails:
        profile["email"] = emails[0]

    # Extract Phone
    phones = PHONE_REGEX.findall(text)
    if phones:
        valid_phones = [p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]
        if valid_phones:
            profile["phone"] = valid_phones[0]

    # Extract Name via spaCy or first line fallback
    if nlp:
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                profile["name"] = ent.text.strip()
                break

    if profile["name"] == "N/A":
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            profile["name"] = lines[0]

    # Simple Skill Extraction Fallback
    skill_keywords = [
        "python", "c++", "java", "machine learning", "deep learning", 
        "computer vision", "nlp", "sql", "tensorflow", "pytorch", "streamlit"
    ]
    lower_text = text.lower()
    found_skills = [s for s in skill_keywords if s in lower_text]
    profile["skills"] = list(set(found_skills))

    return profile