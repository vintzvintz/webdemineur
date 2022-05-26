import random, time
from commun import *
from generateur_html import *


####################### Création d'une nouvelle partie #######################

def init_serveur():
    """
    Crée le dictionaire "partie" au lancement du serveur
    Il sera complété par nouvelle_partie() quand le joueur demande le lancement d'une nouvelle partie
    """
    partie = dict()
    partie[PARTIE_ETAT]=PARTIE_ETAT_INTIAL
    partie['nb_requetes'] = 0
    return partie


def place_bombe_aleatoire( tab_jeu ):
    """
    Ajoute une bombe non dévoilée sur le tableau à un emplacement aléatoire
    """
    taille_x, taille_y = taille_tab_jeu(tab_jeu)

    # recommence tant que l'emplacement choisi n'est pas vide
    while (True):
        x = random.randint(0, taille_x-1)
        y = random.randint(0, taille_y-1)
        contenu_case = tab_jeu[x][y]
        if( est_vide(contenu_case) ):
            tab_jeu[x][y] = BOMB_MASQUEE
            break
    return tab_jeu


def init_tableau_jeu( taille_x, taille_y, nb_bombes ):
    """
    Intialise le tableau de jeu en début de partie
    """
    tab_jeu = [ [VIDE_MASQUEE]*taille_x for i in range(taille_y) ]
    for i in range(nb_bombes):
        tab_jeu = place_bombe_aleatoire(tab_jeu)
    return tab_jeu


def nouvelle_partie( partie, params):
    """
    Crée une nouvelle partie avec un mode de difficulté,
    initialise la grille, et met à jour le dictionaire "partie"
    """
    # détermine le type de partie à créer
    mode = params[PARTIE_MODE]

    # initialise le tableau de jeu
    # on peut modifier ces modes de jeu ou en rajouter un, la grille peut aussi être rectangulaire
    if( mode == PARTIE_MODE_NORMAL):               
        tab_jeu = init_tableau_jeu( 10, 10, 25) 
    elif( mode == PARTIE_MODE_HARDCORE):
        tab_jeu = init_tableau_jeu( 20, 30, 150)
    else:
        mode = PARTIE_MODE_FACILE    # le mode de partie par défaut est "facile"
        tab_jeu = init_tableau_jeu(5, 5, 3)

    # met à jour les données de la partie 
    partie[PARTIE_TAB]=tab_jeu
    partie[PARTIE_MODE] = mode
    partie[PARTIE_ETAT] = PARTIE_ETAT_EN_COURS
    partie[PARTIE_HEURE_DEBUT] = time.time()


####################### traitement de l'action "creuser" #######################

def creuse(partie, x, y):
    """
    Dévoile une case, vérifie que la partie n'est pas perdue,
    et si la case dévoilée est vide, propage les cases dévoilées
    jusqu'à trouver une case ayant une bombe voisine
    """

    tab_jeu = partie[PARTIE_TAB]

    # si la case est déja dévoilée on ne fait rien 
    if( est_devoile( tab_jeu[x][y] ) ):
        pass

    elif( est_bombe(tab_jeu[x][y]) ):
        #PERDU
        tab_jeu[x][y] = BOMB_DEVOILE
        partie[PARTIE_ETAT] = PARTIE_ETAT_PERDU

    else:
        # pas perdu car pas de bombe
        tab_jeu[x][y] = VIDE_DEVOILE

        # creuse les cases voisines non dévoilées s'il n'y a aucune bombe autour
        if( compte_bombes_voisines( tab_jeu, x, y ) == 0 ):
            for ( x_voisin, y_voisin ) in cases_voisines( tab_jeu, x, y):
                case_voisine = tab_jeu[x_voisin][y_voisin]
                if( not est_devoile(case_voisine) ):
                    creuse(partie, x_voisin, y_voisin)


####################### traitement de l'action "placer/retirer drapeau" #######################

def test_victoire(tab_jeu):
    """        
    Vérifie que les drapeaux posés sont sur les bombes en parcourant tout le tableau :
    Si il y a un drapeau sur une case vide ou si il y a une bombe sans drapeau, la 
    partie n'est pas gagnée
    """

    for ligne in tab_jeu:
        for case in ligne :
            if ( case in [BOMB_MASQUEE, VIDE_FLAG] ):
                return False

    return True



def drapeau(partie, x, y ):
    """
    Pose ou retire un drapeau sur la case (x,y) et teste la condition de victoire
    """
    tab_jeu = partie[PARTIE_TAB] # extrait le tableau de jeu du dictionnaire "partie"
    case = tab_jeu[x][y]

    if( case == VIDE_MASQUEE ):           # pose un drapeau
        tab_jeu[x][y] = VIDE_FLAG  

    elif( case == VIDE_FLAG ):            # retire un drapeau
        tab_jeu[x][y] = VIDE_MASQUEE

    elif( case == BOMB_MASQUEE ):         # pose un drapeau
        tab_jeu[x][y] = BOMB_FLAG      

    elif( case == BOMB_FLAG ):            # retire un drapeau
        tab_jeu[x][y] = BOMB_MASQUEE


    else:
        # case == VIDE_DEVOILE or case == BOMB_DEVOILE
        # on ne fait rien si la case est déja dévoilée
        pass

    if( test_victoire( tab_jeu ) ):
        partie[PARTIE_ETAT] = PARTIE_ETAT_GAGNE



