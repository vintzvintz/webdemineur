


# chemins des actions et des fichiers statiques pour construire les liens HTML
ACTION_INTRO = "intro"
ACTION_NOUVELLE_PARTIE = "start_game"
ACTION_CREUSE = "creuse"
ACTION_FLAG = "flag"



############  Données de la partie en cours ###############


# tableau de jeu
PARTIE_TAB = "tab_jeu"

# type de difficulté des parties
PARTIE_MODE = "mode"
PARTIE_MODE_FACILE = "facile"
PARTIE_MODE_NORMAL = "normal"
PARTIE_MODE_HARCORE = "hardcore"


# etat de la partie
PARTIE_ETAT = "partie"
PARTIE_ETAT_INTIAL = "pas commencé"
PARTIE_ETAT_EN_COURS = "en cours"
PARTIE_ETAT_PERDU = "perdu"
PARTIE_ETAT_GAGNE = "gagne"



################# Actions de jeu appelée depuis l'interface web ############

LISTE_ACTIONS = [
    ACTION_INTRO,
    ACTION_NOUVELLE_PARTIE,
    ACTION_CREUSE,
    ACTION_FLAG ]


CHEMIN_RESSOURCES = "/fichiers"


COORD_X = "x"
COORD_Y = "y"

