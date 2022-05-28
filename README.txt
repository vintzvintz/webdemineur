Le projet est un serveur de démineur en HTTP.


****************************************************
*                    Utilisation                   *
****************************************************

Pour lancer le serveur, exécuter webdemineur.py.
Pour jouer, ouvrir l'adresse ip et le port indiqués avec un navigateur (http://127.0.0.1:8000).

La page d'accueil propose de lancer une nouvelle partie.
Les niveaux de difficulté proposés font varier la taille de la grille et le nombre de bombes.

Au départ, la grille de jeu s'affiche avec toutes les cases masquées.

Sur chaque case, il y a deux liens pour exécuter les deux actions classiques du démineur :
	-> C pour creuser
	-> D pour poser ou retirer un drapeau

La partie est chronométrée, et est gagnée quand il y a exactement le même nombre de bombes et de drapeaux, et que chaque drapeau est placé sur une bombe.
La partie est perdue si l'on creuse sur une bombe.

A tout moment on peut :
	-> abandonner la partie, qui est alors considérée perdue, ce qui dévoile toutes les cases
	-> recommencer la partie

****************************************************
*             Description des fichiers             *
****************************************************

-------------------------------------------------------------
webdemineur.py
-------------------------------------------------------------

Fichier principal du projet et point d'entrée à exécuter.

Il appellé le serveur HTTP intégré avec Python.
On s'est inspiré d'exemples trouvés sur internet et on a adapté le contenu de la fonction do_GET().

Les requêtes sont analysées pour distinguer :
* les ressources statiques (fichiers images .png)
	-> traitées par la bibliothèque standard Python depuis le répertoire/fichiers

* les actions de jeu (creuse, drapeau, abandon, recommencer)
    -> traitées par des fonctions dans algo_jeu.py

Certaines actions de jeu ont des paramètres (ex: coordonnées de la case concernée).
Ces paramètres sont décodés afin d'être passés aux fonctions de traitement des actions.

Une variable globale 'partie' de type dictionnaire est créée dans ce fichier.
Elle contient toutes les données de la partie en cours pour les conserver entre les requêtes successives.
Elle est passée systématiquement aux fonctions de traitement des actions de jeu.
Cette variable étant unique pour le serveur, il n'est pas possible de gérer plusieurs parties simultanément.


-------------------------------------------------------------
algos_jeu.py
-------------------------------------------------------------

Ensemble des algorithmes du jeu.

Le point d'entrée principal est traite_action()
Il est appelé par le serveur HTTP pour chaque requête d'action de jeu reçue du joueur.

Pour chaque action :
- on exécute la fonction demandée ( creuse, drapeau, etc...)
- on affiche diverses informations dans la console : requête reçue, état de la partie, grille de jeu

La grille de jeu est un tableau à deux dimensions, les états possibles de chaque case sont définis par des constantes.


-------------------------------------------------------------
generateur_html.py
-------------------------------------------------------------

Fonctions qui génèrent du code HTML envoyé au joueur.

Il y a 3 types de pages :
* intro : sélection de la difficulté et réinitialisation de la partie.
* erreur: affichage des messages d'erreurs (exemples : requêtes invalides)
* partie_en cours : page principale du jeu incluant la grille de jeu, le chronomètre, les liens pour abandonner/recommencer, etc..

Les styles CSS sont directement inclus dans la page HTML.


-------------------------------------------------------------
commun.py
-------------------------------------------------------------

Eléments partagés utilisés dans les autres fichiers.

Définition des constantes.
Fonctions utilitaires : tests, comptage des bombes.


****************************************************
*                 Erreurs Pylint                   *
****************************************************

Il reste quelques erreurs Pylint que nous ne pouvons resoudre :
-> Variables indefinies : Pylint n'a pas les bibliotheques qu'on importe
-> Dans WebDemineur, l 19, Pylint signale que partie est une constante et doit etre inscrite en majuscule, mais partie est un dictionnaire qui se modifie à chaque requete, ce n'est donc pas une constante que nous devons pas nommer en majuscules.
-> Dans WebDemineur, l 76, Pylint indique qu'on peut remplacer le "or" par un "in", mais après vérification, ce changement produit un bug
-> Dans WebDemineur, l 97, donc dans la fonction do_get, Pylint renvoie l'erreur "Either all return statements in a function should return an expression, or none of them should", cependant nous ne parvenons pas à modifier cette fonction trouvée sur internet pour résoudre cette erreur.
-> Dans commun, Pylint dit qu'on ne doit pas utiliser plus de 4 constantes. Cependant, commun est la bibliothèque depuis laquelle nous importons toutes nos constante ; nous ne pouvons donc pas mettre moins de 4 constantes.
-> Dans generateur_html l 250 et 253, on a le même problème que dans WebDemineur l 76.