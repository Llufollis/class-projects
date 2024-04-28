class Cellule:
    def __init__(self, x):
        """Constructeur de la classe Cellule :
        valeur contient la valeur stockee dans la cellule.
        suivant contient le pointeur vers la cellule suivante.
        suivant est toujours initialise a None."""
        self.valeur = x
        self.suivant = None

    def __del__(self):
        """Destructeur de la classe Cellule :
        Supprime la valeur, le pointeur suivant et la cellule elle-meme."""
        del self.valeur
        del self.suivant
        del self


class Pile:
    def __init__(self):
        """Constructeur de la classe Pile :
        sommet contient le pointeur vers la cellule suivante.
        sommet est toujours initialise a None."""
        self.sommet = None
        self.__taille = 0

    def est_vide(self):
        """Renvoie True si la pile est vide, False sinon.
        Entree : aucune.
        Sortie : booleen."""
        return self.__taille == 0

    def __len__(self):
        """Renvoie la taille de la pile.
        Entree : aucune.
        Sortie : entier positif."""
        return self.__taille

    def empiler(self, x):
        """Ajoute x en tete de pile.
        On cree une instance de cellule avec la valeur x
        et suivant pointe vers la tete.
        Entree : x est une valeur possible.
        Sortie : aucune."""
        self.__taille += 1  # la taille augmente de 1
        if self.est_vide():
            self.sommet = Cellule(x)
        else:
            nouveau_sommet = Cellule(x)
            nouveau_sommet.suivant = (
                self.sommet
            )  # on relie la Cellule a la suite de la Pile
            self.sommet = (
                nouveau_sommet  # le sommet de la pile devient la nouvelle Cellule
            )
        return None

    def depiler(self):
        """Supprimer la Cellule de sommet et renvoie sa valeur.
        Entree : aucune.
        Sortie : aucune."""
        if self.est_vide():
            raise BrokenPipeError("La Pile est vide !")
        cellule_a_depiler = self.sommet
        self.sommet = (
            cellule_a_depiler.suivant
        )  # on court-circuite la Cellule de sommet
        retour = cellule_a_depiler.valeur  # on recupere sa valeur
        del cellule_a_depiler  # on la supprime
        self.__taille -= 1  # on met a jour la taille de la pile
        return retour
