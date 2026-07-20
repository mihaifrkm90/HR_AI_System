from scoring import (
    calculeaza_scor,
    determina_nivel
)


def generate_candidate_insights(candidate):

    score = calculeaza_scor(
        candidate["experienta"],
        candidate["performanta"],
        candidate["certificari"]
    )


    strengths = []

    risks = []

    development = []


    if candidate["experienta"] >= 5:

        strengths.append(
            "Strong professional experience."
        )

    else:

        risks.append(
            "Limited professional experience."
        )

        development.append(
            "Gain more hands-on experience."
        )


    if candidate["performanta"] >= 8:

        strengths.append(
            "Excellent performance history."
        )

    elif candidate["performanta"] >= 5:

        strengths.append(
            "Consistent performance."
        )

        development.append(
            "Increase performance to reach leadership level."
        )

    else:

        risks.append(
            "Performance requires improvement."
        )

        development.append(
            "Create a performance improvement plan."
        )


    if candidate["certificari"] >= 3:

        strengths.append(
            "Strong certification portfolio."
        )

    elif candidate["certificari"] >= 1:

        development.append(
            "Obtain additional certifications."
        )

    else:

        risks.append(
            "No professional certifications."
        )

        development.append(
            "Earn industry certifications."
        )


    if score >= 90:

        promotion = "Ready for promotion."

    elif score >= 70:

        promotion = "Likely promotion within 6-12 months."

    elif score >= 50:

        promotion = "Needs additional development before promotion."

    else:

        promotion = "Not ready for promotion."


    return {

        "strengths": strengths,

        "risks": risks,

        "development": development,

        "promotion": promotion

    }