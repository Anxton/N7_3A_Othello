'''
INFOS POUR RELIER : 
Début du jeu, renvoie : plateau[l][c] avec l et c qui peuvent être modifiés à volonté

'''

class Jeu:
    """
    Classe qui gère le déroulement d'un jeu du début à la fin
    """

    """
    --- Méthode pour envoyer messages au front ---
    """
    #def afficher_message(self, texte: str, type_msg: str = "info"):
        #type_msg peut être : "info", "erreur", "alerte"
     #   self.interface.afficher_message(texte, type_msg) #faire cette méthode dans front

    """
    --- Initialisation du jeu ---
    """
    def __init__(self, blancs : str, noirs : str, lignes : int, colonnes : int):
        self.blancs = blancs
        self.noirs = noirs
        self.lignes = lignes
        self.colonnes = colonnes
        self.lancer_jeu()

    """
    --- Lancement de partie ---
        RETOURNE : plateau en début de partie avec les coups possibles pour le joueur blanc qui débute
    """
    def lancer_jeu(self, lignes, colonnes):
        self.lignes = lignes
        self.colonnes = colonnes
        
        #Création plateau
        self.plateau = [[None for _ in range(self.colonnes)] 
                        for _ in range(self.lignes)]

        mid_l = self.lignes // 2
        mid_c = self.colonnes // 2
        
        self.plateau[mid_l-1][mid_c-1] = "blancs"
        self.plateau[mid_l][mid_c] = "blancs"
        self.plateau[mid_l][mid_c-1] = "noirs"
        self.plateau[mid_l-1][mid_c] = "noirs"
      
        self.tour = "blancs"      
        
        #interface.set_plateau(self.plateau, self.tour) #METTRE NOM METHODE FRONT
        self.b_peutjouer = True #Indique si les blancs peuvent jouer
        self.n_peutjouer = True #Indique si les noires peuvent jouer

        # Ajout des coups possibles
        for l in range(self.lignes):
            for c in range(self.colonnes):
                #Vérifie le tour, les coups possibles, met les nouveaux coups possibles dans plateau
                if self.coup_valide(l,c) :
                    self.plateau[l][c] = "possible"
                    peut_jouer = True

        return self.plateau #renvoie la position des pions en début de partie
        #while self.b_peutjouer or self.n_peutjouer :
        #    self.jouer_tour() #itératif jusqu'à ce qu'aucun joueur ne puisse jouer
        #self.fin_partie()

    """
    --- Vérification si un coup est valide ---
    """
    def coup_valide(self, ligne, colonne):
        if self.plateau[ligne][colonne] is not None: #case doit etre vide
            return False

        opposant = 'blancs' if self.tour == 'noirs' else 'noirs'
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]

        for dir_l, dir_c in directions:
            l = ligne + dir_l
            c = colonne + dir_c
            trouve_opposant = False

            # On vérifie que l et c sortent pas des possibles
            while 0 <= l < self.lignes and 0 <= c < self.colonnes:
                if self.plateau[l][c] == opposant : trouve_opposant = True
                elif self.plateau[l][c] == self.tour:
                    if trouve_opposant: return True
                    else : break
                else : break #si on trouve Null (ou un ancien coup possible non enlevé encore) on sort

                l += dir_l
                c += dir_c #-> on continue dans la direction tant qu'on a trouve un opposant

        return False #si aucun coup possible n'a été trouvé

    """
    --- Déroulement complet d'un tour de jeu ---
        RETOURNE : plateau après le coup joué avec les coups possibles pour le prochain joueur ou une erreur si le coup n'est pas valide
    """
    def jouer_tour(self, new_l, new_c):
            #if not self.b_peutjouer and  self.n_peutjouer :
        #    self.jouer_tour() #itératif jusqu'à ce qu'aucun joueur ne puisse jouer
        
            coup_valide = False
            while not coup_valide:
                #new_l, new_c = self.interface.get_coup() #METTRE NOM METHODE FRONT Recuperer coup
                if self.plateau[new_l][new_c] == "possible": coup_valide = True
                else : return "Case invalide !"
     
        # fin du tour -> Changement joueur pour le prochain tour
        if self.tour == "blancs" :
            self.tour = "noirs"
        else :
            self.tour = "blancs"

        peut_jouer = False #si le joueur peut jouer on changera en True

        #Supprime les anciens coups possibles
        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.plateau[l][c] == "possible" : self.plateau[l][c] = None

        # Changement des des coups possibles pour le suivant
        for l in range(self.lignes):
            for c in range(self.colonnes):
                #Vérifie le tour, les coups possibles, met les nouveaux coups possibles dans plateau
                if self.coup_valide(l,c) :
                    self.plateau[l][c] = "possible"
                    peut_jouer = True

        #Vérifie si le joueur peut jouer, sinon X_peutjouer = False
        if peut_jouer is not True : 
            if self.tour == "blancs" :
                self.b_peutjouer = False
            else :
                self.n_peutjouer = False
        else : #Si oui récupérer coup joueur
            if self.tour == "blancs" :
                self.b_peutjouer = True
            else:
                self.n_peutjouer = True

        return self.plateau

    """
    --- Retournement des pions adverses une fois que le joueur a joué ---
    """
    def retourner_pions(self, ligne, colonne):
        self.plateau[ligne][colonne] = self.tour #ajouter coup

        opposant = 'blancs' if self.tour == 'noirs' else 'noirs'
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]

        for dir_l, dir_c in directions:
            l = ligne + dir_l
            c = colonne + dir_c
            pions = [] #pions adverses par lesquels on passe 

            # On vérifie que l et c sortent pas des possibles
            while 0 <= l < self.lignes and 0 <= c < self.colonnes:
                if self.plateau[l][c] == opposant: pions.append((l, c))
                elif self.plateau[l][c] == self.tour: #quand on tombe sur notre couleur
                    for pl, pc in pions: #on change les pions adverses croisés avant
                        self.plateau[pl][pc] = self.tour
                    break
                else: break

                l += dir_l
                c += dir_c #-> on continue dans la direction tant qu'on a trouve un opposant

        self.interface.set_plateau(self.plateau, self.tour) #update avec le nouveau coup

    """
    --- Fin de partie ---
    """
    def fin_partie(self):
        nb_blancs = 0
        nb_noirs = 0

        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.plateau[l][c] == "blancs" : nb_blancs += 1
                elif self.plateau[l][c] == "noirs" : nb_noirs += 1

        if nb_blancs == nb_noirs : self.afficher_message(f"Partie terminée\nEgalité\n{nb_blancs} Blancs        Noirs {nb_noirs}")
        elif nb_blancs > nb_noirs : self.afficher_message(f"Partie terminée\nLes Blancs gagnent !\n{nb_blancs} Blancs        Noirs {nb_noirs}")
        else : self.afficher_message(f"Partie terminée\nLes Noirs gagnent !\n{nb_blancs} Blancs        Noirs {nb_noirs}")
        
        #self.interface.set_resultat(nb_blancs, nb_noirs)

    def get_plateau(self):
        return self.plateau

    def get_tour(self):
        return self.tour

    get 

    
        

