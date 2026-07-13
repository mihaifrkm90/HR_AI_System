from database import incarca_candidati, salveaza_candidati
from scoring import calculeaza_scor, determina_nivel, determina_recomandare


candidati = incarca_candidati()


for candidat in candidati:


    if "istoric" not in candidat or len(candidat["istoric"]) == 0:


        scor = calculeaza_scor(
            candidat["experienta"],
            candidat["performanta"],
            candidat["certificari"]
        )


        nivel = determina_nivel(scor)


        recomandare = determina_recomandare(scor)



        candidat["istoric"]=[

            {
                "scor":scor,
                "nivel":nivel,
                "recomandare":recomandare
            }

        ]



salveaza_candidati(candidati)


print("Database actualizat")