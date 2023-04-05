import re

"""
!!add initiative d6+13
!!del initative
!!get
!!initative
"""

RE_NOM_MACRO = re.compile("(?<=(add|del)\W)[a-zA-Z0-9_]+")
RE_JET_MACRO = re.compile("(?<=[a-zA-Z0-9_])\W*.+")

MAX_MACRO_PER_USER =10

dict_macro = {}
nombre_macro_par_user = {}

def add_macro(cmd, user_id):
    if user_id in nombre_macro_par_user:
        nombre_macro_par_user[user_id] += 1
    else:
        nombre_macro_par_user[user_id] = 1

    assert nombre_macro_par_user[user_id] <= MAX_MACRO_PER_USER, "Le nombre de macro ne peut pas dépasser {0} par utilisateurs".format(MAX_MACRO_PER_USER)

    nom_macro = re.search(RE_NOM_MACRO, cmd).group()
    jet_des_macro = re.search(RE_JET_MACRO, cmd).group()

    dict_macro[str(user_id)+nom_macro] = jet_des_macro

    return "La macro {0} a bien était rajouter".format(nom_macro)

def del_macro(cmd, user_id):
    nom_macro = re.search(RE_NOM_MACRO, cmd).group()
    id_macro = str(user_id)+nom_macro

    assert id_macro in dict_macro, "La macro n'a pas était enregistrée"

    del dict_macro[id_macro]

    return "La macro {0} a bien était supprimer".format(nom_macro)

def get_macro(nom_macro, user_id):
    id_macro = str(user_id)+nom_macro

    assert id_macro in dict_macro, "La macro n'a pas était enregistrée"

    return dict_macro[id_macro]

def get_liste_macro():
    liste_macro_str = "Liste des macros :"
    for macro_key in dict_macro:
        liste_macro_str += f"\t\nNom de la macro : {dict_macro[macro_key][3:]}"
    return liste_macro_str


def exec_cmd_macro(cmd, user_id):
    "Prend en entré la commande sans le point d'exclamation, renvoie le message a afficher, et s'il y a une macro a executer, renvoie une tuple (cmd,None)"
    match cmd[1:4]:
        case "get":
            return get_liste_macro()
        case "add":
            return add_macro(cmd, user_id)
        case "del":
            return del_macro(cmd, user_id)
        case _:
            nom_macro = cmd[1:].replace(" ", "")
            return (get_macro(nom_macro, user_id),)