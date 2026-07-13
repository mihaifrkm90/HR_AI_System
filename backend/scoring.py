import json


def incarca_config():

    with open("config.json", "r") as fisier:
        return json.load(fisier)



def calculeaza_scor(experienta, performanta, certificari):

    config = incarca_config()

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

def determina_nivel(scor):

    if scor >= 90:
        return "High Potential"

    elif scor >= 70:
        return "Ready Soon"

    elif scor >= 50:
        return "Developing"

    else:
        return "Needs Improvement"

def determina_recomandare(scor):

    if scor >= 80:
        return "Promovare"

    elif scor >= 50:
        return "Evaluare suplimentara"

    else:
        return "Nu este pregatit"
    
def evalueaza_profil(candidat):

    scor = calculeaza_scor(
        candidat["experienta"],
        candidat["performanta"],
        candidat["certificari"]
    )

    nivel = determina_nivel(scor)

    recomandare = determina_recomandare(scor)


    return {
        "scor": scor,
        "nivel": nivel,
        "recomandare": recomandare
    }