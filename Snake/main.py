import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from random import randint


class Snake:
    """
    crée un serpent
    Entree : int
    Sortie : None
    """

    def __init__(self, v, s, cs):
        """
        Paramètre le serpent.
        Entree : self, int
        Sortie : None
        """
        self.__cells_to_wait = 0
        self.__velocity = v
        self.__cells_size = cs
        self.__direction = "Down"
        self.__snake = [canvas.create_rectangle(245 + i, 150, 245 + i + cs, 150 + cs, width=2, outline='#081820',
                                                fill="#E0F8D0") for i in range(0, s * v, v)]
        canvas.itemconfigure(self.__snake[0], fill="#081820")  # change la couleur de la tete

    def __getitem__(self, item):
        """
        Renvoit les informations de la liste __snake.
        Entree : self, int
        Sortie : list, int, class, None
        """
        if item == 0:
            return canvas.coords(self.__snake[0])
        if item == 1:
            return len(self.__snake)
        if item == 3:
            return self.__snake[0]
        if item == 4:
            return self.__snake
        if item == 5:
            return self.__snake[-1]
        return None

    def diy(self, x, color):
        """
        Change la couleur du serpent.
        Entree : self, int, str
        Sortie : None
        """
        if x >= 1:
            canvas.itemconfig(self.__snake[x], fill=color)
            canvas.after(50, lambda: self.diy(x - 1, color))
        return None

    def move(self, color):
        """
        Fait avancer le serpent.
        Entree : self
        Sortie : None
        """
        if self.__cells_to_wait <= 0:
            canvas.delete(self.__snake.pop(-1))
        else:
            self.__cells_to_wait -= 1

        # Bouge la tête du serpent.
        head_coo = canvas.coords(self.__snake[0])
        canvas.itemconfig(self.__snake[0], fill="#E0F8D0")
        if self.__direction == "Up":
            self.__snake = [canvas.create_rectangle(head_coo[0], head_coo[1] - self.__velocity, head_coo[2],
                                                    head_coo[3] - self.__velocity, width=2, outline=color,
                                                    fill="#081820")] + self.__snake

        elif self.__direction == "Down":
            self.__snake = [canvas.create_rectangle(head_coo[0], head_coo[1] + self.__velocity, head_coo[2],
                                                    head_coo[3] + self.__velocity, width=2, outline=color,
                                                    fill="#081820")] + self.__snake

        elif self.__direction == "Left":
            self.__snake = [canvas.create_rectangle(head_coo[0] - self.__velocity, head_coo[1],
                                                    head_coo[2] - self.__velocity,
                                                    head_coo[3], width=2, outline=color,
                                                    fill="#081820")] + self.__snake

        elif self.__direction == "Right":
            self.__snake = [canvas.create_rectangle(head_coo[0] + self.__velocity, head_coo[1],
                                                    head_coo[2] + self.__velocity,
                                                    head_coo[3], width=2, outline=color,
                                                    fill="#081820")] + self.__snake

        return None

    def change_dir(self, event):
        """
        Change la direction de la tête et empêche le retour en arrière.
        Entree : self, event
        Sortie : None
        """
        head = canvas.coords(self[3])
        cells = self.__snake
        if event.keysym == "Up" and cells[1] in canvas.find_overlapping(head[0], head[1] - self.__velocity, head[2],
                                                                        head[3] - self.__velocity):
            return None
        if event.keysym == "Down" and cells[1] in canvas.find_overlapping(head[0], head[1] + self.__velocity, head[2],
                                                                          head[3] + self.__velocity):
            return None
        if event.keysym == "Left" and cells[1] in canvas.find_overlapping(head[0] - self.__velocity, head[1],
                                                                          head[2] - self.__velocity, head[3]):
            return None
        if event.keysym == "Right" and cells[1] in canvas.find_overlapping(head[0] + self.__velocity, head[1],
                                                                           head[2] + self.__velocity, head[3]):
            return None
        self.__direction = event.keysym  # sinon, on applique le changement de direction
        return None

    def add_cells(self, x):
        """
        Ajoute x cellules au serpent;
        Entree : self, int
        Sortie : None
        """
        self.__cells_to_wait = x
        return None

    def self_eater(self, pomme):
        """
        Verifie que le serpent ne rentre pas en contact avec lui-même ou avec le bord.
        Entree : self, instance de apple
        Sortie : bool
        """
        c_s = canvas.coords(self[3])
        tup = canvas.find_overlapping(c_s[0], c_s[1], c_s[2], c_s[3])
        if len(tup) > 2:
            if pomme[3] in tup:
                return False
            return True
        return False


