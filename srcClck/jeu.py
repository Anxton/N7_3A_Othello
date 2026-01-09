'''
Résumé méthodes : 
    _init_(lignes : int = 8, colonnes : int = 8)
    init_plateau()

    jouer_tour(new_l: int, new_c: int) -> True si coup valide | False sinon
    _changer_tour() #NE PAS UTILISER, METHODE INTERNE
    fin_tour() -> "terminee" | "passe" | "joue"
    _retourner_pions(ligne : int, colonne : int) #NE PAS UTILISER, METHODE INTERNE

    get_plateau()
    get_tour()
    get_coups_possibles(couleur: str | None = None) -> couleur None = couleur du tour
    is_coup_valide(ligne: int, colonne: int, couleur: str | None = None) -> couleur None = couleur du tour
    is_partie_terminee()
    get_score()

Utilisation de la classe, exemple :

    jeu1 = Jeu()

    #jeu1.init_plateau() #Pas nécessaire, le jeu s'initialise de base à la création de l'objet. Utile pour relancer une partie sur un plateau de même taille
    
    etat = "debut"
    while etat != "terminee": #Tant qu'au moins 1 des joueurs peut jouer
        jeu1.get_plateau() #Pour affichage pions
        jeu1.get_coups_possibles() #Pour affichage coups possibles
        if jeu1.get_coups_possibles() != []: #Si le joueur actuel peut jouer
            while True:
                is_correct = jeu1.jouer_tour(new_l, new_c) #On continue à envoyer des nouvelles coordonnées de clics tant que ce n'est pas une action possible
                if is_correct:
                    break
        etat = jeu1.fin_tour() #changement de joueur

    #on peut ensuite reinitialiser le plateau pour une nouvelle partie avec :
    jeu1.init_plateau()

    # + à tout moment on peut récupérer le plateau, quel joueur joue, le score
'''
from typing import Optional

class Jeu:
    """
    Classe qui gère le déroulement d'un jeu du début à la fin
    """
    
    def __init__(self, lignes : int = 8, colonnes : int = 8):
        """
        --- Initialisation du jeu ---
        Args:
            lignes (int): OPT nombre de lignes du plateau, 8 par défaut
            colonnes(int): OPT nombre de colonnes du plateau, 8 par défaut
        Returns: Pas de retour
        """
        if lignes < 3 or colonnes < 3:
            raise ValueError("Le plateau doit au moins faire 3x3")

        self.lignes = lignes
        self.colonnes = colonnes
        self.init_plateau()

    
    def init_plateau(self, new_l: Optional[int] = 8, new_c: Optional[int] = 8):
        """
        --- Réinitialisation de partie ---
            Note : on peut relancer une partie à partir d'ici avec le même nb de [l][c] sans recréer d'objet jeu
            Args: Aucun
            Returns: Pas de retour
        """
        if new_l != None and new_c != None:
            if new_l < 3 or new_c < 3:
                raise ValueError("Le plateau doit au moins faire 3x3")
            else:
                self.lignes = new_l
                self.colonnes = new_c
            
        self.tour = "blancs"
        
        #Création plateau
        self.plateau = [[None for _ in range(self.colonnes)] 
                        for _ in range(self.lignes)]

        mid_l = self.lignes // 2
        mid_c = self.colonnes // 2
        
        self.plateau[mid_l-1][mid_c-1] = "blancs"
        self.plateau[mid_l][mid_c] = "blancs"
        self.plateau[mid_l][mid_c-1] = "noirs"
        self.plateau[mid_l-1][mid_c] = "noirs"        

    def jouer_tour(self, new_l: int, new_c: int) -> bool:
        """
        --- Déroulement complet d'un tour de jeu ---
            Args:
                new_l(int): choix du joueur : ligne
                new_c(int): choix du joueur : colonne
            Return:
                True si le coup est valide
                False si le coup n'est pas valide
        """
        if not (0 <= new_l < self.lignes and 0 <= new_c < self.colonnes) or not self.is_coup_valide(new_l,new_c):
            return False
        
        self._retourner_pions(new_l,new_c)

        return True
    
    def fin_tour(self) -> str:
        '''
        --- Fin du tour : On change de joueur. Si l'autre joueur ne peut pas jouer, le tour revient au joueur initial ---
            Return:
                "terminee": partie terminee
                "passe": tour passé, le même joueur rejoue
                "joue": changement effectué normalement
        '''
        self._changer_tour()
        if not self.get_coups_possibles():
            self._changer_tour() #on revient au joueur précédent
            if not self.get_coups_possibles():
                return 'terminee' #Plus personne ne peut jouer, fin de partie
            return "passe" #Le même joueur rejoue car l'autre ne peut pas jouer
        return 'joue' #Changement de joueur classique
    
    def _changer_tour(self):
        '''
        --- Changement joueur pour le prochain tour ---
        '''
        if self.tour == "blancs" :
            self.tour = "noirs"
        else :
            self.tour = "blancs"

    """
    --- Retournement des pions adverses une fois que le joueur a joué ---
    """
    def _retourner_pions(self, ligne : int, colonne : int):
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

# ------------------ #
# GETTERs
# ------------------ #

    def get_plateau(self):
        """
            Returns:
                Tableau des pions sur le plateau
                Tableau [l][c] de : "blancs" | "noirs" | None
        """
        return self.plateau

    def get_tour(self):
        return self.tour

    def get_coups_possibles(self, couleur: Optional[str] = None):
        """
        --- Retourne [[l,c]] des positions des coups possibles (pour le joueur dont c'est le tour) ---
            Note : Un retour non null indique que le joueur en cours peut jouer
        """
        if couleur is None :
            couleur = self.tour #Par défaut on regarde les coups possibles du tour en cours

        coups = []
        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.is_coup_valide(l, c, couleur):
                    coups.append((l, c))
        return coups
    

    def is_coup_valide(self, ligne: int, colonne: int, couleur: Optional[str] = None):
        """
        --- Vérification si un coup est valide (pour le joueur dont c'est le tour) ---
            Args:
                ligne(int): l du coup étudié
                colonne(int): c du coup étudié
                couleur(str): OPTIONNEL, couleur du joueur, celui du tour par défaut
            Returns:
                True si le coup est valide
                False sinon
        """
        if self.plateau[ligne][colonne] is not None: #case doit etre vide
            return False

        if couleur is None :
            couleur = self.tour #Par défaut on regarde les coups possibles du tour en cours
        
        opposant = 'blancs' if couleur == 'noirs' else 'noirs'
        
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
                elif self.plateau[l][c] == couleur:
                    if trouve_opposant: return True
                    else : break
                else : break #si on trouve Null (ou un ancien coup possible non enlevé encore) on sort

                l += dir_l
                c += dir_c #-> on continue dans la direction tant qu'on a trouve un opposant

        return False #si aucun coup possible n'a été trouvé


    def is_partie_terminee(self):
        """
        --- Retourne True si aucun des joueurs ne peut jouer = partie terminée ---
        """
        return ( 
            not self.get_coups_possibles("blancs") 
            and 
            not self.get_coups_possibles("noirs") 
        )

    
    def get_score(self):
        """
        --- Retourne les scores dans l'ordre : blancs, noirs ---
        """
        blancs = sum(row.count("blancs") for row in self.plateau)
        noirs  = sum(row.count("noirs") for row in self.plateau)
        return blancs, noirs