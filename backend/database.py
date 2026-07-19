import json
import os


def get_database_file(user):

    return f"database_{user}.json"



def incarca_candidati(user):

    fisier = get_database_file(user)


    if not os.path.exists(fisier):

        return []


    with open(fisier, "r") as f:

        return json.load(f)



def salveaza_candidati(user, candidati):

    fisier = get_database_file(user)


    with open(fisier, "w") as f:

        json.dump(
            candidati,
            f,
            indent=4
        )