import re
from math import sqrt

def remove_punctuation(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

def remove_pronouns(text):
    pronouns = [
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
        "me", "te", "se", "le", "la", "lui", "les", "leur", "y", "en",
        "moi", "toi", "soi", "toi-même", "vous-même", "lui-même", "elle-même",
        "eux-même", "elles-même", "nous-même", "me-même", "te-même", "on"
    ]
    pattern = r'\b(?:' + '|'.join(pronouns) + r')\b'
    return re.sub(pattern, '', text, flags=re.IGNORECASE)

def remove_miscellaneous(text):
    prepositions = [
        "de", "du", "des", "d'", "le", "la", "les", "l'", "un", "une", "au",
        "aux", "en", "dans", "sur", "sous", "vers", "à", "chez", "par", "pour",
        "avec", "sans", "entre", "pendant", "depuis", "devant", "derrière",
        "près", "loin", "jusque", "jusqu'à", "à côté de", "et", "ou", "qu", "s'",
        "m'", "t'", "n'", "a", "c'"
    ]
    pattern = r'\b(?:' + '|'.join(prepositions) + r')\b'
    return re.sub(pattern, '', text, flags=re.IGNORECASE)

def remove_line_breaks(text):
    return text.replace('\n', '')

def text_to_vector(text, all_words):
    words = text.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return [word_count.get(word, 0) for word in all_words]

def cosine_similarity(vec1, vec2):
    dot_product = sum(x * y for x, y in zip(vec1, vec2))
    norm1 = sqrt(sum(x ** 2 for x in vec1))
    norm2 = sqrt(sum(x ** 2 for x in vec2))
    return dot_product / (norm1 * norm2)

def load_text(name):
    with open(f'{name}.txt', 'r') as file:
        return file.read()

text1 = load_text("Le_Horla")
text2 = load_text("Vingt_mille_lieues_sous_les_mers")

text1_cleaned = remove_line_breaks(remove_miscellaneous(remove_pronouns(remove_punctuation(text1.lower()))))
text2_cleaned = remove_line_breaks(remove_miscellaneous(remove_pronouns(remove_punctuation(text2.lower()))))

all_words = set(text1_cleaned.split()).union(set(text2_cleaned.split()))
vec1 = text_to_vector(text1_cleaned, all_words)
vec2 = text_to_vector(text2_cleaned, all_words)

similarity = cosine_similarity(vec1, vec2)
print(f"Les textes ont un score de similarité de {round(similarity, 3)}. Ils ont été convertit en deux vecteurs de {len(vec1)} dimensions.")