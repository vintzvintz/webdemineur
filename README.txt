

Le projet est un serveur de démineur en  HTTP


****************************************************
*                   Utilisation                    *
****************************************************

Pour lancer le serveur, exectuer webdemineur.py
Pour jouer, ouvrir l'adresse ip et le port indiqués avec un navigateur ( http://127.0.0.1:8000 )

La page d'accueil propose de lancer une nouvelle partie 
Les niveaux de difficulté proposés font varier la taille de la grille et le nombre de bombes

Au départ, la grille de jeu s'affiche avec toutes les cases masquées.

Sur chaque case, il y a deux liens pour executer les deux actions classiques du démineur
C pour creuser
D pour poser ou retirer un drapeau

La partie est chronométrée
La partie est gagnée quand toutes les cases avec bombes ont un drapeau, et seulement elles
La partie est perdue si on creuse sur une bombre

A tout moment on peut :
* abandonner la partie, qui est alors considérée perdue, ce qui dévoile toutes les cases
* recommencer la partie

****************************************************
*             Description des fichiers             *
****************************************************

webdemineur.py
-------------

Fichier pricipal du projet et point d'entrée à exécuter

Il appelle le serveur HTTP intégré en standard avec Python
On s'est inspiré d'exemples trouvés sur internet, on a adapté le contenu de la fonction do_GET()

Les requetes sont analysées pour distinguer
 * les ressouces statiques ( fichiers images .png) 
    -> traitées par la bibliothèque standard Python depuis le répertoire /fichiers

 * les actions de jeu (creuse, drapeau, abandon, recommencer) e
    -> traitées par des fonctions dans algo_jeu.py

Certaines actions de jeu ont des paramètres ( ex: coordonnées de la case concernée ). 
Ces paramètres sont décodés afin d'être passés aux fonctions de traitement des actions.

Une variable globale 'partie' de type dictionnaire est créée dans ce fichier.
elle contient toutes les données de la partie en cours pour les conserver entre les requetes successives.
Elle est passée systématiquement aux fonctions de traitement des actions de jeu.
Cette variable étant unique pour le serveur, il n'est pas possible de gérer plusieurs parties simultanément.


algos_jeu.py
------------

 Ensemble des algorithmes du jeu 

 le point d'entrée principal est traite_action() 
 Il est appelé par le serveur HTTP pour chaque requete d'action de jeu reçue du joueur


 Pour chaque action
 - on exécute la fonction demandée ( creuse, drapeau, etc...)
 - on affiche diverses informations dans la console : requete reçue, état de la partie, grille de jeu ( )

La grille de jeu est un tableau à deux dimensions, les états possibles de chaque case sont définis par des constantes.


generateur_html.py
------------------

Fonctions qui génèrent du code html envoyé au joueur.

Il y a 3 types de pages
* intro : sélection de la difficulté et re-initialisation de la partie.
* erreur: affichage des messages d'erreurs (exemples : requetes invalides)
* partie_en cours : page principale du jeu incluant la grille de jeu, le chronometre, les liens pour abandonner/recommencer, etc..


Les styles CSS sont directement inclus dans la page html

commun.py
---------

Eléments partagés utilisés dans les autres fichiers

Définition des constantes 
fonctions utilitaires : tests, comptage des bombes.


