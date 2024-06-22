from PIL import Image
import numpy as np


def merge_image(img1, img2, depth):
    """
    Assemble deux images.
    Entree:
        img1 -> str (chemin de l'image de base)
        img2 -> str (chemin de l'image a cacher)
        depth -> int (profondeur de l'assemblage)
    Sortie: Pillow Image
    """
    new_image = np.zeros((*img1.size, 3), dtype=np.uint8)
    img2 = img2.convert("1").convert("RGB")
    img1_a = np.array(img1)
    img2_a = np.array(img2)
    for y in range(len(img1_a)):
        for x in range(len(img1_a[0])):
            for i in range(3):
                new_image[y][x][i] = int(
                    (
                        (format(img1_a[y][x][i], "0>8b")[:-depth])
                        + (str(img2_a[y][x][0] // 255)) * depth
                    ),
                    2,
                )
    return Image.fromarray(new_image)


def return_image(img, depth):
    """
    Desassemble les images.
    Entree:
        img -> str (chemin de l'image assemblee)
        depth -> int (profondeur de l'assemblage)
    Sortie: Pillow Image
    """
    new_image = np.zeros((*img.size, 3), dtype=np.uint8)
    img_a = np.array(img)
    for y in range(len(img_a)):
        for x in range(len(img_a[0])):
            for i in range(3):
                new_image[y][x][i] = int(bin(img_a[y][x][i])[-1]) * 255
    return Image.fromarray(new_image)


def diff_calc(img1, img2):
    """
    Calcule la difference entre deux images.
    Entree:
        img1 -> str (chemin de l'image 1)
        img2 -> str (chemin de l'image 2)
    Sortie: int (pourcentage de similarite)
    """
    diff = 0
    img1_a = np.array(Image.open(img1))
    img2_a = np.array(Image.open(img2))
    for y in range(len(img1_a)):
        for x in range(len(img1_a[0])):
            for i in range(3):
                if img1_a[y][x][i] != img2_a[y][x][i]:
                    diff += 1
    return (diff * 100) // (len(img1_a) * len(img1_a[0]) * 3)


def create_image(original="", output="", depth=0, *, hide=""):
    """
    Permet de faire appel aux fonction de cachage/decachage et de sauvegarder le resultat.
    Entree:
        original -> str (chemin de l'image original)
        output -> str (chemin de sortie de l'image)
        depth -> int (profondeur de l'assemblage)
        hide -> str (chemin de l'image a cacher)
    Sortie: None
    """
    img_orig = Image.open(original)
    if hide != "":
        img_hide = Image.open(hide)
        img = merge_image(img_orig, img_hide, depth)
    else:
        img = return_image(img_orig, depth)
    img.save(output)
    return None


if __name__ == "__main__":
    if input("Decacher (0), Cacher (1): ") == "1":
        path1 = input("Chemin de l'image de base: ")
        path2 = input("Chemin de l'image à cacher: ")
        path3 = input(f"Chemin de la nouvelle image (sinon {path1}): ")
        profondeur = int(input("Profondeur d'insertion de l'image: "))
        if path3 == "":
            path3 = path1
        create_image(original=path1, hide=path2, depth=profondeur, output=path3)
        print(
            f"La nouvelle et l'ancienne image on un taux de difference de {diff_calc(path1, path3)}%"
        )
    else:
        path1 = input("Chemin de l'image: ")
        path2 = input(f"Chemin de la nouvelle image (sinon {path1}): ")
        profondeur = int(input("Profondeur d'insertion de l'image: "))
        if path2 == "":
            path2 = path1
        create_image(original=path1, depth=profondeur, output=path2)
