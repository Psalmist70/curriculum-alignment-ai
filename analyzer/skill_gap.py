def detect_skill_gaps(curriculum_skills, job_skills):

    missing = []

    for skill in job_skills:

        if skill not in curriculum_skills:
            missing.append(skill)

    return missing