# AI Resume Screener

An intelligent resume screening and job compatibility analysis system built with Flask, SQLite, spaCy, and scikit-learn.

## Features
- Upload resume (PDF/DOCX) and compare against a job description
- Compatibility score using TF-IDF + skill overlap
- ATS readiness check
- Skill gap analysis (technical, soft skills, certifications)
- Course recommendations for missing skills
- Analysis history dashboard

## Requirements
- Python 3.10 or 3.11
- SQLite (built-in, no installation required)

## Setup

### 1. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Create database
```bash
python setup_db.py
```

### 4. Run the app
```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Project Structure
```
ai-resume-screener/
├── app.py                  # Main Flask application
├── config.py               # Configuration (DB, upload settings)
├── setup_db.py             # One-time database creation script
├── skills_data.py          # Skills database & course recommendations
├── requirements.txt
├── models/
│   └── database.py         # SQLAlchemy models (User, Resume, Analysis)
├── nlp_engine/
│   ├── ats_scorer.py       # ATS compatibility scoring
│   ├── gap_analyzer.py     # Skill gap detection
│   ├── preprocessor.py     # NLP text preprocessing
│   ├── recommender.py      # Course & improvement recommendations
│   ├── similarity.py       # TF-IDF + cosine similarity scoring
│   ├── skill_extractor.py  # Skill extraction from text
│   └── text_extractor.py   # PDF/DOCX text extraction
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── upload.html
    ├── dashboard.html
    ├── results.html
    └── history.html
```

## Team
Built by a team of three as an academic project.