####################### traitement de l'action "abandonner" ou partie terminée #######################

def devoile( partie ):
    """
    Dévoile toutes les cases de la grille
    """
    tabj = partie[PARTIE_TAB]
    taille_x, taille_y = taille_tab_jeu(tabj)

    for ligne in range(taille_x ):
        for case in range(taille_y):

            code_case = tabj[ligne][case]

            if est_bombe ( code_case ):
                tabj[ligne][case] = BOMB_DEVOILE
            else: 
                # si la case ne contient pas de bombe elle est forcément vide
                tabj[ligne][case] = VIDE_DEVOILE 


def abandonne(partie):
    devoile( partie )
    partie[PARTIE_ETAT] = PARTIE_ETAT_PERDU



####################### point d'entrée pour traiter les requetes entrantes #######################

def traite_action(partie, action, params):
    """
    Fonction appelée par le serveur HTTP pour traiter les actions de jeu

    partie = dictionnaire contenant les diverses données de la partie en cours
    action = nom de l'action de jeu (nouvelle partie, creuse, drapeau, etc....)
    params = paramètres de l'action (ex : coordonnée de la case, type de partie a créer, etc... )
    """
    # compteur de requetes
    partie['nb_requetes'] += 1
    etat_partie = partie[PARTIE_ETAT]

    try:

        if( action == ACTION_NOUVELLE_PARTIE ):
            nouvelle_partie(partie, params)

        elif( action == ACTION_INTRO ):
            # on n'affiche l'intro que si la partie n'est pas en cours
            if( not etat_partie == PARTIE_ETAT_EN_COURS ):
                return genere_html_intro()

        elif( action == ACTION_CREUSE ):
            creuse( partie, params[COORD_X], params[COORD_Y] )

        elif( action == ACTION_FLAG ):
            drapeau( partie, params[COORD_X], params[COORD_Y] )

        elif( action == ACTION_ABANDON ):
            abandonne(partie)
        
        else:
            print("Il y a un problème dans l'algorithme de traitment des actions de jeu")

    except Exception as e:
        # on ignore silencieusement les erreurs lors du traitement de l'action. Exemples
        #  - parametres de l'action absents ou invalides
        #  - action de jeu sur une partie non initialisée
        print("Erreur ignoree : ")
        print(e)

    # affichage dans la console (pour debug)
    donnees = [ f"action = {action} {params}"]
    donnees += formatte_partie_console( partie )
    for ligne in donnees:
        print( ligne )

    # genere la page HTML correspondant à la partie en cours
    return genere_html_partie( partie )


####################### Tests et aides pour le développement #######################

# utile pour afficher la tableau de jeu au format texte pour débugger 
SYMBOLES_CONSOLE = {
    VIDE_MASQUEE : 'X ',
    BOMB_MASQUEE : 'Xb',
    VIDE_DEVOILE : '. ',   # remplacé par le nb de bombes dans les cases voisines au moment de l'affichage
    VIDE_FLAG    : 'F ',
    BOMB_FLAG    : 'Fb',
    BOMB_DEVOILE : 'B '
}


def formatte_tab_jeu_console( tab_jeu ):         # aussi pour débugger
    """
    Genere une représentation du tableau de jeu en format texte
    """
    taille_x, taille_y = taille_tab_jeu(tab_jeu)
    tab_txt = []
    for x in range( taille_x ):
        ligne = []
        for y in range( taille_y ):
            case = tab_jeu[x][y]
            if( case == VIDE_DEVOILE ):
                txt = str(compte_bombes_voisines( tab_jeu, x, y ))    
                if(len( txt ) == 1):
                    txt = txt + " "
            else:
                txt = SYMBOLES_CONSOLE[case]
            ligne.append( str(txt) )

        # transforme la liste en chaine de caracteres
        ligne_txt = ' '.join(ligne)
        tab_txt.append(ligne_txt)
    
    return tab_txt


def formatte_partie_console( partie ):
    """
    Genere une représenation de toutes les données de la partie en format texte
    """
    txt = ["---------------------------------------"]
    for cle,valeur in partie.items():
        if( cle != PARTIE_TAB ):
            txt.append( f"{cle} = {valeur}")     # met à jour le tableau

    if( partie[PARTIE_ETAT] != PARTIE_ETAT_INTIAL ):
        txt = txt + formatte_tab_jeu_console( partie[PARTIE_TAB] )

    return txt
