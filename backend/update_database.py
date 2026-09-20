from database import incarca_candidati, salveaza_candidati
from scoring import calculate_score, determine_level, determine_recommendation


candidati = incarca_candidati()


for candidat in candidati:


    if "istoric" not in candidat or len(candidat["istoric"]) == 0:


        score = calculate_score(
            candidat["experienta"],
            candidat["performanta"],
            candidat["certificari"]
        )


        level = determine_level(score)


        recommendation = determine_recommendation(score)



        candidat["istoric"]=[

            {
                "scor":score,
                "nivel":level,
                "recomandare":recommendation
            }

        ]



salveaza_candidati(candidati)


print("Database actualizat")