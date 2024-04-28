from random import shuffle, randint, choice
from lib.pile import *


def creation(x: int, y: int) -> list:
    """
    Renvoie une liste de listes qui servent de création au labyrinthe.
    In x, y: int
    Out tab: list
    """
    if x % 2 == 0:
        x += 1
    if y % 2 == 0:
        y += 1

    tab = [
        ["?" if i % 2 != 0 and j % 2 != 0 else "#" for j in range(y)] for i in range(x)
    ]

    entrance_exit = choice(["horizontal", "vertical"])

    if entrance_exit == "horizontal":
        entry_point = (2 * randint(1, x // 2) - 1, 0)
        exit_point = (2 * randint(1, x // 2) - 1, y - 1)
    else:
        entry_point = (0, 2 * randint(1, y // 2 - 1) - 1)
        exit_point = (x - 1, 2 * randint(1, y // 2 - 1) - 1)

    tab[entry_point[0]][entry_point[1]] = ">"
    tab[exit_point[0]][exit_point[1]] = "O"

    return tab


def gen_maze(sizex: int, sizey: int, lab=None, cells=None, x=None, y=None) -> list:
    """
    Cree un labyrinthe avec un algorithme de recherche en profondeur (depth-first search).
    Entree x, y, lab cells: int, int, list, Pile
    Sortie lab: list
    """
    if cells is None:
        lab = creation(sizey, sizex)
        valid_positions = [
            (x, y)
            for y in range(1, sizey - 2)
            for x in range(1, sizex - 2)
            if lab[y][x] != "#"
        ]
        pos = randint(0, len(valid_positions) // 2 - 1) * 2
        x, y = valid_positions[pos]
        cells = Pile()
        lab[y][x] = " "
        cells.empiler((x, y))

    while len(cells) > 0:
        suiv = []
        for coo in [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]:
            if 0 < coo[0] and 0 <= coo[1]:
                if coo[0] < sizex and coo[1] < sizey:
                    if lab[coo[1]][coo[0]] == "?":
                        suiv.append(coo)

        if suiv != []:
            shuffle(suiv)
            diff = ((suiv[0][0] - x) // 2, (suiv[0][1] - y) // 2)
            x, y = suiv[0][0], suiv[0][1]
            lab[y - diff[1]][x - diff[0]] = " "
            lab[y][x] = " "
            cells.empiler((x, y))
        else:
            coo = cells.depiler()
            x, y = coo[0], coo[1]

    return lab
