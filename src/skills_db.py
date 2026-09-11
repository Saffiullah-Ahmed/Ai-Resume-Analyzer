from typing import Dict, List

SKILLS_DATABASE = {
    "programming_languages": [
        "Python", "C++", "Java", "JavaScript", "TypeScript", "Go", "Rust", "R", "SQL"
    ],
    "frameworks_libraries": [
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "FastAPI", "Flask", "React"
    ],
    "machine_learning_ai": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "Exploratory Data Analysis", "Statistical Modeling"
    ],
    "data_databases": [
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Data Analysis", "Web Scraping"
    ],
    "devops_cloud": [
        "Docker", "Kubernetes", "AWS", "Amazon Web Services", "GCP", "Azure", "CI/CD", "Linux"
    ],
    "tools_platforms": [
        "Git", "GitHub", "VS Code", "Jupyter Notebooks", "Graphic Design", "Technical Writing"
    ],
    "soft_skills": [
        "Communication", "Leadership", "Problem Solving", "Teamwork"
    ]
}

def get_flattened_skills():
    """Returns a deduplicated, sorted list of all skills across all categories."""
    skills_set = set()
    for category_skills in SKILLS_DATABASE.values():
        for skill in category_skills:
            skills_set.add(skill)
    return sorted(list(skills_set))