
Pour lancer le serveur, exectuer webdemineur.py

Pour jouer, ouvrir l'adresse ip et le port indiqués avec un navigateur ( http://127.0.0.1:8000 )




CHOSES A FAIRE RESTANTES 

- modifier les images du drapeau et des bombes pour qu'elles soient transparentes ( on peut le faire par CSS ou en modifiant l'image de base)

- pour faire les fonctions gagner/perdu :
    > faire une fonction qui dévoile la grille entièrement (on va la dévoiler dans tous les cas)
    > faire une feuille de style qui affiche un bouton rejouer, qui affiche un message gagné/perdu, et qui change la couleur du fond en fonction de si on a gagné ou perdu
    > modifier la fonction "traite action" pour que si ETAT_PARTIE == perdu ou == gagné, ça lance la feuille de style

- creuse renvoie l'état de la partie directement, mais drapeau a besoin d'appeler test_victoire qui n'est pas encore codée ( algos_jeu ligne 208 )

- modifier la feuille de style pour faire un site plus joli 
