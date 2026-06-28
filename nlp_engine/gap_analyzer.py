"""
Gap Detection — identifies missing skills, weak areas, severity levels.
"""


def _match_rate(matched, total):
    return (len(matched) / total * 100) if total > 0 else 100


def analyze_gaps(resume_skills, jd_skills):
    matched = {}
    missing = {}

    for cat in ['technical_skills', 'soft_skills', 'certifications']:
        r = set(resume_skills.get(cat, []))
        j = set(jd_skills.get(cat, []))
        matched[cat] = sorted(list(r & j))
        missing[cat] = sorted(list(j - r))

    # Extra resume skills not in JD (for "bonus skills" display)
    extra = {}
    for cat in ['technical_skills', 'soft_skills', 'certifications']:
        r = set(resume_skills.get(cat, []))
        j = set(jd_skills.get(cat, []))
        extra[cat] = sorted(list(r - j))

    # Weak areas
    weak_areas = []
    jt = len(jd_skills.get('technical_skills', []))
    js = len(jd_skills.get('soft_skills', []))
    jc = len(jd_skills.get('certifications', []))

    if jt > 0:
        rate = _match_rate(matched['technical_skills'], jt)
        if rate < 40:
            weak_areas.append({'area': 'Technical Skills', 'severity': 'high',
                               'match_rate': round(rate, 1),
                               'message': f"Only {len(matched['technical_skills'])}/{jt} required technical skills found. Major gap."})
        elif rate < 70:
            weak_areas.append({'area': 'Technical Skills', 'severity': 'medium',
                               'match_rate': round(rate, 1),
                               'message': f"{len(matched['technical_skills'])}/{jt} technical skills matched. Room to improve."})

    if js > 0:
        rate = _match_rate(matched['soft_skills'], js)
        if rate < 50:
            weak_areas.append({'area': 'Soft Skills', 'severity': 'medium',
                               'match_rate': round(rate, 1),
                               'message': f"Only {len(matched['soft_skills'])}/{js} required soft skills found."})

    if jc > 0 and len(matched['certifications']) == 0:
        weak_areas.append({'area': 'Certifications', 'severity': 'medium',
                           'match_rate': 0,
                           'message': f"None of the {jc} preferred certifications found."})

    return {
        'matched_skills': matched,
        'missing_skills': missing,
        'extra_skills': extra,
        'weak_areas': weak_areas,
    }