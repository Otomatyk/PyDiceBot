"""
Coeur de DiceIO, définit les fonctions 'exec_cmd' et 'exec_commande'.
"""

import sys
from functools import lru_cache, partial
from random import choices, randint, seed, shuffle
from re import search, split, match
from time import time

from diceio_choice import exec_l, exec_u
from diceio_macro import exec_cmd_macro


LancerDes = list[int]
Condition = str #">" | "<" | "!=" | "=="
Somme = int

MAX_MESSAGE_LEN: int = 2000
IGNORED_COMMANDS: frozenset = frozenset(("!levels", "!rank"))

sr_users: set = set()
last_sr_dices: dict = {}

def relancer_last_sr(user_id: int) -> str:
    n_des = last_sr_dices.get(user_id)
    if n_des == 0:
        return '# Aucune dès à relancer !'
    return f"# {n_des} dès rélancés \n"+exec_lancer_des_sr(str(n_des), user_id)

def exec_lancer_des_sr(cmd: str, user_id: int) -> str | tuple[Somme, LancerDes]:
    "Recoie la commande nettoyée et renvoie le message à afficher ou le resultat des dès"

    if cmd.isdigit():
        n_des = int(cmd)
    
    elif match("[0-9]+(?=d6$)", cmd):
        n_des = int(search("[0-9]+(?=d)", cmd).group())

    else:
        return exec_lancer_des(cmd)

    result = choices(get_dice_range(6), k=n_des)

    n_6 = result.count(6)
    n_succes = result.count(5) + n_6
    n_1 = result.count(1)

    last_sr_dices[user_id] = n_des-n_succes

    return f'Nombre de succes: {n_succes}\
        \nNombre de 6 : {n_6}\
        \nNombre de 1 : {n_1}'

def exec_lancer_des(cmd: str) -> tuple[Somme, LancerDes]:
    "Recoie la commande nettoyée"
    cmd = "+"+cmd #Le premier token rajoute forcement sa somme

    # D'abbord diviser les tokens et trouver l'ordes des opérateurs
    liste_token = split("(\+|(?<!k)\-)", cmd)[1:]

    # Puis les éxécuter
    lancer_des = []
    somme_final = 0

    for op_arithmeique, token in zip(liste_token[::2], liste_token[1::2]):

        assert bool(token), "Token manquant, trop d'opérateurs arithmétiques"

        if token.isdigit():
            somme = int(token)
            lancer_des.append(f"_{somme}")
        else:
            somme, lance = exec_token(token)
            lancer_des.extend(lance)

        somme_final += somme if op_arithmeique == "+" else -somme

    return somme_final, lancer_des

def exec_token(token: str) -> tuple[Somme, LancerDes]:
    """Execute un token (les tokens sont séparés de + et de - dans les lancer de dès)

    Args:
        token (str): le token a analyser et executer

    Returns:
       tuple[int, list[int]]: La somme du résultat et le lancé de dès
    """

    n_des = search("([0-9]+)(?=(d|e))", token)
    n_des = int(n_des.group()) if n_des else 1

    n_face = search("(?<=(d|e))[0-9]+", token)
    assert n_face is not None, "Syntaxe invalide, ll manque le nombre de faces"
    n_face = int(n_face.group())

    lancer_des = choices(range(1, n_face), k=n_des)

    #Explode
    if "e" in token:
        assert n_face > 1, "Utiliser Explode néssecite que le nombre de face soit supérieur à 1"
        for _ in lancer_des:
            while lancer_des[-1] == n_face:
                lancer_des.append( randint(1, n_face) )

    #Keep
    if "k" in token:
        if keep := search("(?<=k)(|\-)[0-9]+", token):
            keep = int(keep.group())
            assert abs(keep) != 0, "Utiliser Keep néssecite que le nombre de dès à garder soit non-nulle"
            lancer_des = appliquer_keep(lancer_des, keep)
        else:
            raise AssertionError("Il manque le nombre de dès de garder avec le keep")

    #Map
    if "(" in token:
        if map_ := search("(g|r|a|b)\(.[0-9]+(?=\))", token):
            map_ = map_.group()
            lancer_des = appliquer_map(lancer_des, map_[0], map_[2], int(map_[3:]), n_face+1)

    #Sort
    if "s" in token:
        lancer_des = sorted(lancer_des)

    return sum(lancer_des), lancer_des

def appliquer_keep(lancer_des: LancerDes, keep: int) -> LancerDes:
    """Garde les meilleurs (+) ou les pires résultats (-) d'un lancé de dès, mélange le lancé après

    Args:
        LancerDes (list[int]): Le lancé de dès
        keep (signed int): Les dès à garder. Avec un nombre négatif, garde les pires résultats

    Returns:
        list[int]: Le lancé de dès après keep
    """

    if len(lancer_des) < abs(keep):
        raise AssertionError("Erreur : Le nombre de dès à garder est supérieur au nombre de dès")

    lancer_des_trier = sorted(lancer_des, reverse=keep > 0)

    lancer_des = lancer_des_trier[0:abs(keep)]
    shuffle(lancer_des)
    return lancer_des

