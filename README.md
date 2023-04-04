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

Pour garder les meilleurs résultats d'un lancer de dès, il faut utiliser l'opérateur **K**eep, tout ce passe comme si seuls ces dès ont était lancés, il s'ajoutent après le nombre de faces :
```!100d100k2```  gardera les deux meilleurs résultats parmis cent dès de cent

Pour garder les pires résultats d'un lancé de dès il faut utiliser des nombres négatifs :
```!100d100k-2```  gardera les deux résultats les plus bas parmis cent dès de cent

## Relancer si le dès a atteint son max

Si vous avez besoins de relancer tout les dès qui ont faire leur résultat maximal, c'est possible, pour ce faire replacer le **d** par un **e**. Comme :
```!15e6``` 

Il est impossible de lancer un dès Explode à une seule face

## Majuscules et espaces

Avant d'éxecuter la commande, toutes les lettres seront mises en minuscules, et les espaces seront supprimés. Ne vous souciez pas de ça.

## Trier les résultats

Si vous voulez trier les résultats de vos lancés de dès, utilisez l'opérateur **S**ort, il se place à peu près n'importe où :
```!s10d6```
```!8d99s```
```!14d8k10s```
```!14d8sk10```

## Piocher dans une liste

Il existe deux commandes qui ne lancent pas de dès, mais qui permmettent de choisir au hasard des/un élement(s). Commençon par L, sa syntaxe est la suivante :
```! NOMBRE_D'ELEMENT_A_CHOISIR l ELEMENT1,ELEMENT2,ELEMENT3``` 
par exemple :
```!3L gauche,droite,10,20,40,100```

Avec L un même élément peut être choisis plusieurs fois, mais ce n'est pas le cas avec U :
```!2u Je ne peux être choisis qu'une seule fois,Moi aussi,De même```

#Variantes de U et L

Il est aussi possible de remplacer les virgules par des points-virgules, ou de mixer les deux !
```!1l Virgule,Point-Virgule;Troisième élément``` 

Ou de mettre des paranthèses/crochets
```!1l(Fusion;De tout,Ce qui,Est Possible]``` 
