# AI Resume Analyzer & Job Recommendation System

## Overview
The **AI Resume Analyzer & Job Recommendation System** is an end-to-end NLP-driven web application designed to evaluate candidate resumes against target job descriptions. The system parses structural resume text, extracts normalized technical skills, computes candidate-job alignment using a hybrid scoring algorithm, and recommends top-matching job roles through an interactive dashboard.

---

## Problem Statement
Traditional Applicant Tracking Systems (ATS) often rely on rigid keyword matching or opaque filtering, leading to high false-rejection rates for qualified candidates. Job seekers frequently struggle to identify specific skill gaps required for target roles. This system addresses these challenges by combining structural skill overlap analysis with TF-IDF text vectorization to deliver transparent match scores, missing skill insights, and target role recommendations.

---

## Features
* **Resume PDF Analysis:** Native parsing and text extraction from single/multi-page text-based PDF and TXT documents.
* **Resume Parsing:** Automated extraction of candidate contact info, work history, and structured skill sections.
* **Skill Extraction:** Exact-match dictionary lookup and regex normalization across a predefined technical taxonomy.
* **Job Description Parsing:** Standardized tokenization and skill set extraction from target job descriptions.
* **Skill Match Calculation:** Set-based overlap analysis evaluating exact candidate-to-job skill coverage.
* **TF-IDF Text Similarity:** Vector cosine similarity scoring using Scikit-Learn TF-IDF vectorizers.
* **Combined Match Score:** Weighted composite scoring mechanism blending explicit skill overlap (70%) with overall text similarity (30%).
* **Missing Skill Detection:** Real-time identification of critical target skills missing from the candidate resume.
* **Job-Role Recommendations:** Algorithmic ranking of candidate profiles against target career path benchmarks.
* **Batch Job Matching:** Scalable evaluation of candidate profiles across multiple job listings simultaneously.
* **Professional Streamlit Dashboard:** Clean user interface with metric summary cards, interactive charts, and sidebar configuration controls.

---

## Technology Stack
* **Language:** Python 3.12
* **Frontend UI:** Streamlit
* **Data Processing & NLP:** Scikit-Learn, NumPy, Pandas
* **Document Parsing:** PyPDF / PDFPlumber
* **Testing Suite:** Pytest

---

## Architecture Pipeline