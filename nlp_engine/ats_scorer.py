"""
ATS (Applicant Tracking System) Compatibility Scorer.
Evaluates resume formatting, keyword density, and structure.
"""
import re


def calculate_ats_score(resume_text, jd_text, resume_skills, jd_skills):
    """
    Returns an ATS score (0-100) with detailed breakdown and feedback.
    """
    checks = []
    total_points = 0
    earned_points = 0

    # 1. Length check (300-1500 words ideal)
    word_count = len(resume_text.split())
    total_points += 15
    if 300 <= word_count <= 1500:
        earned_points += 15
        checks.append({'check': 'Resume Length', 'status': 'pass', 'points': 15,
                        'message': f'Good length ({word_count} words).'})
    elif 200 <= word_count < 300 or 1500 < word_count <= 2000:
        earned_points += 8
        checks.append({'check': 'Resume Length', 'status': 'warn', 'points': 8,
                        'message': f'Acceptable length ({word_count} words). Aim for 300-1500.'})
    else:
        checks.append({'check': 'Resume Length', 'status': 'fail', 'points': 0,
                        'message': f'Poor length ({word_count} words). ATS prefers 300-1500 words.'})

    # 2. Contact info presence
    total_points += 10
    has_email = bool(re.search(r'\S+@\S+\.\S+', resume_text))
    has_phone = bool(re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,}', resume_text))
    if has_email and has_phone:
        earned_points += 10
        checks.append({'check': 'Contact Information', 'status': 'pass', 'points': 10,
                        'message': 'Email and phone number detected.'})
    elif has_email or has_phone:
        earned_points += 5
        checks.append({'check': 'Contact Information', 'status': 'warn', 'points': 5,
                        'message': 'Partial contact info. Include both email and phone.'})
    else:
        checks.append({'check': 'Contact Information', 'status': 'fail', 'points': 0,
                        'message': 'No contact information detected. Add email and phone.'})

    # 3. Section headings
    total_points += 15
    sections_found = 0
    section_keywords = ['experience', 'education', 'skills', 'projects', 'summary',
                        'objective', 'certifications', 'achievements', 'work history',
                        'professional experience', 'technical skills']
    text_lower = resume_text.lower()
    for kw in section_keywords:
        if kw in text_lower:
            sections_found += 1
    if sections_found >= 4:
        earned_points += 15
        checks.append({'check': 'Section Headings', 'status': 'pass', 'points': 15,
                        'message': f'{sections_found} standard sections detected. Well structured.'})
    elif sections_found >= 2:
        earned_points += 8
        checks.append({'check': 'Section Headings', 'status': 'warn', 'points': 8,
                        'message': f'Only {sections_found} sections detected. Add more standard headings.'})
    else:
        checks.append({'check': 'Section Headings', 'status': 'fail', 'points': 0,
                        'message': 'Very few standard sections. Use headings like Experience, Education, Skills.'})

    # 4. Keyword match density
    total_points += 25
    all_jd_skills = (set(jd_skills.get('technical_skills', []))
                     | set(jd_skills.get('soft_skills', [])))
    all_resume_skills = (set(resume_skills.get('technical_skills', []))
                         | set(resume_skills.get('soft_skills', [])))
    if all_jd_skills:
        keyword_rate = len(all_resume_skills & all_jd_skills) / len(all_jd_skills)
    else:
        keyword_rate = 0.5
    kw_points = round(keyword_rate * 25)
    earned_points += kw_points
    if keyword_rate >= 0.7:
        checks.append({'check': 'Keyword Matching', 'status': 'pass', 'points': kw_points,
                        'message': f'{round(keyword_rate*100)}% of JD keywords found in resume.'})
    elif keyword_rate >= 0.4:
        checks.append({'check': 'Keyword Matching', 'status': 'warn', 'points': kw_points,
                        'message': f'{round(keyword_rate*100)}% keyword match. Add more JD keywords.'})
    else:
        checks.append({'check': 'Keyword Matching', 'status': 'fail', 'points': kw_points,
                        'message': f'Only {round(keyword_rate*100)}% keyword match. Significantly improve alignment.'})

    # 5. Action verbs
    total_points += 10
    action_verbs = ['developed', 'implemented', 'designed', 'managed', 'led', 'created',
                    'built', 'optimized', 'improved', 'analyzed', 'delivered', 'achieved',
                    'increased', 'reduced', 'launched', 'established', 'coordinated',
                    'executed', 'streamlined', 'resolved', 'mentored', 'collaborated']
    verbs_found = sum(1 for v in action_verbs if v in text_lower)
    if verbs_found >= 5:
        earned_points += 10
        checks.append({'check': 'Action Verbs', 'status': 'pass', 'points': 10,
                        'message': f'{verbs_found} action verbs found. Strong impact language.'})
    elif verbs_found >= 2:
        earned_points += 5
        checks.append({'check': 'Action Verbs', 'status': 'warn', 'points': 5,
                        'message': f'Only {verbs_found} action verbs. Use more (Developed, Implemented, Led...).'})
    else:
        checks.append({'check': 'Action Verbs', 'status': 'fail', 'points': 0,
                        'message': 'Very few action verbs. Start bullets with action verbs.'})

    # 6. Quantifiable achievements
    total_points += 10
    numbers = re.findall(r'\b\d+[%+]?\b', resume_text)
    metrics = [n for n in numbers if len(n) >= 2]  # filter single digits
    if len(metrics) >= 3:
        earned_points += 10
        checks.append({'check': 'Quantified Achievements', 'status': 'pass', 'points': 10,
                        'message': f'{len(metrics)} metrics/numbers found. Good quantification.'})
    elif len(metrics) >= 1:
        earned_points += 5
        checks.append({'check': 'Quantified Achievements', 'status': 'warn', 'points': 5,
                        'message': 'Few quantified achievements. Add numbers (e.g., "improved by 40%").'})
    else:
        checks.append({'check': 'Quantified Achievements', 'status': 'fail', 'points': 0,
                        'message': 'No quantified achievements. ATS and recruiters value measurable impact.'})

    # 7. No special characters / formatting issues
    total_points += 15
    special_chars = len(re.findall(r'[^\x00-\x7F]', resume_text))
    if special_chars < 5:
        earned_points += 15
        checks.append({'check': 'Clean Formatting', 'status': 'pass', 'points': 15,
                        'message': 'Clean text formatting. ATS-friendly.'})
    elif special_chars < 20:
        earned_points += 8
        checks.append({'check': 'Clean Formatting', 'status': 'warn', 'points': 8,
                        'message': f'{special_chars} special characters detected. Some may confuse ATS.'})
    else:
        checks.append({'check': 'Clean Formatting', 'status': 'fail', 'points': 0,
                        'message': f'{special_chars} special characters. Use plain text formatting.'})

    score = round((earned_points / total_points) * 100, 1) if total_points > 0 else 0

    # Feedback tips
    tips = []
    for c in checks:
        if c['status'] != 'pass':
            tips.append(c['message'])

    if not tips:
        tips.append("Your resume is well-optimized for ATS systems!")

    return {
        'score': score,
        'checks': checks,
        'tips': tips,
        'earned_points': earned_points,
        'total_points': total_points,
    }