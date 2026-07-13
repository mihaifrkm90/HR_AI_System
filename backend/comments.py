import json


def incarca_comentarii():

    try:

        with open("comments.json", "r") as fisier:

            return json.load(fisier)

    except FileNotFoundError:

        return []



def salveaza_comentarii(comentarii):

    with open("comments.json", "w") as fisier:

        json.dump(
            comentarii,
            fisier,
            indent=4
        )



def adauga_comentariu(nume, text):

    comentarii = incarca_comentarii()


    comentariu = {

        "nume": nume,

        "comentariu": text

    }


    comentarii.append(comentariu)


    salveaza_comentarii(comentarii)