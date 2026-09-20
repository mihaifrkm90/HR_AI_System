from scoring import load_config


def explain_score(candidate):

    config = load_config()

    breakdown = []


    # EXPERIENCE

    experience_points = 0

    if candidate["experienta"] >= 5:

        experience_points = config["experienta"]

        experience_reason = "Candidate has strong professional experience."

    elif candidate["experienta"] >= 2:

        experience_points = config["experienta"] / 2

        experience_reason = "Candidate has moderate professional experience."

    else:

        experience_reason = "Candidate has limited professional experience."



    breakdown.append({

        "factor": "Experience",

        "points": int(experience_points),

        "reason": experience_reason

    })



    # PERFORMANCE

    performance_points = 0

    if candidate["performanta"] >= 8:

        performance_points = config["performanta"]

        performance_reason = "Performance rating is excellent."

    elif candidate["performanta"] >= 5:

        performance_points = config["performanta"] / 2

        performance_reason = "Performance rating is acceptable but can improve."

    else:

        performance_reason = "Performance requires improvement."



    breakdown.append({

        "factor": "Performance",

        "points": int(performance_points),

        "reason": performance_reason

    })



    # CERTIFICATIONS

    certification_points = 0

    if candidate["certificari"] >= 3:

        certification_points = config["certificari"]

        certification_reason = "Candidate has strong certification background."

    elif candidate["certificari"] >= 1:

        certification_points = config["certificari"] / 2

        certification_reason = "Candidate has some certifications."

    else:

        certification_reason = "Candidate has no relevant certifications."



    breakdown.append({

        "factor": "Certifications",

        "points": int(certification_points),

        "reason": certification_reason

    })


    return breakdown