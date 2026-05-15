def generate_analytics(results):

    if not results:
        return {}

    total_courses = len(results)

    avg_score = sum(
        r["similarity_score"] for r in results
    ) / total_courses

    highly_aligned = len([
        r for r in results
        if r["similarity_score"] >= 0.70
    ])

    medium_aligned = len([
        r for r in results
        if 0.40 <= r["similarity_score"] < 0.70
    ])

    low_aligned = len([
        r for r in results
        if r["similarity_score"] < 0.40
    ])

    all_missing_skills = []

    for r in results:
        all_missing_skills.extend(r["missing_skills"])

    top_missing_skills = list(set(all_missing_skills))[:10]

    return {
        "total_courses": total_courses,
        "average_similarity_score": round(avg_score, 4),
        "high_alignment_courses": highly_aligned,
        "medium_alignment_courses": medium_aligned,
        "low_alignment_courses": low_aligned,
        "top_missing_skills": top_missing_skills
    }