import json


def incarca_candidati():

    with open("database.json", "r") as fisier:
        return json.load(fisier)



def salveaza_candidati(candidati):

    with open("database.json", "w") as fisier:
        json.dump(candidati, fisier, indent=4)