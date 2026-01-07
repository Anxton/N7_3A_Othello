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

    def lancer_jeu(self):
        #Création plateau
        self.plateau = [[None for _ in range(self.colonnes)] 
                        for _ in range(self.lignes)]

        mid_l = self.lignes // 2
        mid_c = self.colonnes // 2
        
        self.plateau[mid_l-1][mid_c-1] = "blancs"
        self.plateau[mid_l][mid_c] = "blancs"
        self.plateau[mid_l][mid_c-1] = "noirs"
        self.plateau[mid_l)-1][mid_c] = "noirs"
      
        self.tour = "blancs"
        interface = OthelloInterface() #front
        interface.initialiser_jeu(self.lignes,self.colonnes, self.plateau)
        #interface.set_plateau(self.plateau, self.tour) #METTRE NOM METHODE FRONT
        self.b_peutjouer = True #Indique si les blancs peuvent jouer
        self.n_peutjouer = True #Indique si les noires peuvent jouer
        self.jouer_tour() #itératif jusqu'à ce qu'aucun joueur ne puisse jouer
        self.fin_partie()

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
                elif self.plateau[l][c] == self.turn:
                    if trouve_opposant: return True
                    else : break
                else : break #si on trouve Null (ou un ancien coup possible non enlevé encore) on sort

                l += dl
                c += dc #-> on continue dans la direction tant qu'on a trouve un opposant

        return False #si aucun coup possible n'a été trouvé
            
     def jouer_tour(self):
         peut_jouer = False #si le joueur peut jouer on changera en True

         # Vérification des coups possibles
          for c in range(self.colonnes)
             for l in range(self.lignes)
                #Supprime les anciens coups possibles
                if self.plateau[l][c] == "possible" : self.plateau[c][l] = None
                #Vérifie le tour, les coups possibles, met les nouveaux coups possibles dans plateau
                if self.coup_valide(l,c) :
                    self.plateau[l][c] = "possible"
                    peut_jouer = True

         interface.set_plateau(self.plateau, self.tour)

         #Vérifie si le joueur peut jouer, sinon X_peutjouer = False
         if peut_jouer is not True : 
            if self.tour == "blancs" : self.b_peutjouer = False
            else self.n_peutjouer = False
            #si peut pas jouer on affiche qu'il ne peut pas jouer avant changement de tour ?
         else : #Si oui récupérer coup joueur
            if self.tour == "blancs" : self.b_peutjouer = True
            else self.n_peutjouer = True
            new_l, new_c = interface.get_coup() #METTRE NOM METHODE FRONT Recuperer coup
            self.plateau[new_l][new_c] = self.tour #ajouter coup
            #QUI s'occupe de refuser le coup si la case choisie n'est pas un coup possible ?
     
        # fin du tour
        if self.b_peutjouer == True or self.n_peutjouer == True
            if self.tour = "blancs" : self.tour = "noirs"
            else self.tour = "blancs"
            self.jouer_tour()
        
        #Si aucun joueur ne peut jouer (= partie terminée), on sort de la fonction

    def fin_partie(self):
        nb_blancs = 0
        nb_noirs = 0

        for c in range(self.colonnes)
             for l in range(self.lignes)
                if self.plateau[l][c] == "blancs" : nb_blancs += 1
                elif self.plateau[l][c] == "noirs" : nb_blancs += 1

        interface.set_resultat(nb_blancs, nb_noirs)



