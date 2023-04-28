import re
from random import randint, choices, shuffle
from re import search, split, match
from dice_engine_l_et_u import exec_l, exec_u
from dice_engine_macro import exec_cmd_macro

RE_FORMAT_TOKEN_VALIDE = re.compile("[0-9]*(d|e)[0-9]+.*")
RE_N_DES = re.compile("([0-9]+)(?=(d|e))")
RE_N_FACE = re.compile("(?<=(d|e))[0-9]+")

RE_KEEP = re.compile("(?<=k)(|\-)[0-9]+")

RE_MAP = re.compile("(g|r|a|b)\(.[0-9]+(?=\))")

RE_OPS = re.compile("(?<!k)[\+\-]")
RE_SPLIT_TOKEN = re.compile("(\+|(?<!k)\-)")

RE_FORMAT_U = re.compile("[0-9]+u.+")
RE_FORMAT_L = re.compile("[0-9]+l.+")

MAX_MESSAGE_LEN = 2000

Lancer_des = list[int]
Condition = str #">" | "<" | ">=" | "<=" | "!=" | "=="

def exec_lancer_des(cmd:str) -> tuple[int, Lancer_des]: 
    "Recoie la commande nettoyée"
    cmd = "+"+cmd #Le premier lancé de dès rajouter forcement sa somme

    #D'abbord diviser les tokens et trouver l'ordes des opérateurs
    liste_token = split(RE_SPLIT_TOKEN, cmd)[1:]

    #Puis les éxécuter
    lancer_des = []
    somme_final = 0

    for op, token in zip(liste_token[::2], liste_token[1::2]):
        
        assert bool(token), "Token manquant, trop d'opérateurs arithmétiques"
        
        if token.isdigit():
            somme = int(token)
            lancer_des.append(f"_{somme}")
        else:
            somme, lance = exec_token(token)
            lancer_des.extend(lance)
        
        somme_final = somme_final+somme if op == "+" else somme_final-somme
        
    return somme_final, lancer_des

def exec_token(token:str) -> tuple[int, Lancer_des]:
    """Execute un token (les tokens sont séparés de + et de - dans les lancer de dès)

    Args:
        token (str): le token a analyser et executer

    Returns:
       tuple[int, list[int]]: La somme du résultat et le lancé de dès
    """
    n_des = search(RE_N_DES, token)
    n_des = int(n_des.group()) if n_des else 1

    n_face = search(RE_N_FACE, token)
    assert hasattr(n_face, "group"), "Syntaxe invalide, ll manque le nombre de faces"
    n_face = int(n_face.group())

    lancer_des = choices(range(1, n_face+1), k=n_des)

    #Explode
    if "e" in token:
        assert n_face > 1, "Utiliser Explode néssecite que le nombre de face soit supérieur à 1"
        for _ in lancer_des:
            while lancer_des[-1] == n_face:
                lancer_des.append( randint(1, n_face) )

    #Keep
    if "k" in token:
        keep = search(RE_KEEP, token)
        if keep:
            keep = int(keep.group())
            lancer_des = appliquer_keep(lancer_des, keep)

    #Map
    if "(" in token:
        map_ = search(RE_MAP, token)
        if map_:  
            map_ = map_.group()
            lancer_des = appliquer_map(lancer_des, map_[0], map_[2], int(map_[3:]), n_face+1)

    #Sort
    if "s" in token:
        lancer_des = sorted(lancer_des)

    return sum(lancer_des), lancer_des

def appliquer_keep(lancer_des:Lancer_des, keep:int) -> Lancer_des:
    """Garde les meilleurs (+) ou les pires résultats (-) d'un lancé de dès, mélange le lancé après

    Args:
        lancer_des (list[int]): Le lancé de dès
        keep (signed int): Les dès à garder. Avec un nombre négatif, garde les pires résultats

    Returns:
        list[int]: Le lancé de dès après keep
    """
    if keep > 0:
        lancer_des_trier = sorted(lancer_des, reverse=True)
    else:
        lancer_des_trier = sorted(lancer_des)

    lancer_des = lancer_des_trier[0:abs(keep)]
    shuffle(lancer_des)
    return lancer_des

