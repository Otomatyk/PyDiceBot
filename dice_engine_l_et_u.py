from random import randint, choice
import re

REGEX_SEPARATORS = re.compile("[,;]")
REGEX_ELEMENTS = re.compile("(?<=(l|u).)[^$]+")

def trouver_elements_et_n_fois(cmd:str) -> tuple[list[str], int]:
    elements = re.search(REGEX_ELEMENTS, cmd)
    assert elements != None, "Syntaxe invalide, aucun élément n'est présent"

    nombre_fois = cmd[:elements.start()-2]
    assert nombre_fois.isdigit(), "Syntaxe invalide, le nombre d'éléments choisis est inférieur à 1"
    nombre_fois = int(nombre_fois)

    elements = re.split(REGEX_SEPARATORS, elements.group())


    assert nombre_fois >= 1, "commande invalide, le nombre d'élément choisis est invalide"
    assert bool(elements) == True, "commande invalide, aucun élément n'est présent"

    return elements, nombre_fois

def exec_l(cmd:str) -> list[str]:
    elements, nombre_fois = trouver_elements_et_n_fois(cmd)
        
    return [choice(elements) for i in range(nombre_fois)]

def exec_u(cmd:str) -> list[str]:
    elements, nombre_fois = trouver_elements_et_n_fois(cmd)

    assert nombre_fois <= len(elements), "commande invalide, le nombre d'éléments choisis est supérieur au nombre de choix possible"
    
    choix = []
    for i in range(nombre_fois):
        index = randint(0, len(elements)-1)
        choix.append(elements[index])
        del elements[index]

    return choix