class Apple:
    """
    Crée une pomme aux coordonnées x, y et lui donne un type.
    """

    def __init__(self, s):
        """
        Paramètre la classe.
        Entree : self, int
        Sortie : None
        """
        if randint(1, 10) == 10:
            self.__color = 'yellow'
        else:
            self.__color = 'red'
        y = randint(20, 450)
        x = randint(20, 450)
        while len(canvas.find_overlapping(x, y, x + 10, y + 10)) > 1:
            y = randint(20, 450)
            x = randint(20, 450)
        self.__apple = canvas.create_oval(x, y, x + s, y + s, fill=self.__color, width=2, outline='#081820')

    def __getitem__(self, item):
        """
        Revoit les informations de l'instance.
        Entree : self, int
        Sortie : list, instance, str
        """
        if item == 0:
            return canvas.coords(self.__apple)
        if item == 1:
            return self.__color
        if item == 3:
            return self.__apple
        return None

    def delete_a(self):
        """
        Suprime la pomme.
        Entree : self
        Sortie : None
        """
        canvas.delete(self.__apple)
        return None


def info():
    """
    Affiche une boite d'information.
    Entree : None
    Sortie : None
    """
    tkinter.messagebox.showinfo(title=None,
                                message="Blockade, créé par Gremlin en 1976, est le premier jeu de type snake connu. "
                                        "Rapidement aprés sa création, il est devenu un succés sur les bornes "
                                        "d'arcade. Les premières"
                                        "apparitions du terme 'snake' remonte plutôt à 1982 avec des clones tels que "
                                        "'Snake Byte'.\n\nLe clone ci-présent a été fait par Llufollis.")
    return None


