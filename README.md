# Documentation de Dice Engine

## Les bases

Voici la syntaxe pour un lancé de dès basique :
```! NOMBRE_DE_DES d NOMBRES_FACES```

Par exemple, lancer huit dès de quatre faces chacun, il faut faire :
```!8d4```

Il est possible d'ommetre le nombre de dès, dans ce cas là, un seul dés sera lancer :
```!d6``` 
Cette commande lancera un seul dè à six face

## Addition et soustraction

Il est aussi possible d'additioner/soustraire des lancés de dès (Ou des constantes) entre eux, il suffit d'utiliser le signe + et -, la somme sera afficher au début du résultat
```!d6+2d10-8``` Lancera d'abbod un dè de six, additionerra son résultat à la somme de deux dès de dix, puis vas soustraire le résultat de huit.

Le résultat de chaque dès sera quand même afficher.

## Garder les meilleurs/pires résultats

Pour garder les meilleurs/pires résultats d'un lancer de dès, il faut utiliser les opérateurs **K**eep et **K**eep **L**ower, tout ce passe comme si seuls ces dès ont était lancés, il s'ajoutent après le nombre de faces :
```!100d100k2```  gardera les deux meilleurs résultats parmis cent dès de cent
```!100d100kl2```  gardera les deux résultats les plus bas parmis cent dès de cent

## Relancer si le dès a atteint son max

Si vous avez besoins de relancer tout les dès qui ont faire leur résultat maximal, c'est possible, pour ce faire replacer le **d** par un **e**. Comme :
```!15e6``` 

## Majuscules et espaces

Avant d'éxecuter la commande, toutes les lettres seront mises en minuscules, et les espaces seront supprimés. Ne vous souciez pas de ça.
