from validation import citeste_numar, verifica_experienta, verifica_performanta, verifica_certificari


def afiseaza_candidati(candidates):

    print("\n--- Lista candidati ---")

    for candidat in candidates:

        print(
            candidat["nume"],
            "-",
            candidat["experienta"],
            "ani experienta"
        )



def adauga_candidat(candidates):

    print("\n--- Adauga candidat ---")

    nume = input("Nume: ")


    while True:

        experienta = citeste_numar("Experienta ani: ")

        if verifica_experienta(experienta):
            break

        print("Experienta nu poate fi negativa.")



    while True:

        performanta = citeste_numar("Performanta 1-10: ")

        if verifica_performanta(performanta):
            break

        print("Performanta trebuie sa fie intre 1 si 10.")



    while True:

        certificari = citeste_numar("Certificari: ")

        if verifica_certificari(certificari):
            break

        print("Numarul de certificari nu poate fi negativ.")



    candidat = {

        "nume": nume,
        "experienta": experienta,
        "performanta": performanta,
        "certificari": certificari,
        "istoric": []


    }


    candidates.append(candidat)

    print("Candidat adaugat!")
    


def cauta_candidat(candidates):

    nume_cautat = input("\nNume candidat: ")

    for candidat in candidates:

        if candidat["nume"].lower() == nume_cautat.lower():

            return candidat


    return None



def modifica_candidat(candidates):

    nume_cautat = input("\nNume candidat: ")


    for candidat in candidates:

        if candidat["nume"].lower() == nume_cautat.lower():

            print("\nCandidat gasit.")
            
            print("Lasa gol daca nu vrei sa modifici.")
            modificat = False


            experienta = input("Experienta noua: ")

            if experienta:
                candidat["experienta"] = int(experienta)
                modificat = True


            performanta = input("Performanta noua: ")

            if performanta:
                candidat["performanta"] = int(performanta)
                modificat = True

            certificari = input("Certificari noi: ")

            if certificari:
                candidat["certificari"] = int(certificari)
                modificat = True


            if modificat:

                print("\nCandidat actualizat!")

            else:

                print("\nNicio modificare efectuata.")


            input("\nApasa ENTER pentru a continua...")

            if modificat:
                return candidat
            else:
                return None


    print("Candidatul nu a fost gasit.")

    input("\nApasa ENTER pentru a continua...")

    return None