from lib.txttobinary import btt, compression
from lib.maze import gen_maze
from lib.resolv import resolve
from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
from copy import deepcopy


def save(maze: list, bouton: Button) -> None:
    """
    Cree un fichier binaire avec les donnees du labyrinthe.
    In tab_maze, bouton : list, Button()
    Out : None
    """
    bouton["state"] = "disable"  # evite que l'utilisateur spam le bouton ensuite

    try:  # permet de connaitre la derniere sauvegarde
        with open("save/savelist.txt", "r") as savelist:
            savefilestr = int(savelist.readline().split(";")[-2]) + 1
    except FileNotFoundError:
        savefilestr = "0"

    str_maze = ":".join("".join(row) for row in maze)  # convertit le labyrinthe en str
    bin_maze = compression(str_maze)  # convert str_maze en un array de 0 et 1

    with open(f"save/save{savefilestr}.bin", "wb") as binfile:
        binfile.write(bin_maze)

    with open("save/savelist.txt", "a") as savelist:
        savelist.write(f"{savefilestr};")  # ajoute le numero de la sauvegarde

    tkinter.messagebox.showinfo(
        title="Amaze!",
        message=f"Labyrinthe sauvegardé!\n (~/save/save{savefilestr}.bin)",
    )
    return None


def resize_image(image_path: str, width: int, height: int) -> ImageTk.PhotoImage:
    """
    Resize and return a image with  a given path to a given size.
    In image_path, width, height: str, int, int
    Out :PhotoImage()
    """
    original_image = Image.open(image_path)
    # resampling_mode = Image.Resampling.NEAREST if width > 50 else Image.Resampling.BICUBIC # pas possible avec windows
    # resized_image = original_image.resize((width, height), resample=resampling_mode)
    resized_image = original_image.resize((width, height))
    return ImageTk.PhotoImage(resized_image)


def display(tab: list, activ_save=False) -> None:
    """
    Display the maze with sweet sweet handmade tiles.
    In tab: list
    Out : None
    """
    root = Tk()
    root.title("Amaze!")
    root.configure(bg="white")
    root.resizable(False, False)
    root.iconphoto(False, PhotoImage(file="assets/logo.png"))

    # definit la taille d'une cellule
    screen_height = root.winfo_screenheight() - 100
    tcellx = round(screen_height / len(tab))
    tcelly = round(screen_height / len(tab[0]))
    if tcellx > tcelly:
        tcell = tcelly
    else:
        tcell = tcellx
    del tcellx, tcelly

    maze_canva = Canvas(
        root,
        width=(len(tab[0]) - 1) * tcell,
        height=(len(tab) - 1) * tcell,
        bg="white",
        bd=0,
    )

    images = {  # doit etre dans la loop tk pour ne pas etre garbage collected
        "a": resize_image("assets/end_up.png", tcell, tcell),
        "b": resize_image("assets/end_down.png", tcell, tcell),
        "c": resize_image("assets/end_left.png", tcell, tcell),
        "d": resize_image("assets/end_right.png", tcell, tcell),
        "ab": resize_image("assets/straight.png", tcell, tcell),
        "cd": resize_image("assets/straight_down.png", tcell, tcell),
        "da": resize_image("assets/down_right.png", tcell, tcell),
        "ca": resize_image("assets/down_left.png", tcell, tcell),
        "cb": resize_image("assets/up_left.png", tcell, tcell),
        "db": resize_image("assets/up_right.png", tcell, tcell),
        "cab": resize_image("assets/three_left.png", tcell, tcell),
        "dab": resize_image("assets/three_right.png", tcell, tcell),
        "cda": resize_image("assets/three_down.png", tcell, tcell),
        "cdb": resize_image("assets/three_up.png", tcell, tcell),
        "cdab": resize_image("assets/cross.png", tcell, tcell),
        " ": resize_image("assets/empty.png", tcell, tcell),
        "end": resize_image("assets/end.png", tcell, tcell),
        "start": resize_image("assets/start.png", tcell, tcell),
        "return": resize_image("assets/return.png", 20, 20),
        "brain": resize_image("assets/brain.png", 20, 20),
        "save": resize_image("assets/save.png", 20, 20),
    }

    # applique les images
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            name = ""
            if tab[i][j] == " ":
                for coo in [
                    (j - 1, i, "c"),
                    (j + 1, i, "d"),
                    (j, i - 1, "a"),
                    (j, i + 1, "b"),
                ]:
                    if 0 <= coo[0] and 0 <= coo[1]:
                        if tab[coo[1]][coo[0]] in [" ", "O", ">"]:
                            name += coo[2]
                maze_canva.create_image(
                    j * tcell - 1, i * tcell - 1, image=images[name]
                )
            elif tab[i][j] == "O":
                maze_canva.create_image(
                    j * tcell - 1, i * tcell - 1, image=images["end"]
                )
            elif tab[i][j] == ">":
                maze_canva.create_image(
                    j * tcell - 1, i * tcell - 1, image=images["start"]
                )
            else:
                maze_canva.create_image(j * tcell - 1, i * tcell - 1, image=images[" "])
    maze_canva.pack(side=LEFT)

    # cree les boutons
    buttons_canva = Canvas(root, background="white")
    save_button = Button(
        buttons_canva,
        text="Sauvegarder",
        command=lambda: save(tab, save_button),
        image=images["save"],
        compound=LEFT,
    )
    resolv_button = Button(
        buttons_canva,
        text="R\u00e9soudre",
        command=lambda: resolve(
            deepcopy(tab), maze_canva, root, tcell, button=resolv_button
        ),
        image=images["brain"],
        compound=LEFT,
    )
    return_button = Button(
        buttons_canva,
        text="Retour",
        command=lambda: start(root),
        image=images["return"],
        compound=LEFT,
    )

    # desactive le bouton "Sauvegarder"
    if not activ_save:
        save_button["state"] = "disabled"

    resolv_button.pack(padx=20, pady=10)
    save_button.pack(padx=20, pady=10)
    return_button.pack(padx=20, pady=10)
    buttons_canva.pack(side=LEFT)

    root.mainloop()