def eval_condition_map(des:int, condition:Condition, n_condition:int) -> bool:
    """Test si un dès respècte une condition

    Args:
        des (int): Le dès à tester
        condition (Condition): La condition (>, <, ==, !=...ect)
        n_condition (int): Le nombre à droite de l'opération

    Returns:
        bool: Le résultat du test
    """
    return eval(str(des) +condition+ str(n_condition) )
                
def relancer(des:int ,condition:Condition, n_condition:int, n_face:int) -> int:
    """Relance le dès si la condition est vraie

    Args:
        des (int): _description_
        condition (Condition): La condition (>, <, ==, !=...ect)
        n_condition (int): Le nombre à droite du test
        n_face (int): Le nombre de face du dès

    Returns:
        int: Le nouveau dès (ou l'ancien!)
    """

    if eval_condition_map(des, condition, n_condition):
        return randint(1,n_face-1)
    else:
        return des

def rajouter(lancer_des:Lancer_des, condition:Condition, n_condition:int, n_face:int):

    def rajouter_si(des):
        if eval_condition_map(des, condition, n_condition):
            lancer_des.append(randint(1,n_face))
        return des
    
    return map(rajouter_si, lancer_des)
    
def appliquer_map(lancer_des:Lancer_des, action_map:str, condition_map:Condition, n_condition_map:int, n_face:int):
    fn_condition = lambda des:eval_condition_map(des, condition_map, n_condition_map)

    match condition_map:
        case "!":
            condition_map = "!="
        case "=":
            condition_map = "=="
    
    match action_map:
        case "r":
            fn_condition = lambda des: relancer(des, condition_map, n_condition_map, n_face)

            lancer_des = map(fn_condition, lancer_des)

        case "g":
            lancer_des = filter(fn_condition, lancer_des)
            
        case "a":
            return rajouter(lancer_des, condition_map, n_condition_map, n_face)

        case "b":
            lancer_des = map(fn_condition, lancer_des)

    return list(lancer_des)

def exec_commande(cmd:int, user_id=1):
    "Prend en entré la commande (avec le point d'exclamation), et renvoie le message à afficher"
    if cmd in ("!rank", "!levels"):
        return ""
    
    cmd = cmd[1:]

    try:
        if match(RE_FORMAT_U, cmd):
            result = exec_u(cmd)

        elif match(RE_FORMAT_L, cmd):
            result = exec_l(cmd)
        
        elif cmd[0] == "!":
            result = exec_cmd_macro(cmd, user_id)
            if type(result) == tuple:
                print("Resultat : ", result[0])
                somme, des = exec_lancer_des(result[0])
                result = f'# {somme}\n{cmd} {des}'
        else:
            cmd = cmd.lower()
            cmd = cmd.replace(" ", "" )

            somme, des = exec_lancer_des(cmd)
            result = f'# {somme}\n{cmd} {des}'

    except AssertionError as erreur:
        result = 'Erreur : ' + erreur.args[0]

    except EOFError as erreur:
        match erreur.args[0]:
            case "'NoneType' object has no attribute 'group'":
                result = "Erreur indéterminée, possibles causes : \n\tLes divisions et multiplications ne sont pas prises en comptes"
            
            case _:
                result = 'Erreur indéterminée, cause : '+ erreur.args[0]
    except Exception as erreur:
        result = 'Erreur indéterminée, cause : '+ erreur.args[0]
   
    finally:
        if len(result) >= MAX_MESSAGE_LEN:
            return '```md\nMessage trop long```'
        else:
            return f'```md\n{result}```'

if __name__ == "__main__":
    cmd = 1
    print("-*-*- DICE ENGINE -*-*-")
    while cmd not in ("quit", "exit", "bye", "quitter"):
        cmd = input("$ ")
        print( exec_commande("!"+cmd) )
