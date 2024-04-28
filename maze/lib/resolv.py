from lib.maze import gen_maze
from lib.pile import Pile
from random import shuffle
from tkinter import Canvas, Tk, Button
import tkinter.messagebox
from time import time


def find_maze_start(maze: list) -> tuple:
    """
    Find the coo of the maze's entrance.
    In maze: list
    Out: tuple
    """
    maze_end, mazex = len(maze), len(maze[0])
    for i in range(maze_end):
        for l in range(mazex):
            if maze[i][l] == ">":
                return (l, i)

    # si le labyrinthe n'a pas d'entree
    tkinter.messagebox.showinfo(
        title="Amaze!", message="Il y a des erreurs dans le labyrinthe!"
    )
    raise Exception("Il y a des erreurs dans le labyrinthe!")
    return (-1, -1)


def find_available_moves(
    curr_x: int, curr_y: int, sizex: int, sizey: int, maze: list
) -> list:
    """
    renvoit les coordonnees possible pour certain x et y
    In curr_x, curry, sizex, sizey, maze: int, int, int, int, list
    Out: list
    """
    moves = [
        (curr_x - 1, curr_y),
        (curr_x + 1, curr_y),
        (curr_x, curr_y - 1),
        (curr_x, curr_y + 1),
    ]
    return [
        (x, y)
        for x, y in moves
        if 0 < x < sizex and 0 < y < sizey and maze[y][x] in [" ", "O"]
    ]


def rectangle(
    x: int, y: int, taille_cells: int, couleur: str, canvas: Canvas, *, cailloux=None
) -> Pile:
    """
    cree un carre au coordonnees x et y
    In x, y, taille_cells, couleur, canvas, cailloux = int, int, int, str, Canvas(), Pile()
    Out cailloux: Pile()
    """
    if cailloux == None:
        canvas.create_rectangle(
            (x * taille_cells) - taille_cells / 2,
            (y * taille_cells) - taille_cells / 2,
            ((x + 1) * taille_cells) - taille_cells / 2,
            ((y + 1) * taille_cells) - taille_cells / 2,
            width=0,
            fill=couleur,
            tags=("path",),
        )
    else:
        cailloux.empiler(
            canvas.create_rectangle(
                (x * taille_cells) - taille_cells / 2,
                (y * taille_cells) - taille_cells / 2,
                ((x + 1) * taille_cells) - taille_cells / 2,
                ((y + 1) * taille_cells) - taille_cells / 2,
                width=0,
                fill=couleur,
                tags=("path",),
            )
        )
    return cailloux


def win(
    x: int, y: int, taille_cells: int, start: int, canvas: Canvas, button: Button
) -> None:
    """
    gere la fin du programme, quand la tete trouve la fin du labyrinthe.
    In x, y, taille_cells, start, canvas, button: int, int, int, int, Canva(), Button()
    Out: None
    """
    # reactive le bouton de resolution
    button["state"] = "active"

    # affiche un carre vert sur la fin du labyrinthe
    rectangle(x, y, taille_cells, "green", canvas)

    # calcule le temps
    end = time()
    seconds = round(end) - round(start)
    heures, minutes = 0, 0
    while seconds > 59:
        minutes += 1
        seconds -= 60
        if minutes > 59:
            heures += 1
            minutes -= 60
    if minutes > 0:
        m = f"{minutes}min "
    else:
        m = ""
    if heures > 0:
        h = f"{heures}h "
    else:
        h = ""

    # affiche le temps
    tkinter.messagebox.showinfo(
        title="Amaze!", message=f"Labyrinthe résolu en {h}{m}{seconds}s!"
    )

    return None


def delete_old_path(canvas: Canvas) -> None:
    """
    reset l'ancien chemin.
    In: canvas: Canvas()
    Out: None
    """
    items = canvas.find_all()

    for item_id in items:
        tags = canvas.gettags(item_id)
        if "path" in tags:
            canvas.delete(item_id)
    return None


def resolve(
    maze: list,
    canvas: Canvas,
    root: Tk,
    taille_cells: int,
    *,
    button=None,
    poucet=None,
    x=None,
    y=None,
    cailloux=None,
    start=None,
) -> None:
    """
    Resout le labyrinthe, compte le temps de resolution et grise le bouton de resolution
    In :
        maze (list)
        canvas (Canvas())
        root (Tk())
        taille_cells(int)
        button (Button())
        poucet (Pile())
        x (int)
        y (int)
        cailloux (Pile())
        start (int)
    Out :
        None
    """
    if poucet != None and poucet.est_vide():
        try:
            find_available_moves(x, y, maze) == []
        except:
            button["state"] = "active"
            tkinter.messagebox.showinfo(
                title="Amaze!", message=f"Labyrinthe impossible!"
            )
            del poucet, cailloux, x, y, start, maze
            return None

    if poucet == None:  # initialisation
        delete_old_path(canvas)
        button["state"] = "disabled"
        start = time()
        x, y = find_maze_start(maze)
        rectangle(x, y, taille_cells, "black", canvas)
        sizex, sizey = len(maze[0]), len(maze)
        poucet = Pile()
        cailloux = Pile()

    sizex, sizey = len(maze[0]), len(maze)
    suiv = find_available_moves(x, y, sizex, sizey, maze)

    if suiv != []:  # si on peut avancer
        shuffle(suiv)
        x, y = suiv[0][0], suiv[0][1]

        if maze[y][x] == "O":
            win(x, y, taille_cells, start, canvas, button)
            del poucet, cailloux, x, y, start, maze
            return None

        maze[y][x] = "V"
        poucet.empiler((x, y))
        cailloux = rectangle(x, y, taille_cells, "red", canvas, cailloux=cailloux)

    else:  # sinon on recule
        coo = poucet.depiler()
        x, y = coo[0], coo[1]

        next_suiv = find_available_moves(x, y, sizex, sizey, maze)
        for x2, y2 in next_suiv:
            if maze[y][x] == "O":
                win(x, y, taille_cells, end, canvas, button)
                del poucet, cailloux, x, y, start, maze
                return None
        if next_suiv == []:
            edit = cailloux.depiler()
            canvas.itemconfig(edit, fill="#a6a6a6")
        else:
            poucet.empiler((x, y))

    root.after(
        5,
        lambda: resolve(
            maze,
            canvas,
            root,
            taille_cells,
            poucet=poucet,
            x=x,
            y=y,
            cailloux=cailloux,
            start=start,
            button=button,
        ),
    )
