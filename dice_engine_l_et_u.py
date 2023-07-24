from random import randint, choices, sample
import re

RE_SEPARATORS = re.compile("[,;]")
RE_ELEMENTS = re.compile("(?<=(l|u).)[^$\#]+")

def trouver_elements_et_n_fois(cmd:str) -> tuple[list[str], int]:
    elements = re.search(RE_ELEMENTS, cmd)
    assert elements != None, "Syntaxe invalide, aucun élément n'est présent"

    nombre_fois = cmd[:elements.start()-2]
    assert nombre_fois.isdigit(), "Commande invalide, le nombre d'élément choisis est invalide"
    nombre_fois = int(nombre_fois)

    if "#" in cmd:
        commentaire = cmd[cmd.index("#"):]
    else:
        commentaire = ""

    elements = re.split(RE_SEPARATORS, elements.group())

    assert nombre_fois >= 1, "Syntaxe invalide, le nombre d'éléments choisis est inférieur à 1"

    return elements, nombre_fois, commentaire

def formater_resultat(commentaire, elements):
    if type(elements) == str and not elements.startswith(" "):
        elements = " "+startswith
    return "Résultat du tirage : \n{0}\n{1}".format(commentaire, str(elements)[1:-1])

def exec_l(cmd:str):
    elements, nombre_fois, commentaire = trouver_elements_et_n_fois(cmd)      
    return formater_resultat(commentaire, choices(elements, k=nombre_fois))

def exec_u(cmd:str):
    elements, nombre_fois, commentaire = trouver_elements_et_n_fois(cmd)
    assert nombre_fois <= len(elements), "commande invalide, le nombre d'éléments choisis est supérieur au nombre de choix possible"
    
    choix = sample(elements, nombre_fois)

    return formater_resultat(commentaire, choix)
