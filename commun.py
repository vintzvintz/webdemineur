######################  Données de la partie en cours ###############

# tableau de jeu
PARTIE_TAB = "tab_jeu"

# heure de début de la partie - pour calculer le temps écoulé
PARTIE_HEURE_DEBUT = "heure_debut"

# type de difficulté des parties
PARTIE_MODE = "mode"
PARTIE_MODE_FACILE = "facile"
PARTIE_MODE_NORMAL = "normal"
PARTIE_MODE_HARDCORE = "hardcore"


# etat de la partie
PARTIE_ETAT = "etat_partie"
PARTIE_ETAT_INTIAL = "pas commencé"
PARTIE_ETAT_EN_COURS = "en cours"
PARTIE_ETAT_PERDU = "perdu"
PARTIE_ETAT_GAGNE = "gagne"


################# Actions de jeu appelée depuis l'interface web ############

ACTION_INTRO = "intro"
ACTION_NOUVELLE_PARTIE = "start_game"
ACTION_CREUSE = "creuse"
ACTION_FLAG = "flag"

LISTE_ACTIONS = [
    ACTION_INTRO,
    ACTION_NOUVELLE_PARTIE,
    ACTION_CREUSE,
    ACTION_FLAG ]


CHEMIN_RESSOURCES = "/fichiers"


COORD_X = "x"
COORD_Y = "y"


##########################################################

#  code déplacé ici pour éviter des erreurs d'import 
# fonctions utilisés à la fois dans algo_jeu.py et dans generateur_html.py


# Etats possibles pour chaque case du tableau de jeu
# les valeurs n'ont pas d'importance tant qu'elles sont différentes

VIDE_MASQUEE = 'vm'
VIDE_FLAG    = 'vf'
VIDE_DEVOILE = 'vd'
BOMB_MASQUEE = 'bm'
BOMB_FLAG    = 'bf'
BOMB_DEVOILE = 'bd'


##########################################################
# déplacé ici pour qu'on puisse le modifier

TAILLE_CASE = 60

############## Fonctions utilitaires ######################

# tests

def est_vide( code_case ):
    """
    Verifie si la case est vide
    """ 
    return code_case in [ VIDE_MASQUEE, VIDE_FLAG, VIDE_DEVOILE ]


def est_bombe( code_case ):
    """
    Verifie si la case contient une bombe
    """ 
    return code_case in [ BOMB_MASQUEE, BOMB_FLAG, BOMB_DEVOILE ]


def est_drapeau( code_case ):
    """
    Verifie si la case a un drapeau
    """ 
    return code_case in [ VIDE_FLAG, BOMB_FLAG ]


def est_devoile( code_case ):
    """
    Verifie si la case est dévoilée
    """ 
    return code_case in [ VIDE_DEVOILE, BOMB_DEVOILE ]


def est_masquee( code_case ):
    """
    Vérifie si la case est masquée
    """
    return code_case in [ VIDE_MASQUEE, BOMB_MASQUEE ]


# evite de passer les dimensions du jeu en paramètres à toutes les fonctions
def taille_tab_jeu(tab_jeu):
    """
    Renvoie la taille des lignes et des colonnes de la grille
    """
    taille_x = len(tab_jeu)
    taille_y = len(tab_jeu[0])
    return ( taille_x, taille_y)


def cases_voisines( tab_jeu, x, y ):
    """
    Renvoie la liste des coordonnées des cases voisines
    """
    taille_x, taille_y = taille_tab_jeu( tab_jeu )
    decalage_voisins = [(-1,0),     #nord
                        (0,1),      #est    
                        (1,0),      #sud    
                        (0,-1),     #ouest    
                        (-1,1),     #nord-est    
                        (1,1),      #sud-est    
                        (1,-1),     #sud-ouest
                        (-1,-1),    #nord-ouest
    ]

    voisins = []

    for decalage in decalage_voisins:
        #calcule les coordonnées du voisin
        x_voisin = x + decalage[0]
        y_voisin = y + decalage[1]

        # ignore les voisins inexistants (situés hors du tableau)
        if( x_voisin >= 0 and x_voisin < taille_x and y_voisin >= 0 and y_voisin < taille_y ):
            voisins.append( ( x_voisin, y_voisin ) )
    return voisins


def compte_bombes_voisines( tab_jeu, x, y ):
    """
    Renvoie le nombre de bombes qui entourent une case de coordonnées (x,y)
    """
    nb_bombes_voisines = 0
    voisins = cases_voisines( tab_jeu, x, y )
    for ( x_voisin, y_voisin ) in voisins:
        voisin = tab_jeu[x_voisin][y_voisin]
        if( est_bombe(voisin) ) :
            nb_bombes_voisines +=1

    return nb_bombes_voisines


def devoile( partie ):
    """
    Dévoile toutes les cases de la grille
    """
    tabj = partie[PARTIE_TAB]
    x, y = taille_tab_jeu(tabj)

    for ligne in range(len(tabj)):
        for case in range(x):

            code_case = tabj[ligne][case]

            if est_bombe ( code_case ):
                tabj[ligne][case] = BOMB_DEVOILE
            else: 
                # si la case ne contient pas de bombe elle est forcément vide
                tabj[ligne][case] = VIDE_DEVOILE 
