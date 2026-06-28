"""
Recommendation Engine — courses, certifications, ATS tips, improvement roadmap.
"""
from skills_data import COURSE_RECOMMENDATIONS


def generate_recommendations(missing_skills, weak_areas, compatibility_score):
    recs = {
        'course_recommendations': [],
        'certification_suggestions': [],
        'ats_tips': [],
        'improvement_suggestions': [],
        'priority_skills': [],
        'learning_path': [],
    }

    # Priority skills (top 5 missing technical)
    all_missing_tech = missing_skills.get('technical_skills', [])
    recs['priority_skills'] = all_missing_tech[:5]

    # Course recommendations
    for skill in all_missing_tech[:10]:
        sl = skill.lower()
        if sl in COURSE_RECOMMENDATIONS:
            recs['course_recommendations'].append({
                'skill': skill,
                'courses': COURSE_RECOMMENDATIONS[sl]
            })
        else:
            recs['course_recommendations'].append({
                'skill': skill,
                'courses': [{'name': f"Search '{skill}' courses",
                             'platform': 'Coursera / Udemy / YouTube',
                             'url': f"https://www.google.com/search?q={skill.replace(' ', '+')}+course"}]
            })

    # Certification suggestions
    for cert in missing_skills.get('certifications', []):
        recs['certification_suggestions'].append({
            'certification': cert,
            'tip': f"Pursue '{cert}' to strengthen your profile for this role."
        })

    # ATS tips
    recs['ats_tips'] = [
        "Use a clean, single-column layout with standard section headings.",
        "Mirror exact keywords from the job description in your resume.",
        "Use standard fonts (Arial, Calibri, Times New Roman) at 10-12pt.",
        "Avoid images, graphics, tables, and text boxes — ATS can't parse them.",
        "Save as PDF to preserve formatting across all systems.",
        "Start bullet points with action verbs (Developed, Implemented, Led).",
        "Include a dedicated 'Skills' section with both technical and soft skills.",
        "Quantify achievements (e.g., 'Reduced load time by 40%', 'Led team of 8').",
        "Keep resume to 1-2 pages maximum.",
        "Use consistent date formatting (e.g., Jan 2024 – Present).",
    ]

    # Tiered improvement suggestions
    if compatibility_score < 30:
        recs['improvement_suggestions'] = [
            "⚠️ Your resume has a low match. Major revision needed.",
            "Tailor your resume specifically for this job description.",
            "Focus on acquiring the top 3-5 missing technical skills first.",
            "Rewrite your experience to highlight relevant projects and impact.",
            "Build personal projects or contribute to open source in this domain.",
            "Consider entry-level certifications to demonstrate commitment.",
        ]
        recs['learning_path'] = [
            {'step': 1, 'action': 'Learn top 3 missing technical skills', 'timeframe': '2-4 weeks each'},
            {'step': 2, 'action': 'Build 2 portfolio projects using those skills', 'timeframe': '3-4 weeks'},
            {'step': 3, 'action': 'Earn a relevant certification', 'timeframe': '4-8 weeks'},
            {'step': 4, 'action': 'Rewrite resume with new skills and projects', 'timeframe': '1 week'},
            {'step': 5, 'action': 'Re-analyze and iterate', 'timeframe': 'Ongoing'},
        ]
    elif compatibility_score < 60:
        recs['improvement_suggestions'] = [
            "📊 Moderate match. Good foundation, but notable gaps remain.",
            "Fill identified skill gaps — they're your quickest path to a higher score.",
            "Highlight relevant projects and experience more prominently.",
            "Add any certifications related to the role.",
            "Use keywords from the JD naturally throughout your resume.",
        ]
        recs['learning_path'] = [
            {'step': 1, 'action': 'Address top 3 skill gaps', 'timeframe': '2-3 weeks each'},
            {'step': 2, 'action': 'Strengthen resume with quantified achievements', 'timeframe': '1 week'},
            {'step': 3, 'action': 'Pursue one relevant certification', 'timeframe': '4-6 weeks'},
            {'step': 4, 'action': 'Re-analyze resume after updates', 'timeframe': 'Ongoing'},
        ]
    elif compatibility_score < 80:
        recs['improvement_suggestions'] = [
            "✅ Good match! Your resume aligns well with the requirements.",
            "Address remaining skill gaps for an excellent match.",
            "Ensure your resume clearly showcases relevant experience.",
            "Add a tailored professional summary for this specific role.",
            "Proofread for consistency and professional tone.",
        ]
        recs['learning_path'] = [
            {'step': 1, 'action': 'Fill remaining 1-2 skill gaps', 'timeframe': '1-2 weeks each'},
            {'step': 2, 'action': 'Polish resume formatting and language', 'timeframe': '1 week'},
            {'step': 3, 'action': 'Prepare for interviews on matched skills', 'timeframe': 'Ongoing'},
        ]
    else:
        recs['improvement_suggestions'] = [
            "🎯 Excellent match! Your resume strongly aligns with this role.",
            "Fine-tune with specific keywords from the job description.",
            "Prepare for interviews — review topics related to matched skills.",
            "Consider adding a tailored cover letter to complement your resume.",
            "Keep learning and stay updated with industry trends.",
        ]
        recs['learning_path'] = [
            {'step': 1, 'action': 'Polish and finalize resume', 'timeframe': '1-2 days'},
            {'step': 2, 'action': 'Prepare interview answers for key skills', 'timeframe': '1-2 weeks'},
            {'step': 3, 'action': 'Apply confidently!', 'timeframe': 'Now'},
        ]

    return recs