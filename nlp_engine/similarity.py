"""
Hybrid Compatibility Scoring:
  - TF-IDF + Cosine Similarity  (text-level)
  - Skill overlap ratio          (skill-level)
  - Weighted combination
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_engine.preprocessor import preprocess_to_string


def _tfidf_cosine_score(resume_text, jd_text):
    proc_r = preprocess_to_string(resume_text)
    proc_j = preprocess_to_string(jd_text)
    if not proc_r.strip() or not proc_j.strip():
        return 0.0
    vec = TfidfVectorizer()
    matrix = vec.fit_transform([proc_r, proc_j])
    sim = cosine_similarity(matrix[0:1], matrix[1:2])
    return float(sim[0][0]) * 100


def _skill_overlap_score(resume_skills, jd_skills):
    r_all = set(resume_skills.get('technical_skills', [])
                + resume_skills.get('soft_skills', [])
                + resume_skills.get('certifications', []))
    j_all = set(jd_skills.get('technical_skills', [])
                + jd_skills.get('soft_skills', [])
                + jd_skills.get('certifications', []))
    if not j_all:
        return 100.0
    overlap = r_all & j_all
    return (len(overlap) / len(j_all)) * 100


def calculate_compatibility_score(resume_text, jd_text,
                                  resume_skills=None, jd_skills=None):
    """
    Weighted hybrid score:
      60 % TF-IDF cosine similarity
      40 % Skill overlap ratio
    """
    tfidf_score = _tfidf_cosine_score(resume_text, jd_text)

    if resume_skills and jd_skills:
        skill_score = _skill_overlap_score(resume_skills, jd_skills)
    else:
        skill_score = tfidf_score  # fallback

    combined = round(0.6 * tfidf_score + 0.4 * skill_score, 2)
    return {
        'overall': min(combined, 100.0),
        'tfidf_score': round(tfidf_score, 2),
        'skill_score': round(skill_score, 2),
    }