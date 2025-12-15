class Jeu:
    """
    Classe qui gère le déroulement d'un jeu du début à la fin
    """

    #blancs, noirs, lignes, colonnes, tour, fi
    # Initialisation de la classe
    #def __init__(self, blancs : Joueur, noirs : Joueur, lignes : int, colonnes : int):
    def __init__(self, blancs : str, noirs : str, lignes : int, colonnes : int):
        self.blancs = blancs
        self.noirs = noirs
        self.lignes = lignes
        self.colonnes = colonnes
        self.lancer_jeu()

    def lancer_jeu():
        #Création plateau
        self.plateau = [[None for _ in range(colonnes)] for _ in range(lignes)]
        self.plateau[(colonnes/2)-1][(lignes/2)-1] = "blancs"
        self.plateau[colonnes/2][lignes/2] = "blancs"
        self.plateau[colonnes/2][(lignes/2)-1] = "noirs"
        self.plateau[(colonnes/2)-1][(lignes/2)] = "noirs"
      
        self.tour = blancs
        interface = OthelloInterface() #front
        interface.initialiserJeu() #METTRE NOM METHODE FRONT
        self.b_peutjouer = True #Indique si les blancs peuvent jouer
        self.n_peutjouer = True #Indique si les noires peuvent jouer
        self.jouer_tour()

    def jouer_tour():
      # Vérification des coups possibles
      for c in range(0,colonnes)
        for l in range(0,lignes)
            #Supprime les anciens coups possibles
            if self.plateau[c][l] = "possible" : self.plateau[c][l] = None

            #Vérifie le tour, les coups possibles, met les nouveaux coups possibles dans plateau

            #Vérifie si le joueur peur jouer, sinon X_peutjouer = False

            #Si oui récupérer coup joueur et fin du tour

            #Si joueur peut pas jouer fin du tour, voir comment voir si l'autre peut jouer

      
      
      




