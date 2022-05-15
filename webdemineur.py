from http.server import SimpleHTTPRequestHandler
import socketserver

# permet d'appeler les fonctions définies dans d'autres fichiers
from constantes import *
from algos_jeu import *

PORT_HTTP = 8000

EXTENSIONS_FICHIERS_STATIQUES = [ ".css",    # feuille de style
                                 ".png"]    # images


# Variable globale contenant les données de la partie en cours
# sera rempli par les fonctions dans algos_jeu.py
partie = init_partie_vide()


def decode_parametres(chaine):
    """
    interprete les parametres d'une action, reçus sous forme d'une chaine de caractères 
    chaine = "parametre1=valeur1&parametre2=valeur2&parametre3=valeur3 ......"
    renvoie un dictionnaire = 
    { parametre1 : valeur1,
      parametre2 : valeur2,
      etc...}
    """

    # Les parametres sont séparés par le caractere '&'
    liste1 = chaine.split('&')

    params = dict()
    for p in liste1:
        # le nom du parametre et la valeur sont séparés par un signe =
        paire = p.split('=')
        
        if( len(paire)==1 ):
            # parametre sans valeurs 
            paire = (p, None)
        
        if( len(paire) not in [1,2] ):
            # cas non prévu
            print( f"Erreur : les parametres de la requete sont invalides : {chaine}" )
        
        # ajoute au dictionnaire
        params[paire[0]] = paire[1]

    return params



def analyse_requete(path):
    """
    détermine si la requete concerne un fichier ou une action de jeu

    renvoie une paire
    ('statique', None) pour les ressources statiques
    ('intro', None) pour la page d'accueil
    (nom_action, dict(parametres) ) pour les actions de jeu
    ('erreur', None ) si la requete est invalide
    """

    # cas particulier pour la page d'accueil
    if( path== "/" or path==""):
        return (ACTION_INTRO, None)

    # Est-ce une action de jeu ?
    for action in LISTE_ACTIONS:
        if( path.startswith( '/'+action ) ):
            params_chaine = path[ len(action)+2 : ]     # recupere la partie "paramètres" de la requete
            params = decode_parametres(params_chaine)
            return ( action, params )

    # Est-ce une ressource statique ?
    extension = path[-4:]
    if( extension in EXTENSIONS_FICHIERS_STATIQUES ):
        return ('statique', path)

    # Est-ce autre chose qu'une action ou une ressource ?
    return ('erreur',None)


# Utilisation HTTPRequestHandler inspiré d'exemples trouvés sur internet
class DemineurRequestHandler( SimpleHTTPRequestHandler ):
    """
    Traitement des requetes reçues par le serveur
    """

    def do_GET(self):
        """
        la fonction do_GET() d'origine dans SimpleHTTPRequestHandler permet uniquement 
        de renvoyer des fichiers statiques.

        Cette version est modifiée pour gerer également les actions de jeu
        """

        print( self.requestline )

        action,params = analyse_requete(self.path)

        # pour les ressources statiques, on appelle la fonction do_GET d'origine de SimpleHTTPRequestHandler qui s'occupe de tout
        if( action == 'statique' ):
            return super().do_GET()

        # pour les actions de jeu, on appelle traite_action() et on transfère son résultat au client 
        # traite_action doit renvoyer du html

        # Réponse par défaut = erreur
        code_reponse = 500
        contenu_reponse = "Erreur interne"

        if( action in LISTE_ACTIONS ):
            # execute l'action de jeu sur la partie en cours, avec les paramètres indiqués
            succes, contenu = traite_action(partie, action, params)

            # change le code de réponse par défaut en cas de succès
            if(succes):
                code_reponse = 200

            if(contenu):
                # contenu = message d'erreur éventuel ou page HTML en cas de succès
                contenu_reponse = contenu

        else:  #( not action == 'erreur' ):
            # Erreur 404 si l'action est inconnue
            code_reponse = 404
            contenu_reponse = "Ressource non trouvée"

        self.send_response( code_reponse )
        self.send_header('content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(contenu_reponse.encode())


def run():
    # Code magique trouvé sur internet pour lancer un serveur HTTP
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer( ("", PORT_HTTP), DemineurRequestHandler) as httpd:
        httpd.allow_reuse_address=True
        print("Serveur ouvert sur le port ", PORT_HTTP)

        httpd.serve_forever()


if (__name__ == "__main__" ):
    # init_tableau_jeu(DIM_X, DIM_Y, 10)
    run()