def main():
    """
    Gére le jeu.
    Entree : None
    Sortie : None
    """

    def start(diff):
        """
        Commence le jeu.
        Entree : int
        Sortie : None
        """
        #  Reset le canva.
        canvas.delete("all")
        canvas.create_image(0, 0, image=fond, anchor="nw")
        canvas.create_window(260, 565, window=label)
        canvas.create_rectangle(20, 20, 520, 520, outline="red")

        #  Crée le serpent.
        if diff == 1 or diff == 0:
            serpent = Snake(6, 6, 5)
            diff = "facile"
        elif diff == 2:
            serpent = Snake(11, 6, 10)
            diff = "normal"
        else:
            serpent = Snake(21, 6, 20)
            diff = "HARDCORE"
        pomme = Apple(10)
        score = 0

        #  Attache les touches aux actions.
        root.bind("<Up>", serpent.change_dir)
        root.bind("<Down>", serpent.change_dir)
        root.bind("<Right>", serpent.change_dir)
        root.bind("<Left>", serpent.change_dir)
        label.config(text=f'score: {score} Taille: {serpent[1]}')

        #  Lance le jeu.
        game(serpent, pomme, score, diff)

        return None

    def game(serpent, pomme, score, diff):
        """
        Gére les deplacements du serpent, l'apparition de la pomme et la fin du jeu.
        Entree : instance de serpent, de pomme, int
        Sortie : None
        """
        c_p = canvas.coords(pomme[3])
        h_color = '#081820'
        if serpent[3] in canvas.find_overlapping(c_p[0], c_p[1], c_p[2], c_p[3]):

            if pomme[1] == 'red':
                score += 1
                serpent.add_cells(serpent[1] * 20 // 100)
                h_color = 'red'
            else:
                score += 5
                serpent.add_cells(serpent[1] * 50 // 100)
                h_color = 'yellow'
            pomme.delete_a()
            pomme = Apple(10)
            label.config(text=f'score: {score} Taille: {serpent[1]}')

        if serpent.self_eater(pomme):
            serpent.diy(serpent[1] - 1, "red")
            rep = tkinter.messagebox.askretrycancel(title=None,
                                                    message="Oups, vous êtes devenu de la purée de serpent.")
            with open("data/save.txt", "r") as file:
                save = file.read()
            if save.split(";")[0] == "" or int(save.split(";")[0]) < score:
                with open("data/save.txt", "w") as file:
                    file.write(f"{str(score)};{diff}")
            if rep:
                main()
                return None
            else:
                root.destroy()
            return None

        else:
            serpent.move(h_color)
            canvas.after(60, lambda: game(serpent, pomme, score, diff))
        return None

    def diff_change(*args):
        """
        Change le texte de diff_affi.
        Entree : event
        Sortie : None
        """
        if round(diff.get()) == 1 or round(diff.get()) == 0:
            diff_affi.configure(text="Difficulté: Facile", foreground="green")
        elif round(diff.get()) == 2:
            diff_affi.configure(text="Difficulté: Normal", foreground="black")
        else:
            diff_affi.configure(text="Difficulté: HARDCORE", foreground="red")
        return None

    #  Reset le canva.
    canvas.delete("test")

    #  Tente de recupérer l'ancien meilleur score.
    try:
        with open("data/save.txt", "r") as file:
            save_s = file.read()
            text_score = "Meilleur score:\n"+f"{save_s.split(';')[0]} en difficulté {save_s.split(';')[1]}"
    except FileNotFoundError:
        with open("data/save.txt", "w") as file:
            file.write("0;None")
            text_score = "Meilleur score:\nVous n'avez pas de scores pour le moment\n lancez une partie :) !"

    #  Configure les boutons.
    best_score = ttk.Label(canvas, text=text_score,
                           font=("Helvetica", 14), background="#E0F8D0", justify='center')
    label = ttk.Label(
        root,
        text='Bienvenu sur Blockade Py !',
        font=("Helvetica", 14), background="#E0F8D0")
    diff = tk.DoubleVar()
    diff_selec = ttk.Scale(canvas, from_=1, to=3, orient="horizontal", command=diff_change, variable=diff)
    start_button = ttk.Button(canvas, text="Commencer", command=lambda: start(round(diff.get())), style='my.TButton')
    info_button = ttk.Button(canvas, text="?", command=info, style='info.TButton', width=3)
    diff_affi = ttk.Label(
        root,
        text='Difficulté: Facile',
        font=("Helvetica", 14), background="#E0F8D0", foreground="green")

    #  Affiche les widgets.
    canvas.create_window(270, 70, window=best_score)
    canvas.create_window(270, 565, window=label)
    canvas.create_window(499, 563, window=info_button)
    canvas.create_window(270, 220, window=diff_affi)
    canvas.create_window(270, 250, window=diff_selec)
    canvas.create_window(270, 300, window=start_button)
    canvas.create_image(0, 0, image=fond, anchor="nw")

    return None


if __name__ == '__main__':
    # Création de la fenetre.
    root = tk.Tk()
    root.title("Snack")
    root.iconphoto(False, tk.PhotoImage(file='data/logo.png'))
    root.resizable(False, False)

    # Définition du canva.
    fond = tk.PhotoImage(file="data/fond.png")
    canvas = tk.Canvas(root, width=540, height=600, bg='black')
    canvas.pack(fill="both", expand=True)

    # Style des boutons (ttk).
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('my.TButton', bordercolor="#081820", bg="#e0f8d0")
    style.configure('info.Tbutton', borderwidth=0, bordercolor="#081820", bg="#e0f8d0")

    #  Démarre le jeu.
    main()

    # Boucle de la fenêtre.
    root.mainloop()
