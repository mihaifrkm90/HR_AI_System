import json
import os


def get_database_file(user):

    return f"database_{user}.json"



def incarca_candidati(user):

    fisier = get_database_file(user)


    if not os.path.exists(fisier):

        return []


    try:

        with open(fisier, "r") as f:

            continut = f.read()

            if continut.strip() == "":
                return []

            return json.loads(continut)


    except json.JSONDecodeError:

        return []



def salveaza_candidati(user, candidati):

    fisier = get_database_file(user)


    with open(fisier, "w") as f:

        json.dump(
            candidati,
            f,
            indent=4
        )