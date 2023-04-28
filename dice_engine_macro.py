import re

"""
!!add initiative d6+13
!!del initative
!!get
!!initative

# Macro avec parametre :
!!add initiative d6+13-$
!!initative 5 #Egale a 'd6+13-5'
"""

RE_NOM_MACRO = re.compile("(?<=(add|del|arg)\s)[a-zA-Z0-9_]+")
RE_NOM_MACRO_GET = re.compile("(?<=!)[0-9a-zA-Z_]+(?=(\s*|$))")
RE_JET_MACRO = re.compile("(?<=[a-zA-Z0-9_])\s+[0-9de+-grab()lu,;\[\]=!><\$]+")
RE_ARG_MACRO = re.compile("(?<=\s)[0-9]+([\s]*|$)")

MAX_MACRO_PER_USER = 10

dict_macro = {}
nombre_macro_par_user = {}

def add_macro(cmd:str, user_id:int) -> str:
    if user_id in nombre_macro_par_user:
        nombre_macro_par_user[user_id] += 1
    else:
        nombre_macro_par_user[user_id] = 1

    assert nombre_macro_par_user[user_id] <= MAX_MACRO_PER_USER, f"Le nombre de macro ne peut pas dépasser {MAX_MACRO_PER_USER} par utilisateurs"

    nom_macro = re.search(RE_NOM_MACRO, cmd).group()
    jet_des_macro = re.search(RE_JET_MACRO, cmd).group()
    jet_des_macro = "!" + (jet_des_macro[1:] if jet_des_macro.startswith(" ") else jet_des_macro)

    dict_macro[str(user_id)+nom_macro] = jet_des_macro

    return "La macro '{0}' a bien était rajouter".format(nom_macro)

def del_macro(cmd:str, user_id:int) -> str:
    nom_macro = re.search(RE_NOM_MACRO, cmd).group()
    id_macro = str(user_id)+nom_macro

    assert id_macro in dict_macro, "La macro n'a pas était enregistrée"

    del dict_macro[id_macro]

    return "La macro '{0}' a bien était supprimer".format(nom_macro)

def get_macro(cmd:str, user_id:int) -> str:
    nom_macro = re.search(RE_NOM_MACRO_GET, cmd).group()
    id_macro = str(user_id)+nom_macro

    assert id_macro in dict_macro, f"La macro '{nom_macro}' n'a pas était enregistrée"
    
    macro = dict_macro[id_macro]

    if "$" in macro:
        arg = re.search(RE_ARG_MACRO, cmd)
        if arg is not None:
            arg = arg.group()
            assert arg.isdigit(), "Le paramètre d'entré doit être un nombre entier !"
        else:
            arg = "0"
        macro = macro.replace("$", arg)
    
    return (macro,None)

def get_liste_macro() -> str:
    liste_macro_str = "Liste des macros :"

    for nom, cmd in zip(dict_macro.keys(), dict_macro.values()):
        liste_macro_str += f"\t\n'{nom}' : '{cmd}'"
    return liste_macro_str


def exec_cmd_macro(cmd:str, user_id:int):
    "Prend en entré la commande sans le point d'exclamation, renvoie le message a afficher, et s'il y a une macro a executer, renvoie une tuple (cmd,None)"
    match cmd[1:4]:
        case "get":
            return get_liste_macro()
        case "add":
            return add_macro(cmd, user_id)
        case "del":
            return del_macro(cmd, user_id)
        case _:
            return get_macro(cmd, user_id,)
