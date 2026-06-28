"""
Skill Extraction — matches resume/JD text against predefined skill databases.
Uses multi-word phrase matching + single-word boundary matching.
"""
import re
from skills_data import TECHNICAL_SKILLS, SOFT_SKILLS, CERTIFICATIONS


def _match_skills(text_lower, skill_set):
    found = set()
    for skill in skill_set:
        if len(skill.split()) == 1:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found.add(skill)
        else:
            if skill in text_lower:
                found.add(skill)
    return sorted(list(found))


def extract_skills_from_text(text):
    text_lower = text.lower()
    return {
        'technical_skills': _match_skills(text_lower, TECHNICAL_SKILLS),
        'soft_skills': _match_skills(text_lower, SOFT_SKILLS),
        'certifications': _match_skills(text_lower, CERTIFICATIONS),
    }


def count_total_skills(skills_dict):
    return (len(skills_dict.get('technical_skills', []))
            + len(skills_dict.get('soft_skills', []))
            + len(skills_dict.get('certifications', [])))