"""
Module pour tester les performances et la qualité des différentes version de DiceIO.
"""

from time import time


def benchmark(test_fn, n_execution:int=3000):
    """
    Test les perfs et la qualité de la fonction 'exec_commande' de diceio_core.py.
    Executera 'n_execution' fois chaque test.
    Les commandes qui n'ont pas eu le résultat attendu au premier test, ne sont éxécuter qu'une seule fois.
    """

    # Si la tuple contient True, la cmd doit retourner une erreur.
    test_strings = (
        ("10d6", False),
        ("d10", False),
        ("5g2", True),
        ("5d", True),
        ("d", True),

        ("4+8", False),
        ("7-8", False),
        ("3+", True),
        ("-100", True),

        ("10d10+9d9+8d8+7d7+6d6", False),

        ("6e3", False),
        ("3e1", True),

        ("25d10k8", False),
        ("25d10k-8", False),
        ("8d50k0", True),
        ("4d8k", True),
        ("20d6k100", True),

        ("12d4s", False),
        ("s12d4", False),
        ("12d4sk3", False),
        ("12d4k3s", False),

        ("1l 1,2,3", False),
        ("1l python;ruby,perl;java", False),
        ("1u salut,coucou,bonjour", False),
        ("1l 1,2,3 #Numero chance ;", False),
        ("1u salut,coucou,bonjour #PNJ dit ", False),
        ("2l a,b,c,", False),
        ("0l a,b,c", True),
        ("4u un,deux", True),
        ("10l", True),
        ("l gauche,droite", True),
        ("3 gauche,droite", True)
    )

    tests_passes:int = 0
    temps_debut:float = time()

    for cmd, returns_error in test_strings:
        cmd = "!"+cmd

        result = test_fn(cmd)
        returned_error = "Erreur" in result

        reussi = returned_error if returns_error==True else 1-returned_error
        tests_passes += reussi

        if not reussi:
            print("Test échoué :", cmd)
            print("Erreur déclenché ?", returned_error)
            print("Erreur attendu ?",returns_error)
            print("Message :", result, end="\n")
            continue
        
        for _ in range(n_execution):
            test_fn(cmd)
    
    temps_execution = (time() - temps_debut)*1000
    precision_pourcentage = round((tests_passes / len(test_strings)) * 100, 3)

    print("Temps d'execution :", temps_execution, "ms")
    print("Précision :", precision_pourcentage, "%")

if __name__ == "__main__":
    input("Appuyer sur Enter pour commencer le test sur 'diceio.core.py'\n")

    from diceio_core import exec_commande
    benchmark(exec_commande)
