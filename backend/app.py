from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse

from reportlab.pdfgen import canvas

from database import incarca_candidati, salveaza_candidati

from scoring import calculeaza_scor, determina_nivel, determina_recomandare

from history import incarca_istoric, adauga_evaluare, salveaza_istoric, obtine_analiza_evolutie

from comments import incarca_comentarii, salveaza_comentarii

from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


def get_user(request: Request):

    return request.headers.get("X-User", "demo")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


@app.get("/")
def home():

    return {
        "mesaj": "HR System Online"
    }


@app.get("/candidati")
def lista_candidati(request: Request):
    candidati = incarca_candidati(get_user(request))

    rezultate = []


    for candidat in candidati:

        scor = calculeaza_scor(
            candidat["experienta"],
            candidat["performanta"],
            candidat["certificari"]
        )


        nivel = determina_nivel(scor)


        candidat_nou = candidat.copy()

        candidat_nou["scor"] = scor
        candidat_nou["nivel"] = nivel


        rezultate.append(candidat_nou)



    return JSONResponse(
        content=rezultate
    )


@app.post("/candidati")
def adauga_candidat(request: Request, candidat: dict):

    candidati = incarca_candidati(get_user(request))


    scor = calculeaza_scor(
        candidat["experienta"],
        candidat["performanta"],
        candidat["certificari"]
    )


    nivel = determina_nivel(scor)


    recomandare = determina_recomandare(scor)


    candidat["istoric"] = [

        {
            "scor": scor,
            "nivel": nivel,
            "recomandare": recomandare
        }

    ]


    candidati.append(candidat)


    salveaza_candidati(get_user(request), candidati)


    adauga_evaluare(
        candidat,
        scor,
        nivel,
        recomandare
    )


    return {

        "mesaj":"Candidat adaugat si evaluat AI",

        "scor":scor,

        "nivel":nivel,

        "recomandare":recomandare

    }
@app.get("/candidati/{nume}")
def profil_candidat(request: Request, nume: str):

    candidati = incarca_candidati(get_user(request))

    for candidat in candidati:

        if candidat["nume"].lower() == nume.lower():

            return candidat


    return {
        "eroare": "Candidat negasit"
    }

@app.get("/evaluare/{nume}")
def evaluare_candidat(request: Request, nume: str):

    candidati = incarca_candidati(get_user(request))

    for candidat in candidati:

        if candidat["nume"].lower() == nume.lower():

            scor = calculeaza_scor(
                candidat["experienta"],
                candidat["performanta"],
                candidat["certificari"]
            )

            nivel = determina_nivel(scor)

            recomandare = determina_recomandare(scor)


            return {
                "nume": candidat["nume"],
                "scor": scor,
                "nivel": nivel,
                "recomandare": recomandare
            }


    return {
        "eroare": "Candidat negasit"
    }

@app.delete("/candidati/{nume}")
def sterge_candidat(nume: str, request: Request):

    candidati = incarca_candidati(get_user(request))

    candidati_noi = []

    gasit = False


    for candidat in candidati:

        if candidat["nume"].lower() == nume.lower():

            gasit = True

        else:

            candidati_noi.append(candidat)



    if gasit:

        salveaza_candidati(get_user(request), candidati_noi)
        
        istoric = incarca_istoric()


        istoric_nou = []


        for evaluare in istoric:

            if evaluare["nume"].lower() != nume.lower():

                istoric_nou.append(evaluare)



        salveaza_istoric(istoric_nou)

        return {
            "mesaj": "Candidat sters"
        }


    return {
        "eroare": "Candidat negasit"
    }

@app.put("/candidati/{nume}")
def modifica_candidat(request: Request, nume: str, date_noi: dict):

    candidati = incarca_candidati(get_user(request))


    for candidat in candidati:


        if candidat["nume"].lower() == nume.lower():


            candidat["experienta"] = date_noi["experienta"]

            candidat["performanta"] = date_noi["performanta"]

            candidat["certificari"] = date_noi["certificari"]



            scor = calculeaza_scor(
                candidat["experienta"],
                candidat["performanta"],
                candidat["certificari"]
            )


            nivel = determina_nivel(scor)


            recomandare = determina_recomandare(scor)



            adauga_evaluare(
                candidat,
                scor,
                nivel,
                recomandare
            )



            salveaza_candidati(get_user(request), candidati)



            return {

                "mesaj":"Candidat actualizat si reevaluat",

                "scor":scor,

                "nivel":nivel,

                "recomandare":recomandare

            }


    return {

        "eroare":"Candidat negasit"
}

@app.get("/istoric/{nume}")
def istoric_candidat(nume:str):

    istoric = incarca_istoric()


    rezultate = []


    for evaluare in istoric:

        if evaluare["nume"].lower() == nume.lower():

            rezultate.append(evaluare)



    return rezultate

@app.get("/nivel/{nume}")
def nivel_candidat(request: Request, nume:str):

    candidati = incarca_candidati(get_user(request))

    for candidat in candidati:

        if candidat["nume"].lower() == nume.lower():

            scor = calculeaza_scor(
                candidat["experienta"],
                candidat["performanta"],
                candidat["certificari"]
            )

            nivel = determina_nivel(scor)

            return {
                "nivel": nivel,
                "scor": scor
            }


    return {
        "eroare":"Candidat negasit"
    }

