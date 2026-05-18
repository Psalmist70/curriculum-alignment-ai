from collections import Counter

def generate_analytics(results):

    if not results:
        return {
            "total_courses": 0,
            "average_score": 0,
            "high_match": 0,
            "medium_match": 0,
            "low_match": 0,
            "top_missing_skills": []
        }

    total_courses = len(results)

    scores = [
        float(r.get("similarity_score", 0))
        for r in results
    ]

    avg_score = sum(scores) / total_courses

    high = len([s for s in scores if s >= 0.70])
    medium = len([s for s in scores if 0.40 <= s < 0.70])
    low = len([s for s in scores if s < 0.40])

    # ==========================================
    # TOP MISSING SKILLS (FIXED - FREQUENCY BASED)
    # ==========================================
    all_missing_skills = []

    for r in results:
        all_missing_skills.extend(r.get("missing_skills", []))

    skill_counts = Counter(all_missing_skills)

    top_missing_skills = [
        skill for skill, _ in skill_counts.most_common(10)
    ]

    return {
        "total_courses": total_courses,
        "average_score": round(avg_score, 4),

        # MATCH LEVELS (FRONTEND FRIENDLY)
        "high_match": high,
        "medium_match": medium,
        "low_match": low,

        # INSIGHTS
        "top_missing_skills": top_missing_skills
    }