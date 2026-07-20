import json
import os
from datetime import datetime


def get_history_file(user):

    return f"history_{user}.json"



def incarca_istoric(user):

    fisier = get_history_file(user)

    if not os.path.exists(fisier):

        return []


    try:

        with open(fisier, "r") as file:

            continut = file.read()

            if continut.strip() == "":
                return []

            return json.loads(continut)


    except json.JSONDecodeError:

        return []



def salveaza_istoric(user, istoric):

    fisier = get_history_file(user)

    with open(fisier, "w") as file:
        
        json.dump(
            istoric,
            file,
            indent=4
        )



def adauga_evaluare(user, candidat, scor, nivel, recomandare):

    istoric = incarca_istoric(user)

    evaluare = {
        "nume": candidat["nume"],
        "scor": scor,
        "nivel": nivel,
        "recomandare": recomandare,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M")
        
    }

    istoric.append(evaluare)

    salveaza_istoric(
        user,
        istoric
    )



def obtine_analiza_evolutie(user, nume):


    istoric = incarca_istoric(user)


    scoruri = []


    for evaluare in istoric:

        if evaluare["nume"].lower() == nume.lower():

            scoruri.append(
                evaluare["scor"]
            )


    if len(scoruri) == 0:

        return {
            "eroare":"Nu exista evaluari"
        }


    primul_scor = scoruri[0]

    ultimul_scor = scoruri[-1]


    diferenta = ultimul_scor - primul_scor


    if diferenta > 0:

        trend = "Pozitiv"

    elif diferenta < 0:

        trend = "Negativ"

    else:

        trend = "Stabil"



    return {

        "primul_scor": primul_scor,

        "ultimul_scor": ultimul_scor,

        "diferenta": diferenta,

        "trend": trend

    }