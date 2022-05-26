import random, time
from commun import *
from generateur_html import *


####################### Création d'une nouvelle partie #######################

def init_partie_vide():
    """
    Crée le dictionaire "partie", qui contient toutes les données de partie les
    plus récentes ( le mode, l'état... )
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
    try: 
        mode = params[PARTIE_MODE]
    except:
        mode = PARTIE_MODE_FACILE    # le mode de partie par défaut est "facile"

    # initialise le tableau de jeu
    if( mode == PARTIE_MODE_FACILE):               # on peut modifier ces modes de jeu ou en rajouter un, la grille peut aussi être rectangulaire
        tab_jeu = init_tableau_jeu( 5, 5, 5)
    elif( mode == PARTIE_MODE_NORMAL ):
        tab_jeu = init_tableau_jeu( 10, 10, 25)
    elif( mode == PARTIE_MODE_HARDCORE):
        tab_jeu = init_tableau_jeu( 30, 40, 250)
    else:
        return (False, f"Type de difficulté '{mode}' invalide")
    partie[PARTIE_TAB]=tab_jeu

    # met à jour les autres paramètres
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
        return

    if( est_bombe(tab_jeu[x][y]) ):
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

def test_victoire(tab_jeu):                 # A FAIRE
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

    # cas particulier pour la page d'accueil
    if( action == ACTION_INTRO ):
        return( True, genere_html_intro())

    # modifie les données de la partie selon l'action du joueur
    elif( action == ACTION_NOUVELLE_PARTIE ):
        nouvelle_partie(partie, params)

    elif( action == ACTION_CREUSE ):
        creuse( partie, params[COORD_X], params[COORD_Y] )

    elif( action == ACTION_FLAG ):
        drapeau( partie, params[COORD_X], params[COORD_Y] )

    else:
        print( "Erreur action '{action} inconnue")

    # affichage dans la console (pour debug)
    donnees = [ f"action = {action} {params}"]
    donnees += formatte_partie_console( partie )
    for ligne in donnees:
        print( ligne )

    # genere la page HTML correspondant à la partie en cours
    html = genere_html_partie( partie )

    return ( True, html )


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
    txt = []
    for cle,valeur in partie.items():
        if( cle != PARTIE_TAB ):
            txt.append( f"{cle} = {valeur}")     # met à jour le tableau
    txt = txt + formatte_tab_jeu_console( partie[PARTIE_TAB] )
    return txt


def teste_algorithmes():
    """
    Test des algorithmes de jeu sans l'interface web
    """
    partie = init_partie_vide()
    traite_action( partie, ACTION_NOUVELLE_PARTIE, {PARTIE_MODE:PARTIE_MODE_FACILE})
    traite_action( partie, ACTION_CREUSE, {COORD_X:5, COORD_Y:5} )
    

# astuce pour executer les tests quand le module est exécuté mais pas importé
if( __name__ == '__main__'):
    teste_algorithmes()



# devoile