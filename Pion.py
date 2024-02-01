class Pion:

    DIST_MAX = 2

    def __init__(self, id, x, y, joueur) :
        self.id = id
        self.x = x
        self.y = y
        self.joueur = joueur 
        self.couleur = joueur.couleur

    def deplacer(self, x, y, damier, tour) :
        dpl_x = x - self.x
        dpl_y = y - self.y
        print("Position XY actuelle :", self.x, self.y)
        print("Position sélectionnée :", self.x + dpl_x, self.y + dpl_y)

        # On vérifie si le tour correspond au pion bougé - ok
        if tour != self.joueur.id : return False

        print(damier[self.x + dpl_x][self.y + dpl_y])
        # On vérifie si la case sélectionnée est vide - ok
        if isinstance(damier[self.x + dpl_x][self.y + dpl_y], (Pion, Dame)) : return False

        # On vérifie si le déplacement est diagonale - ok
        if abs(dpl_x) != abs(dpl_y) : return False 

        # On vérifie si le pion est sur la même case - ok
        if x == self.x : return False

        # On vérifie si le déplacement est trop grand - ok
        if abs(dpl_x) > self.DIST_MAX : return False

        coef_x = -1 if dpl_x >= Pion.DIST_MAX else 1
        coef_y = -1 if dpl_y >= Pion.DIST_MAX else 1

        # On vérifie si le pion sort du plateau - ok
        if self.hors_plateau(dpl_x, dpl_y, coef_x, coef_y, damier) : return False

        # On vérifie si le joueur peux aller à l'envers - ok
        if not self.deplacement_arriere(dpl_x, dpl_y, coef_x, coef_y, damier) : return False

        if self.y + dpl_y > 9: return False
        # On bouge le pion - ok
        if abs(dpl_y) == 1 :
            self.x += dpl_x
            self.y += dpl_y
            return True
        else :
            return self.terminer_deplacement(dpl_x, dpl_y, coef_x, coef_y, damier)

    def deplacement_arriere(self, dpl_x, dpl_y, coef_x, coef_y, damier) :
        pion = True
        # On regarde si on passe au dessus d'un pion
        if (self.x + dpl_x + coef_x or self.y + dpl_y + coef_y) < len(damier) and (self.x + dpl_x + coef_x or self.y + dpl_y + coef_y) >= 0:
            pion = isinstance(damier[self.x][self.y], (Pion, Dame))

        if dpl_y == self.DIST_MAX and self.joueur == 1 and not pion :
            return False
        elif dpl_y == -self.DIST_MAX and self.joueur == 2 and not pion :
            return False
        # On vérifie que le déplacement arrière ne vaut pas 1
        elif (dpl_y == 1 and self.joueur.id == 1) or (dpl_y == -1 and self.joueur.id == 2) :
            return False

        return True

    def terminer_deplacement(self, dpl_x, dpl_y, coef_x, coef_y, damier) :
        # On vérifie si on passe par dessus un pion, si oui on le mange - ok
        if isinstance(damier[self.x + dpl_x + coef_x][self.y + dpl_y + coef_y], (Pion, Dame)) :
            print("Position du pion mangé :", self.x + dpl_x + coef_x, self.y + dpl_y + coef_y)
            pion_adverse = damier[self.x + dpl_x + coef_x][self.y + dpl_y + coef_y]
            self.x += dpl_x
            self.y += dpl_y
            return self.manger(pion_adverse, damier)
        else : return False

  