def load_save(file_nb: int, to_close: Tk) -> None:
    """
    Charge une sauvegarde .bin l'affiche
    In file_nb, to_close: int
    Out: None
    """
    if to_close is not None:
        to_close.destroy()

    with open(f"save/save{file_nb}.bin", "rb") as file:
        binary_data = file.read()

    bin_string = "".join(
        format(byte, "03b") for byte in binary_data
    )  # Les fichiers de sauvegarde sont encodes sur 3 bits

    dico_decomp = {" ": "000", ">": "100", "O": "101", ":": "011", "#": "001"}
    deco_list = btt(dico_decomp, bin_string).split(":")
    maze = []
    for i in deco_list:
        tmp = []
        for l in i:
            tmp.append(l)
        maze.append(tmp)

    display(maze)

    return None


def valid_values(varx: StringVar, vary: StringVar, to_close: Tk, info: Label) -> None:
    """
    verifie des les valeurs x et y de creation du labyrinthe sont correctes
    In varx, vary, to_close, info = StringVar(), StringVar(), Tk(), Label()
    Out : None
    """
    try:
        x, y = int(varx.get()), int(vary.get())
        if x < 5 or x > 500 or y < 5 or y > 500:
            info.config(
                text="La taille du labyrinthe doit \u00eatre\n entre 5x5 et 500x500 (\u25d4\u005f\u25d4)",
                foreground="red",
            )
        else:
            to_close.destroy()
            maze = gen_maze(x, y)
            display(maze, True)
    except:
        info.config(
            text="Vous devriez essayer avec\n des chiffres (\uffe2\u005f\uffe2)",
            foreground="red",
        )

    return None


def start(to_close=None) -> None:
    """
    Affiche la fenetre de selection du labyrinthe
    In to_close: Tk()
    Out: None
    """
    if to_close is not None:
        to_close.destroy()

    root = Tk()
    root.title("Amaze!")
    root.resizable(False, False)
    root.configure()
    root.iconphoto(False, PhotoImage(file="assets/logo.png"))

    top_frame = Frame(root)
    entry_frame = Frame(top_frame)
    bottom_frame = Frame(root)

    info_label = Label(
        top_frame,
        text="Super Labyrinthe Mega Ultra HD\n 4K Premium ChatPGT IA 14.5",
        font=("Times New Roman", 15, "bold"),
        justify=CENTER,
        foreground="blue",
    )
    info_label.pack_propagate(0)
    info_label.pack(side=TOP)
    txtx = Label(entry_frame, text="x", font=("Times New Roman", 11, "bold"))

    sizex_var = StringVar(root)
    sizex_var.set("10")
    sizey_var = StringVar(root)
    sizey_var.set("10")

    sizex_entry = Entry(entry_frame, textvariable=sizex_var)
    sizex_entry.pack(padx=5, pady=10, side="left")

    txtx.pack(side=LEFT)

    sizey_entry = Entry(entry_frame, textvariable=sizey_var)
    sizey_entry.pack(padx=5, pady=10, side="left")

    create_button = Button(
        top_frame,
        text="G\u00e9n\u00e9rer un labyrinthe",
        command=lambda: valid_values(sizex_var, sizey_var, root, info_label),
    )
    create_button.pack(pady=10, side="bottom")

    try:
        with open("save/savelist.txt", "r") as savelist:
            option_save = savelist.readline().split(";")[:-1]

        save_var = StringVar(root)
        save_var.set(option_save[0])

        option_menu_save = OptionMenu(bottom_frame, save_var, *option_save)
        save_button = Button(
            bottom_frame,
            text="Charger un labyrinthe",
            command=lambda: load_save(save_var.get(), root),
        )
        save_button.pack(pady=10, side="bottom")
        option_menu_save.pack(pady=10, side="bottom")

        entry_frame.pack()
        top_frame.pack(padx=20, pady=20, side="top")
        bottom_frame.pack(padx=20, pady=20)
    except FileNotFoundError:
        top_frame.pack(padx=20, pady=20, side="top")
        entry_frame.pack()
        create_button.pack(pady=10)

    root.mainloop()


start()
