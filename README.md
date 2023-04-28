# Documentation de Dice Engine

## L'intérpréteur

Si vous lancer dice_engine_core.py vous allez vous retrouver devant une ligne de commande commencant par un $, vous pouvez essayer n'importe quelle commande à condition de ne pas mettre le point d'exclamation (il faut le mettre seulement si vous lancez la commande depuis discord)

## Les bases

Voici la syntaxe pour un lancé de dès basique :
```! NOMBRE_DE_DES d NOMBRES_FACES```

Par exemple, pour lancer huit dès de quatre faces chacun, il faut faire :
```!8d4```

Il est possible d'ommetre le nombre de dès, dans ce cas là, un seul dés sera lancer :
```!d6``` 
Cette commande lancera un seul dè à six face.

## Addition et soustraction

Il est aussi possible d'additioner/soustraire des lancés de dès (Ou des constantes) entre eux, il suffit d'utiliser le signe + et -, la somme sera afficher au début du résultat.

```!d6+2d10-8``` Lancera d'abbod un dè de six, additionerra son résultat à la somme de deux dès de dix, puis vas soustraire le résultat de huit.

Le résultat de chaque dès sera quand même afficher mais les constantes commenceront avec un souligné du bas.

## Garder les meilleurs/pires résultats

Pour garder les meilleurs résultats d'un lancer de dès, il faut utiliser l'opérateur **K**eep, tout ce passe comme si seuls ces dès ont était lancés, il s'ajoutent après le nombre de faces :
```!100d100k2```  gardera les deux meilleurs résultats parmis cent dès de cent.

Pour garder les pires résultats d'un lancé de dès il faut utiliser des nombres négatifs :
```!100d100k-2```  gardera les deux résultats les plus bas parmis cent dès de cent.

## Relancer si les dès qui ont atteint leur max

Si vous avez besoins de relancer tout les dès qui ont faire leur résultat maximal, c'est possible, pour ce faire replacer le **d** par un **e**. Comme :
```!15e6``` 

Il est impossible de lancer un dès Explode à une seule face.

## Majuscules et espaces

Avant d'éxecuter la commande, toutes les lettres seront mises en minuscules et les espaces seront supprimés. Ne vous souciez pas de ça.

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
```!3L gauche,droite,10,20,40,100``` Retournera trois élements parmis la liste donnée.

Avec L un même élément peut être choisis plusieurs fois, mais ce n'est pas le cas avec U :
```!2u Je ne peux être choisis qu'une seule fois,Moi aussi,De même```

Si vous voulez que peut importe le tirage un message soit afficher, vous pouvez le mettre après une diése à la fin du message :

```!1l oui,non #Devrais-je aller à gauche ?``` 
Cette commande retournera :
```
# Devrais-je aller à gauche ?
Oui/Non
```

### Variantes de U et L

Il est aussi possible de remplacer les virgules par des points-virgules, ou de mixer les deux !
```!1l Virgule,Point-Virgule;Troisième élément``` 

Ou de mettre des paranthèses/crochets à la places des espaces.
```!1l(Fusion;De tout,Ce qui,Est Possible]``` 

## Appliquer une opération sur chaque dès

### Condition

Pour comprendre le reste du chapitre il faut savoir comment écrire des conditions :
```>6``` Est True si le dé est supérieur à 6
```<6``` Est True si le dé est inférieur à 6
```!6``` Est True si le dé est different de 6
```=6``` Est True si le dé est égal à 6

### (B)ooléan, est ce que ce dè respecte cette condition ?

Avec **B**ooléean on peux savoir quels sont les dès qui respectent la condition choisit :
```!15d6b(>4)```
Cette commande renvoira une liste de True et de False, selon si le dès est supérieur ou inférieur à 4.

La somme sera égale au  nombre de dès respéctant la condition.

### (R)elancer, relance le dès si la condition est respéctée

Si la condition est respéctée, le dè sera relancer est son nouveau résultat ajouté à la somme (L'ancien résultat sera ignoré) :
```!15d6r(=1)```

### (G)arder, le filtre

Seulements les dès respéctant la condition seront gardés dans le résultat final :
```!100d500g(<128)``` Enlévra tous les dès supérieur ou égal à 128.

### Relancer et (A)jouter, le cousin de explode

Comme le **R**elancer, mais agis comme si le dè relancer en est un nouveau :
```!3d8a(=8)``` Est équivalent à ```!3e8```

### Keep et G,R,A,B

Quand on utilise un Keep et un des GRAB dans le même lancé il faut faire attention à l'ordre !
Par exemple :
```!10d100g(<50)k1``` Aura comme résultat le plus grand dè inférieur à 50, tandis que
```!10d100k1g(<50)``` Aura comme résultat le meilleur dé (s'il est inférieur à 50, sinon il n'y aura aucun dès gardés).

## Les macros

Si vous en avez marre de taper régulierment la même commande complexe, vous devrez utiliser une macro !
Pour en rajouter une il faut faire (Le nom ne peut contenir que des caractères alphanumériques et des underscores) :
```!!add NOM_DE_LA_MACRO LANCER_MACRO ```
(Mettez qu'un seul point d'exclamation si vous êtes sur l'interpréteur)

Pour l'éxécuter :
```!!NOM_DE_LA_MACRO```

Pour en supprimer :
```!! del NOM_DE_LA_MACRO```

Et pour obtenir la liste des macros enregistrées :
```!!get```

Par exemple (Le nom choisit est plutôt long pour que ce soit comprenhsible) :
```!!add dm_attaque 4d8k3+7```
```!!dm_attaque```
```!!del dm_attaque```

### Macros avec parmaètre

Il est possible de créer des macros avec un paramètre d'entré (comme une fonction mathématique), le résultat dépendra de ce paramètre.
Pour en créer une, il faut faire comme pour une macro basique, mais en mettant un dollar $ là où le paramètre va, exemple :
`!!add 3_des 3d$`. 
Pour l'éxecuter il faut rajouter la paramètre après le nom de la macro : `!!3_des 5` sera equivalent à `!3d5`.
Si aucune paramètre n'est fournit, les $ seront remplacer par 0

---
NOTE : Pour eviter de surcharger la RAM du serveur, il y a une limite de 10 Macro / Utilisateur, pour la modifier, changer la valeur de MAX_MACRO_PER_USER dans dice_engine_macro.py

# FAQ

## J'ai l'erreur "Message trop long", que faire ?

Dice Engine a était conçu pour un bot discord, si le message est plus long que 2.000 Char (La limite de discord), ce message d'erreur s'affiche, pour régler ce problème il faut changer la constante MAX_MESSAGE_LEN dans dice_engine_core.py

## C'est quoi !sr ?

C'est une fonctionalité en cours de création, qui permet à chaque utilisateur discord de faire !sr pour simplifier l'affichage des lancés de dès pour le Jeux De Rôle Shadworun.
