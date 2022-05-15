
from constantes import *


def genere_page_html_complete( titre, body ):
    """
    Genere une page html complete avec le contenu indiqué
    """

    css = CHEMIN_RESSOURCES + "/demin_style.css"

    head = f"""
    <meta charset="utf-8" />
    <title>{titre}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{css}" type="text/css" />
"""

    html = f"""<html>
  <head>
    {head}
  </head>
  <body>
    {body}
  </body>
</html>
"""
    return html



def genere_html_intro():
    """
    genere la page html de lancement du jeu
    """

    body = f"""
    <p>Page avec des liens pour lancer une nouvelle partie</p>
    <ul>
    <li><a href="{ACTION_NOUVELLE_PARTIE}?mode={PARTIE_MODE_FACILE}">Facile</a></li>
    <li><a href="{ACTION_NOUVELLE_PARTIE}?mode={PARTIE_MODE_NORMAL}">Normal</a></li>
    <li><a href="{ACTION_NOUVELLE_PARTIE}?mode={PARTIE_MODE_HARCORE}">Hardcore</a></li>
    </ul>
    """
    return genere_page_html_complete( titre="Démineur", body=body)



def formatte_tab_jeu_html( tab_jeu ):
    """
    Genere une représentation du  tableau de jeu pour insertion dans une page html
    """
    pass



def genere_html_partie_en_cours( partie ):
    """
    genere le html pour une partie en cours
    """
    # A COMPLETER
    body = "wesh wesh wesh"
    return genere_page_html_complete( titre="Partie en cours", body=body)



def genere_html_fin(tab_jeu):
    """
    genere la page html de lancement du jeu
    """
    # A COMPLETER
    body = "Page avec le tableau de jeu entierement dévoilé, une message perdu/gagné et un lien vers la page d'intro pour relancer une nouvelle partie"
    return genere_page_html_complete( titre="Partie terminée", body=body)