def _eval_condition(des: int, condition: Condition, n_condition: int) -> bool:
    """Test si un dès respècte une condition

    Args:
        des (int): Le dès à tester
        condition (Condition): La condition (>, <, ==, !=...ect)
        n_condition (int): Le nombre à droite de l'opération

    Returns:
        bool: Le résultat du test
    """

    match condition:
        case "=":
            return des == n_condition
        case "!":
            return des != n_condition
        case "<":
            return des < n_condition
        case ">":
            return des > n_condition

    raise ValueError("Valeur invalide pour 'condition'")

def relancer(des: int ,condition: Condition, n_condition: int, n_face: int) -> int:
    """Relance le dès si la condition est vraie

    Args:
        des (int): _description_
        condition (Condition): La condition (>, <, ==, !=...ect)
        n_condition (int): Le nombre à droite du test
        n_face (int): Le nombre de face du dès

    Returns:
        int: Le nouveau dès (ou l'ancien!)
    """

    if _eval_condition(des, condition, n_condition):
        return randint(1,n_face-1)
    return des

def rajouter(lancer_des: LancerDes, condition: Condition, n_condition: int, n_face: int):
    """Rajoute un seul nouveau dès pour chaque dès respectant la condition"""

    def rajouter_si(des):
        if _eval_condition(des, condition, n_condition):
            lancer_des.append(randint(1,n_face))
        return des

    return map(rajouter_si, lancer_des)

def appliquer_map(lancer_des:LancerDes, action_map:str,
                  condition_map:Condition, n_condition_map:int, n_face:int):
    """Applique Map sur un lancé de dès """
    fn_condition = partial(_eval_condition, condition=condition_map, n_condition=n_condition_map)

    match action_map:
        case "r":
            lancer_des = map(
                lambda des: relancer(des, condition_map, n_condition_map, n_face),
                lancer_des)

        case "g":
            lancer_des = filter(fn_condition, lancer_des)

        case "a":
            return rajouter(lancer_des, condition_map, n_condition_map, n_face)

        case "b":
            lancer_des = map(fn_condition, lancer_des)

    return list(lancer_des)

def exec_commande(cmd: int, user_id: int=1) -> str:
    "Prend en entré la commande (avec le point d'exclamation), l'execute, et renvoie le message à afficher"
    seed(time())

    if cmd in IGNORED_COMMANDS:
        return ""

    cmd: str = cmd[1:]

    try:
        if "u" in cmd:
            result_message = exec_u(cmd)

        elif "l" in cmd:
            result_message = exec_l(cmd)

        elif cmd == "h":
            result_message = relancer_last_sr(user_id)

        elif cmd == "sr":
            if user_id in sr_users:
                sr_users.remove(user_id)
                result_message = "!SR Désactivé."
            else:
                sr_users.add(user_id)
                result_message = "!SR Activé."
            
        elif cmd.startswith("!"):
            result = exec_cmd_macro(cmd, user_id)

            if type(result) is tuple:
                print("Resultat : ", result[0])
                somme, des = exec_lancer_des(result[0])
                result_message = f'# {somme}\n{cmd} {des}'
            else:
                result_message = result

        elif cmd == "help":
            result_message = "Documentation : https://github.com/Otomatyk/Dice-IO"

        else:
            cmd = cmd.lower()
            cmd = cmd.replace(" ", "" )

            if user_id in sr_users:
                result_message = exec_lancer_des_sr(cmd, user_id)

                if type(result_message) is tuple:
                    somme, des = result_message
                    result_message = f'# {somme}\n{cmd} {des}'
                elif type(result_message) is str:
                    result_message = "# "+result_message
                else:
                    raise ValueError("Erreur fatale, type incorrecte pour le !sr")
            else:
                somme, des = exec_lancer_des(cmd)
                result_message = f'# {somme}\n{cmd} {des}'

    except AssertionError as erreur:
        result_message = 'Erreur : ' + erreur.args[0]

    except EOFError as erreur:
        match erreur.args[0]:
            case "'NoneType' object has no attribute 'group'":
                result_message = \
                  "Erreur indéterminée, possibles causes : \n\tLes divisions et multiplications ne sont pas prises en comptes"

            case _:
                result_message = 'Erreur indéterminée, cause : '+ erreur.args[0]

    except Exception as erreur:
        result_message = 'Erreur indéterminée, cause : '+ erreur.args[0]

    if len(result_message) >= MAX_MESSAGE_LEN:
        result_message = "Message trop long"

    return f'```md\n{result_message}```'

if __name__ == "__main__":
    print("-*-*- DICE ENGINE -*-*-")

    last_cmd: str = ""
    QUIT_COMMAND = {"!quit", "!exit", "!quitter"}

    while True:
        INPUT_CMD = "!"+input("$ ")

        if INPUT_CMD in QUIT_COMMAND:
            break

        if INPUT_CMD == "!":
            INPUT_CMD = last_cmd
            print(INPUT_CMD)

        # Supprime le '''md\n'''
        print( exec_commande(INPUT_CMD)[6:-3] )

        last_cmd = INPUT_CMD

    sys.exit()
