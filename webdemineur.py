from http.server import SimpleHTTPRequestHandler
import socketserver

# permet d'appeler les fonctions définies dans d'autres fichiers
from commun import *
from algos_jeu import *

PORT_HTTP = 8000 # peut être modifié

EXTENSIONS_FICHIERS_STATIQUES = [ ".css",    # feuille de style
                                  ".png"]    # images


# Variable globale contenant les données de la partie en cours
# sera rempli et modifié par des fonctions dans algos_jeu.py à chaque évènement de la partie.
partie = init_serveur()



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

        cle = paire[0]
        valeur = paire[1]

        # conversion en entier des coordonnées
        if (cle in [COORD_X, COORD_Y]):
            valeur = int(valeur)
        
        # ajoute au dictionnaire
        params[cle] =  valeur

    return params


def analyse_requete(path):
    """
    détermine si la requete concerne un fichier ou une action de jeu
    renvoie une paire
    ('statique', None) pour les ressources statiques ( les images )
    (nom_action, dict(parametres) ) pour les actions de jeu et la page d'accueil
    ('erreur', None ) si la requete est invalide
    """

    # Est-ce une ressource statique ?
    extension = path[-4:]    # pour vérifier si le fichier est .png, .css...
    if( extension in EXTENSIONS_FICHIERS_STATIQUES ):
        return ( 'statique', path )

    # cas particulier pour la page d'accueil
    if( path == "/" or path == ""):
        return (ACTION_INTRO, None)

    # Est-ce une action de jeu connue ?
    for action in LISTE_ACTIONS:
        if( path.startswith( '/' + action ) ):
            params_chaine = path[ len(action) + 2 : ]     # recupere la partie "paramètres" de la requete
            params = decode_parametres( params_chaine )
            return ( action, params )

    # Les autres requetes sont invalides
    return ( 'erreur', None )


# Utilisation HTTPRequestHandler, trouvée sur internet et modifiée
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

        # analyse la requete pour savoir si c'est une action ou une ressource statique
        action, params = analyse_requete(self.path)

        # pour les ressources statiques, on appelle la fonction do_GET d'origine de SimpleHTTPRequestHandler qui s'occupe de tout
        if( action == 'statique' ):
            return super().do_GET()

        # en dehors des ressources statiques, on doit traiter la requete nous-memes et renvoyer une réponse au client
        if( action == 'erreur' ):
            # pour les requetes non reconnues, on renvoie une erreur
            code_reponse = 500
            html = genere_page_erreur( f"<p>Requete invalide : <pre> {self.requestline}<pre></p>" )
        else:
            # pour les actions de jeu, on appelle traite_action() avec les données de la partie en cours
            code_reponse = 200
            html = traite_action( partie, action, params )


        self.send_response( code_reponse )
        self.send_header('content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())


####################### Point d'entrée principal de l'application #######################

def run():
    # Code trouvé sur internet pour lancer un serveur HTTP
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer( ("", PORT_HTTP), DemineurRequestHandler) as httpd:
        print( f"\nServeur ouvert sur http://127.0.0.1:{PORT_HTTP}\n")

        httpd.serve_forever()

if (__name__ == "__main__" ):
    run()

