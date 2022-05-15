
import random
from constantes import *
from generateur_html import *


# Taille du tableau de jeu
DIM_X = 8
DIM_Y = 12


# Etats possibles pour chaque case du tableau de jeu
VIDE_MASQUEE = 'vm'
VIDE_FLAG    = 'vf'
VIDE_DEVOILE = 'vd'
BOMB_MASQUEE = 'bm'
BOMB_FLAG    = 'bf'
BOMB_DEVOILE = 'bd'


# tests
def est_vide( code_case ): 
    return code_case in [ VIDE_MASQUEE, VIDE_FLAG, VIDE_DEVOILE ]

def est_bombe( code_case ):
    return code_case in [ BOMB_MASQUEE, BOMB_FLAG, BOMB_DEVOILE ]

def est_drapeau( code_case ):
    return code_case in [ VIDE_FLAG, BOMB_FLAG]

def est_devoile( code_case ):
    return code_case in [ VIDE_DEVOILE, BOMB_DEVOILE]


def init_partie_vide():
    partie = dict()
    partie[PARTIE_ETAT]=PARTIE_ETAT_INTIAL
    partie['nb_requetes']=0
    return partie


def taille_tab_jeu(tab_jeu):
    """
    """
    taille_x = len(tab_jeu)
    taille_y = len(tab_jeu[0])
    return ( taille_x, taille_y)



def cases_voisines( tab_jeu, x, y ):
    """
    renvoie la liste des coordonnées des cases voisines
    """
    taille_x, taille_y = taille_tab_jeu(tab_jeu)
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
        if( x_voisin>=0 and x_voisin<taille_x and y_voisin>=0 and y_voisin<taille_y ):
            voisins.append((x_voisin, y_voisin))
    return voisins


def compte_bombes_voisines(tab_jeu, x, y):
    """
    renvoie le nombre de bombes qui entourent une case de coordonnées (x,y)
    """
    nb_bombes_voisines = 0
    voisins = cases_voisines(tab_jeu, x,y)
    for (x_voisin, y_voisin) in voisins:
        voisin = tab_jeu[x_voisin][y_voisin]
        if( est_bombe(voisin) ) :
            nb_bombes_voisines +=1
    return nb_bombes_voisines




# utile pour debug en mode texte
SYMBOLES_CONSOLE = {
    VIDE_MASQUEE : 'x ',
    BOMB_MASQUEE : '+ ',
    VIDE_DEVOILE : '. ',
    VIDE_FLAG    : 'f ',
    BOMB_FLAG    : 'F',
    BOMB_DEVOILE : 'B '
}


def formatte_tab_jeu_console( tab_jeu ):
    """
    Genere une représentation du tableau de jeu pour affichage dans la console
    """
    taille_x, taille_y = taille_tab_jeu(tab_jeu)
    tab_txt = []
    for x in range(taille_x):
        ligne = []
        for y in range(taille_y):
            case = tab_jeu[x][y]
            if( case==VIDE_DEVOILE ):
                txt = str(compte_bombes_voisines( tab_jeu, x, y ))
                if( len(txt)==1 ):
                    txt = txt+" "
            else:
                txt = SYMBOLES_CONSOLE[case]
            ligne.append(str(txt))

        # transforme la liste en chaine de caracteres
        ligne_txt = ' '.join(ligne)
        tab_txt.append(ligne_txt)
    return tab_txt



def formatte_partie_console( partie ):
    txt = []
    for cle,valeur in partie.items():
        if( cle != PARTIE_TAB ):
            txt.append( f"{cle} = {valeur}")
    txt = txt+formatte_tab_jeu_console(partie[PARTIE_TAB])
    return txt


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
    # détermine le type de partie à créer
    try: 
        mode = params[PARTIE_MODE]
    except:
        mode = PARTIE_MODE_FACILE

    # initialise le tableau de jeu
    if( mode == PARTIE_MODE_FACILE):
        tab_jeu = init_tableau_jeu( 10, 10, 5)
    elif( mode == PARTIE_MODE_NORMAL ):
        tab_jeu = init_tableau_jeu( 10, 10, 25)
    elif( mode == PARTIE_MODE_HARCORE):
        tab_jeu = init_tableau_jeu( 30, 40, 250)
    else:
        return (False, f"Type de difficulté '{mode}' invalide")
    partie[PARTIE_TAB]=tab_jeu

    # met à jour les autres paramètres
    partie[PARTIE_MODE]=mode
    partie[PARTIE_ETAT]=PARTIE_ETAT_EN_COURS



def creuse(partie, x, y):

    tab_jeu = partie[PARTIE_TAB]

    # si la case est déja dévoilée on ne fait rien 
    if( est_devoile(tab_jeu[x][y]) ):
        return

    if(est_bombe(tab_jeu[x][y])):
        #PERDU
        tab_jeu[x][y] = BOMB_DEVOILE
        partie[PARTIE_ETAT] = PARTIE_ETAT_PERDU
    else:
        # pas perdu car pas de bombe
        tab_jeu[x][y] = VIDE_DEVOILE

        # creuse récursivement les cases voisines non dévoilées s'il n'y a aucune bombe autour
        if( compte_bombes_voisines(tab_jeu,x,y)==0 ):
            for (x_voisin, y_voisin) in cases_voisines( tab_jeu, x, y):
                case_voisine = tab_jeu[x_voisin][y_voisin]
                if( not est_devoile(case_voisine) ):
                    creuse(partie, x_voisin, y_voisin)

def test_victoire(tab_jeu):
    return False


def drapeau(partie, x, y ):
    """
    pose ou retire un drapeau sur la case (x,y) et teste la condition de victoire
    """
    tab_jeu = partie[PARTIE_TAB]
    case = tab_jeu[x][y]

    if( case == VIDE_MASQUEE ):
        tab_jeu[x][y] = VIDE_FLAG
    elif( case == VIDE_FLAG ):
        tab_jeu[x][y] = VIDE_MASQUEE
    elif( case == BOMB_FLAG ):
        tab_jeu[x][y] = BOMB_MASQUEE
    elif( case == BOMB_MASQUEE ):
        tab_jeu[x][y] = BOMB_FLAG
    else:
        # case == VIDE_DEVOILE or case == BOMB_DEVOILE
        # on ne fait rien si la case est déja dévoilée
        pass

    if( test_victoire(tab_jeu) ):
        partie[PARTIE_ETAT]=PARTIE_ETAT_GAGNE



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
        drapeau( partie, params )
    else:
        pass  
        #erreur action inconnue


    # affichage dans la console (pour debug)
    donnees = [ f"action = {action} {params}"]
    donnees += formatte_partie_console(partie)
    for ligne in donnees:
        print( ligne )


    # Pour tester
    body = "<br>".join(donnees)
    html = genere_page_html_complete( "Wesh bro", "<pre>"+body+"</pre>")

    # A COMPLETER
    # html = genere_html_partie(partie)

    # Envoi vers l'utilisateur
    return (True, html)


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