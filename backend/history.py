import json
from datetime import datetime


def incarca_istoric():

    try:
        with open("history.json", "r") as fisier:
            return json.load(fisier)

    except FileNotFoundError:
        return []



def salveaza_istoric(istoric):

    with open("history.json", "w") as fisier:
        json.dump(
            istoric,
            fisier,
            indent=4
        )


def adauga_evaluare(candidat, scor, nivel, recomandare):

    print("SALVARE ISTORIC:", candidat["nume"], scor)

    istoric = incarca_istoric()
    ultima_evaluare = None
    for evaluare in reversed(istoric):

        if evaluare["nume"].lower() == candidat["nume"].lower():

            ultima_evaluare = evaluare

            break


    if ultima_evaluare:

        if (
            ultima_evaluare["scor"] == scor
            and ultima_evaluare["nivel"] == nivel
            and ultima_evaluare["recomandare"] == recomandare
        ):

            return

    evaluare = {
        "nume": candidat["nume"],
        "scor": scor,
        "nivel": nivel,
        "recomandare": recomandare,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M")

    }

    istoric.append(evaluare)

    salveaza_istoric(istoric)


def afiseaza_istoric(nume):

    istoric = incarca_istoric()

    gasit = False

    print("\n--- Istoric evaluari ---")


    for evaluare in istoric:

        if evaluare["nume"].lower() == nume.lower():

            print("\nCandidat:", evaluare["nume"])
            print("Scor:", evaluare["scor"])
            print("Nivel:", evaluare["nivel"])
            print("Recomandare:", evaluare["recomandare"])
        if "data" in evaluare:
            print("Data:", evaluare["data"])

            gasit = True


    if not gasit:

        print("Nu exista istoric pentru acest candidat.")

def analiza_evolutie(nume):

    istoric = incarca_istoric()

    scoruri = []


    for evaluare in istoric:

        if evaluare["nume"].lower() == nume.lower():

            scoruri.append(
                evaluare["scor"]
            )


    print("\n--- Analiza evolutie ---")


    if len(scoruri) < 2:

        print("Nu exista suficiente evaluari pentru analiza.")

        return


    primul_scor = scoruri[0]
    ultimul_scor = scoruri[-1]


    diferenta = ultimul_scor - primul_scor


    print("Primul scor:", primul_scor)
    print("Ultimul scor:", ultimul_scor)


    if diferenta > 0:

        print("Evolutie: +", diferenta)
        print("Trend: Pozitiv")


    elif diferenta < 0:

        print("Evolutie:", diferenta)
        print("Trend: Negativ")


    else:

        print("Evolutie: 0")
        print("Trend: Stabil")

        
def obtine_analiza_evolutie(nume):

    istoric = incarca_istoric()

    scoruri = []


    for evaluare in istoric:

        if evaluare["nume"].lower() == nume.lower():

            scoruri.append(evaluare["scor"])


    if len(scoruri) == 0:

        return {
            "eroare": "Nu exista evaluari"
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