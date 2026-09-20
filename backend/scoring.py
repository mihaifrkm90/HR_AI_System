import json


def load_config():

    with open("config.json", "r") as fisier:
        return json.load(fisier)



def calculate_score(experienta, performanta, certificari):

    config = load_config()

    scor = 0

    if experienta >= 5:
        scor += config["experienta"]

    elif experienta >= 2:
        scor += config["experienta"] / 2


    if performanta >= 8:
        scor += config["performanta"]

    elif performanta >= 5:
        scor += config["performanta"] / 2


    if certificari >= 3:
        scor += config["certificari"]

    elif certificari >= 1:
        scor += config["certificari"] / 2


    return int(scor)

def determine_level(scor):

    if scor >= 90:
        return "High Potential"

    elif scor >= 70:
        return "Ready Soon"

    elif scor >= 50:
        return "Developing"

    else:
        return "Needs Improvement"

def determine_recommendation(score):

    if score >= 80:
        return "Promotion Recommended"

    elif score >= 50:
        return "Additional Evaluation Required"

    else:
        return "Not Ready for Promotion"
    
def evaluate_profile(candidate):

    score = calculate_score(
        candidate["experienta"],
        candidate["performanta"],
        candidate["certificari"]
    )


    level = determine_level(score)


    recommendation = determine_recommendation(score)


    return {

        "score": score,

        "level": level,

        "recommendation": recommendation

    }