@app.get("/statistici")
def statistici(request: Request):

    candidati = incarca_candidati(get_user(request))


    total = len(candidati)


    if total == 0:

        return {

            "total":0,

            "high_potential":0,

            "ready_soon":0,

            "developing":0,

            "needs_improvement":0,

            "procent_high_potential":0,

            "medie_scor":0,

            "medie_performanta":0

        }



    high_potential = 0
    ready_soon = 0
    developing = 0
    needs_improvement = 0


    suma_scor = 0
    suma_performanta = 0



    for candidat in candidati:


        scor = calculeaza_scor(

            candidat["experienta"],

            candidat["performanta"],

            candidat["certificari"]

        )


        nivel = determina_nivel(scor)



        suma_scor += scor

        suma_performanta += candidat["performanta"]



        if nivel == "High Potential":

            high_potential += 1


        elif nivel == "Ready Soon":

            ready_soon += 1


        elif nivel == "Developing":

            developing += 1


        elif nivel == "Needs Improvement":

            needs_improvement += 1




    return {


        "total": total,


        "high_potential": high_potential,


        "ready_soon": ready_soon,


        "developing": developing,


        "needs_improvement": needs_improvement,


        "procent_high_potential":

        round((high_potential / total) * 100,2),



        "medie_scor":

        round(suma_scor / total,2),



        "medie_performanta":

        round(suma_performanta / total,2)

    }


@app.get("/raport/{nume}")
def raport_candidat(request: Request, nume:str):

    candidati = incarca_candidati(get_user(request))


    for candidat in candidati:

        if candidat["nume"].lower() == nume.lower():


            scor = calculeaza_scor(
                candidat["experienta"],
                candidat["performanta"],
                candidat["certificari"]
            )


            nivel = determina_nivel(scor)


            recomandare = determina_recomandare(scor)


            raport = f"""

============================

      HR AI REPORT

============================


Candidat:

{candidat["nume"]}



Experienta:

{candidat["experienta"]} ani



Performanta:

{candidat["performanta"]}/10



Certificari:

{candidat["certificari"]}



----------------------------


SCOR AI:

{scor}/100



CLASIFICARE:

{nivel}



RECOMANDARE:

{recomandare}



STATUS:

{"Promovare recomandata" if scor>=80 else "Necesita dezvoltare"}



============================

"""


            return PlainTextResponse(
                raport
            )


    return {
        "eroare":"Candidat negasit"
    }


@app.post("/reevaluare/{nume}")
def reevaluare_candidat(request: Request, nume:str, date:dict):


    candidati = incarca_candidati(get_user(request))


    for candidat in candidati:


        if candidat["nume"].lower() == nume.lower():


            scor = calculeaza_scor(
                date["experienta"],
                date["performanta"],
                date["certificari"]
            )


            nivel = determina_nivel(scor)


            recomandare = determina_recomandare(scor)


            adauga_evaluare(
            candidat,
            scor,
            nivel,
            recomandare
            )


            salveaza_candidati(get_user(request), candidati)

                    
            return {

                "mesaj":"Evaluare noua salvata",

                "scor":scor,

                "nivel":nivel,

                "recomandare":recomandare

            }



    return {
        "eroare":"Candidat negasit"
    }

@app.get("/analiza/{nume}")
def analiza_candidat(nume:str):

    rezultat = obtine_analiza_evolutie(nume)

    return rezultat


@app.get("/comentarii/{nume}")
def lista_comentarii(nume:str):

    comentarii = incarca_comentarii()


    rezultate = []


    for comentariu in comentarii:

        if comentariu["nume"].lower() == nume.lower():

            rezultate.append(comentariu)


    return rezultate



@app.post("/comentarii/{nume}")
def adauga_comentariu(nume:str, date:dict):

    comentarii = incarca_comentarii()


    comentarii.append({

        "nume": nume,

        "comentariu": date["comentariu"]

    })


    salveaza_comentarii(comentarii)


    return {

        "mesaj":"Comentariu salvat"

    }

@app.get("/raport_pdf/{nume}")
def raport_pdf(request: Request, nume:str):

    candidati = incarca_candidati(get_user(request))


    for candidat in candidati:


        if candidat["nume"].lower() == nume.lower():


            scor = calculeaza_scor(
                candidat["experienta"],
                candidat["performanta"],
                candidat["certificari"]
            )


            nivel = determina_nivel(scor)


            recomandare = determina_recomandare(scor)


            fisier = f"raport_{nume}.pdf"


            pdf = canvas.Canvas(fisier)


            pdf.setFont(
                "Helvetica-Bold",
                18
            )


            pdf.drawString(
                100,
                750,
                "HR AI Candidate Evaluation Report"
            )


            pdf.drawString(
                100,
                720,
                "Generated automatically by AI HR System"
            )


            pdf.setFont(
                "Helvetica",
                12
            )


            y = 700


            date = [

                f"Candidat: {nume}",

                f"Experienta: {candidat['experienta']} ani",

                f"Performanta: {candidat['performanta']}/10",

                f"Certificari: {candidat['certificari']}",

                "",

                f"Scor AI: {scor}/100",

                f"Nivel: {nivel}",

                f"Recomandare: {recomandare}"

                f"Status: {'Promovare recomandata' if scor >= 80 else 'Necesita dezvoltare'}"

                f"Data raport: {datetime.now().strftime('%d-%m-%Y %H:%M')}",

            ]


            for linie in date:


                pdf.drawString(
                    100,
                    y,
                    linie
                )


                y -= 30



            pdf.save()


            return FileResponse(
                fisier,
                media_type="application/pdf",
                filename=fisier
            )


    return {
        "eroare":"Candidat negasit"
    }