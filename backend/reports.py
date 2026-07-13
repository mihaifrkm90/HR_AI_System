def salveaza_raport(rezultate):

    with open("raport.txt", "w") as fisier:

        for rezultat in rezultate:

            fisier.write("====================\n")
            fisier.write("Evaluare candidat\n")
            fisier.write("====================\n")

            fisier.write(
                f"Nume: {rezultat['nume']}\n"
            )

            fisier.write(
                f"Scor: {rezultat['scor']}\n"
            )

            fisier.write(
                f"Nivel: {rezultat['nivel']}\n"
            )

            fisier.write(
                f"Recomandare: {rezultat['recomandare']}\n\n"
            )

def salveaza_raport_individual(candidat, rezultat):

    nume_fisier = candidat["nume"] + "_raport.txt"

    with open(nume_fisier, "w") as fisier:

        fisier.write("====================\n")
        fisier.write("Raport Candidat\n")
        fisier.write("====================\n\n")

        fisier.write(
            f"Nume: {candidat['nume']}\n"
        )

        fisier.write(
            f"Experienta: {candidat['experienta']} ani\n"
        )

        fisier.write(
            f"Performanta: {candidat['performanta']}/10\n"
        )

        fisier.write(
            f"Certificari: {candidat['certificari']}\n\n"
        )

        fisier.write(
            f"Scor: {rezultat['scor']}\n"
        )

        fisier.write(
            f"Nivel: {rezultat['nivel']}\n"
        )

        fisier.write(
            f"Recomandare: {rezultat['recomandare']}\n"
        )