def generate_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Improve your {skill} skills through structured courses"
        )

    return recommendations