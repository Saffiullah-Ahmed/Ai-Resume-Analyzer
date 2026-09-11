import os
import json
from datetime import datetime
from src.text_similarity import compute_text_similarity

print("==================================================")
print("     STEP 10.7 — SAVE TEXT SIMILARITY RESULT      ")
print("==================================================")

# 1. Define input and output file paths
resume_path = os.path.join("data", "processed", "parsed_resume.json")
job_path = os.path.join("data", "processed", "job_descriptions", "junior_machine_learning_engineer.json")
output_dir = os.path.join("data", "processed")
output_path = os.path.join(output_dir, "text_similarity_result.json")

# Verify input files exist
if not os.path.exists(resume_path):
    raise FileNotFoundError(f"Resume file missing at: {resume_path}")
if not os.path.exists(job_path):
    raise FileNotFoundError(f"Job file missing at: {job_path}")

# 2. Load Resume
with open(resume_path, "r", encoding="utf-8") as f:
    resume_data = json.load(f)

candidate_name = resume_data.get("name") or resume_data.get("candidate_name") or "Unknown Candidate"
resume_text = (
    resume_data.get("clean_text") or 
    resume_data.get("raw_text") or 
    resume_data.get("text") or 
    ""
)

if not resume_text:
    skills = resume_data.get("skills") or resume_data.get("extracted_skills") or []
    experience = resume_data.get("experience") or resume_data.get("work_experience") or []
    summary = resume_data.get("summary") or ""
    
    skills_str = " ".join(skills) if isinstance(skills, list) else str(skills)
    exp_str = " ".join([str(e) for e in experience]) if isinstance(experience, list) else str(experience)
    
    resume_text = f"{candidate_name} {summary} {skills_str} {exp_str}"

# 3. Load Job Description
with open(job_path, "r", encoding="utf-8") as f:
    job_data = json.load(f)

job_title = job_data.get("job_title", "Unknown Job Title")
job_text = (
    job_data.get("clean_text") or 
    job_data.get("raw_text") or 
    job_data.get("text") or 
    ""
)

if not job_text:
    req_skills = job_data.get("required_skills", [])
    pref_skills = job_data.get("preferred_skills", [])
    desc = job_data.get("description", "")
    
    req_str = " ".join(req_skills) if isinstance(req_skills, list) else str(req_skills)
    pref_str = " ".join(pref_skills) if isinstance(pref_skills, list) else str(pref_skills)
    
    job_text = f"{job_title} {desc} {req_str} {pref_str}"

# 4. Compute Similarity
sim_result = compute_text_similarity(resume_text, job_text)

# 5. Build structured payload
output_payload = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "candidate_name": candidate_name,
    "job_title": job_title,
    "method": sim_result["method"],
    "similarity_score": sim_result["similarity_score"],
    "similarity_percentage": sim_result["similarity_percentage"]
}

# 6. Save payload to JSON
os.makedirs(output_dir, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_payload, f, indent=4)

print(f"Candidate Name       : {candidate_name}")
print(f"Job Title            : {job_title}")
print(f"Method               : {output_payload['method']}")
print(f"Similarity Score     : {output_payload['similarity_score']}")
print(f"Similarity Percentage: {output_payload['similarity_percentage']}%")
print(f"\n[SUCCESS] Results successfully written to: {output_path}")