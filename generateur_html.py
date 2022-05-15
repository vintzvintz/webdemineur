import time

from commun import *



#################### Structure générale commune d'un page HTML############################

def genere_page_html_complete( titre, style, body ):
    """
    Genere une page html complete avec le contenu et les règles CSS fournies
    """
    html = f"""<html>
  <head>
    <meta charset="utf-8" />
    <title>{titre}</title>
    <style>
    {style}
    </style>
  </head>
  <body>
    {body}
  </body>
</html>
"""
    return html



#################### Règles de formattage ############################

def genere_css_grille(nb_x, nb_y, taille_case):
    """
    Les règles de formattage dépendent de la taille de la grille de jeu
    """

    # accolades doublées dans les f-strings pour descativer la substitution des variables
    # Inspiré du tutorial mozilla
    # https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Grids -->
    css= f"""
        body {{
            width: 90%;
            max-width: 1000px;
            margin: 1em auto;
            font: .9em/1.2 Arial, Helvetica, sans-serif;
        }}

        .tabjeu {{
            display: grid;
            gap: 1px;
            grid-template-columns: repeat({nb_x}, {taille_case}px);
            grid-template-rows: repeat({nb_y}, {taille_case}px);
        }}

        .tabjeu div {{
            border-radius: 3px;
            padding: 5px;
            border: 1px solid rgb(79,185,227);
        }}
        .masque {{
            background-color: rgb(200,180,220);
        }}
        .devoile {{
            background-color: rgb(200,180,220);
        }}
        .flag {{
            background-color: rgb(57,232,99);
            background-image: url('{CHEMIN_RESSOURCES}/drapeau.png');
        }}
        .bombe {{
            background-color: rgb(207,32,20);
            background-image: url('{CHEMIN_RESSOURCES}/bombe.png');
        }}
"""
    return css


def genere_html_intro():
    """
    genere la page d'accueil
    """

    body = f"""
    <p>Quel défi allez-vous relever aujourd'hui ?</p>
    <ul>
    <li><a href="{ACTION_NOUVELLE_PARTIE}?mode={PARTIE_MODE_FACILE}">Facile</a></li>
    <li><a href="{ACTION_NOUVELLE_PARTIE}?mode={PARTIE_MODE_NORMAL}">Normal</a></li>
    <li><a href="{ACTION_NOUVELLE_PARTIE}?mode={PARTIE_MODE_HARCORE}">Hardcore</a></li>
    </ul>
    """

    # CSS de la page d'accueil à compléter
    style = ""
    return genere_page_html_complete(   titre="Démineur", style=style, body=body)



##########################  Generateurs de html pour chaque type de case et pour le tableau entier ######################

def genere_lien_actions(x,y):
    """
    Génère deux éléments cliquables pour poser les drapeaux et pour creuser 
    """
    div = f"""
            <a href="/{ACTION_FLAG}?x={x}&y={y}">D</a>
            <a href="/{ACTION_CREUSE}?x={x}&y={y}">C</a> 
"""
    return div

def genere_cellule_masquee(x,y):
    actions = genere_lien_actions(x,y)
    div = f"""
        <div class="masque">
            <!-- masqué sans drapeau-->
            {actions}
        </div>
"""
    return div


def genere_cellule_drapeau(x, y):
    actions = genere_lien_actions(x,y)
    div = f"""
        <div class="flag">
            <!-- drapeau -->
            {actions}
        </div>
"""
    return div

def genere_cellule_devoilee( nb_voisins ):
    div = f"""
        <div class="devoile">
            {nb_voisins}
        </div>
"""
    return div


def genere_cellule_bombe():
    div = f"""
        <div class="bombe">
            <!-- Bombe -->
        </div>
"""
    return div


def genere_html_tab_jeu( partie ):
    """
    Genere une représentation du tableau de jeu pour insertion dans une page html
    """
    tab_jeu = partie[PARTIE_TAB]

    #etat_partie = partie[PARTIE_ETAT]

    taille_x, taille_y = taille_tab_jeu(tab_jeu)

    # on construit une liste d'éléments <div> correspondant à la liste des cases
    cellules = ""

    for x in range(taille_x):
        for y in range(taille_y):
            case = tab_jeu[x][y]
            if( case==VIDE_MASQUEE or case == BOMB_MASQUEE ):
                cellules += genere_cellule_masquee(x,y)
            elif(case==VIDE_FLAG or case == BOMB_FLAG ):
                cellules += genere_cellule_drapeau(x,y)
            elif(case==VIDE_DEVOILE):
                nb = compte_bombes_voisines(tab_jeu,x,y)
                cellules += genere_cellule_devoilee(nb)
            elif(case==BOMB_DEVOILE):
                cellules += genere_cellule_bombe()
            else:
                print('Erreur : case tab_jeu invalide')

    # on encadre la liste des cellules dans un élément <div> pour formatter la grille
    div_tableau = f"""
    <div class="tabjeu">
    {cellules}
    </div>
    """

    return div_tableau


def genere_html_partie( partie ):
    """
    genere le html pour une partie en cours
    """
    nb_x, nb_y = taille_tab_jeu( partie[PARTIE_TAB] )

    # A completer
    #  * titre = {dépend de l'état de la partie }
    #  * ajouter le temps écoulé
    #  * générer une page différente quand la partie est terminée 
    #           avec des messages perdu/gagné
    #           sans les liens dig/flag
    #           etc...


    temps = time.time() - partie[PARTIE_HEURE_DEBUT]
    print( f"Durée écoulée = {temps} ")

    css = genere_css_grille( nb_x, nb_y, 60)
    body = f"<p>Durée écoulée = {temps} </p>"
    body += genere_html_tab_jeu( partie )
    return genere_page_html_complete( titre="Partie en cours", style=css, body=body)





