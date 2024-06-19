import os.path
from os import remove
import tkinter as tk
from urllib.request import urlretrieve

def logger(func):
    """
    Fonction pot de fleur, juste pour afficher ce qui ce passe dans le programme
    Entree: funct -> funct
    Sortie: En fonction de la fonction d'entrée
    """
    def print_err(*arg, **kwarg):
        try:
            output = func(*arg, **kwarg)
            print(f"[Ok] {func.__name__}")
            return output
        except Exception as error:
            print(f"[Error] {func.__name__} ran into {error}")
    return print_err

@logger
def first_init():
    """
    Télécharge les bases de données de l'Arcep et les assembles en une base de données.
    Entree: None
    Sortie: None
    """
    # Telecharge les db (csv) de l'Arcep
    if not os.path.isfile('identifiants_CE.csv'):
        urlretrieve("https://extranet.arcep.fr/uploads/identifiants_CE.csv", "identifiants_CE.csv")
    if not os.path.isfile('MAJNUM.csv'):
        urlretrieve("https://extranet.arcep.fr/uploads/MAJNUM.csv", "MAJNUM.csv")

    # Organise les données en deux listes
    raw_rows_a = []
    raw_rows_b = []
    with open("identifiants_CE.csv", "r", encoding='iso-8859-3') as file: # rip l'utf
        file_csv_a = file.readlines()[1:]
        for row in file_csv_a:
            raw_rows_a.append(row)
    with open("MAJNUM.csv", "r", encoding='iso-8859-3') as file:
        file_csv_b = file.readlines()[1:]
        for row in file_csv_b:
            raw_rows_b.append(row)

    # Organise les deux liste en un dictionnaire
    dict_a = {}
    for row in raw_rows_a:
        tmp = row.split(';')
        if tmp[0][0] == "\"":
            tmp[0] = tmp[0][1:-1]
        if tmp[3] != "" and tmp[3][0] == "\"":
            tmp[3] = tmp[3][1:-1]
        dict_a[tmp[1]] = f'{tmp[0]};{tmp[2][1:-1]};{tmp[3]};{tmp[4][1:-1]};{tmp[6]}'

    # Pour donner l'impression de faire de l'optimisation
    del file_csv_a, file_csv_b

    # Sauvegarde les données organisées
    with open("database", "w") as file:
        for row in raw_rows_b:
            tmp = row.split(';')
            file.write(f'{tmp[0]};{dict_a[tmp[3]]}')

    # si tout marche, ça ne court pas, donc on peut supprimer les csv inutiles
    os.remove('identifiants_CE.csv')
    os.remove('MAJNUM.csv')

    # Très important
    return None


@logger
def load_db(name):
    """
    Charge la base de données.
    Entree: name -> Str (Nom de la base de données)
    Sortie: database -> dict
    """
    database = {}
    with open(name, 'r') as db:
        raw_db = db.readlines()
    for line in raw_db:
        tmp = line.split(';')
        database[tmp[0]] = [*tmp[1:]]
    return database

@logger
def query_db(query):
    """
    Fait une recherche dans la base de données.
    Entree: query -> Str
    Sortie: data -> list
    """
    data = []
    while len(data) == 0 and len(query) > 0:
        try:
            data = DATABASE[query]
        except:
            query = query[:-1]
    return data


@logger
def search():
    """
    Lance une recherche et affiche le resultat.
    Entree: None
    Sortie: None
    """
    # prend la demande
    numbers = ''.join(entry.get().split(' '))

    # 1er verifications
    if not numbers.isnumeric():
        err.config(text="Vous devez rentrez seulement des chiffres!")
        return None
    if len(numbers) == 10:
        numbers = numbers[1:]

    data = query_db(numbers)

    # 2d verifications
    if data == []:
        err.config(text="Pas d'informations trouvées!")
        return None

    # Affiche les valeurs
    output1.config(text=f"{data[0]}")
    output2.config(text=f"{data[1]}")
    output3.config(text=f"{data[2]}, {data[3]}")
    output4.config(text=f"{data[4][:-1]}")
    err.config(text="")

    # jamais un sans deux
    return None
    

root = tk.Tk()
root.title("Phone Lookup")

# charge la base de données sinon lance sa création
if not os.path.isfile('database'):
    first_init()
DATABASE = load_db('database')

# entrees
input_frame  =  tk.Frame(root)
input_frame.grid(row=0,  column=0,  padx=10,  pady=5)
output_frame  =  tk.Frame(root)
output_frame.grid(row=1,  column=0,  padx=10,  pady=5)

entry = tk.Entry(input_frame)
button = tk.Button(input_frame, text="Rechercher", command=search)
entry.grid(row=0,  column=0,  padx=10,  pady=2)
button.grid(row=0,  column=1,  padx=10,  pady=2)

# sorties
label1 = tk.Label(output_frame, text="Identité de l'operateur:", anchor="w")
output1 = tk.Label(output_frame, text="", font='bold', anchor="e")
label2 = tk.Label(output_frame, text="Numero SIRET:", anchor="w")
output2 = tk.Label(output_frame, text="", font='bold', anchor="e")
label3 = tk.Label(output_frame, text="Adresse:", anchor="w")
output3 = tk.Label(output_frame, text="", font='bold', anchor="e")
label4 = tk.Label(output_frame, text="Date de déclaration:", anchor="w")
output4 = tk.Label(output_frame, text="", font='bold', anchor="e")
err = tk.Label(output_frame, text="", fg="red", anchor="center")
space = tk.Label(output_frame, text="")
err.grid(row=0, column=0)
label1.grid(row=1, column=0, sticky="w")
label2.grid(row=2, column=0, sticky="w")
label3.grid(row=3, column=0, sticky="w")
label4.grid(row=4, column=0, sticky="w")
output1.grid(row=1, column=1, sticky="e")
output2.grid(row=2, column=1, sticky="e")
output3.grid(row=3, column=1, sticky="e")
output4.grid(row=4, column=1, sticky="e")
space.grid(row=5, column=0)

# une boucle, je crois
root.mainloop()