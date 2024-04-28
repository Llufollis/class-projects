def btt(dico_binaire, chaine_bin):
    """
    Bin To Text (Arno)
    In dico_binaire, chaine_bin: dict, str
    Out chaine_decomp: str
    """
    chaine_decomp, current_code = "", ""
    dico_inv = {valeur: clef for clef, valeur in dico_binaire.items()}
    for bit in chaine_bin:
        current_code += bit
        try:
            chaine_decomp += dico_inv[current_code]
            current_code = ""
        except KeyError:
            pass
    return chaine_decomp


def ttb(dico_bin, text_in):
    """
    Text To Bin (Octave)
    In dico_bin, text_in : dict, str
    out: text_bin: str
    """
    text_bin_list = [dico_bin[elem] for elem in text_in if elem in dico_bin]
    text_bin = "".join(text_bin_list)
    return text_bin


def compression(maze):
    """
    Convertit un labyrinthe str en un array de bits.
    In maze: str
    Out: bits array
    """
    dico_decomp = {" ": "000", ">": "100", "O": "101", ":": "011", "#": "001"}
    binmaze = ttb(dico_decomp, maze)
    return bytes(int(binmaze[i : i + 3], 2) for i in range(0, len(binmaze), 3))
