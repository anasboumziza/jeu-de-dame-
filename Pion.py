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

    def manger(self, pion, damier) :
        print(self, pion)
        if self.joueur != pion.joueur :
            self.joueur.ajouterAuCimetiere(pion)
            pion.joueur.perdrePion(pion)
            if self.enchainement(damier) : return None
            return True
        return False

    # On vérifie si le joueur peut rejouer si oui en renvoi True et le tour ne sera pas passé
    def enchainement(self, damier) :
        if (self.x + 2 or self.y + 2 or self.x - 2 or self.y - 2) > len(damier) - 2 : return False
        if (self.x + 2 or self.y + 2 or self.x - 2 or self.y - 2) < 1 : return False

        pion_environnants = [damier[self.x + 1][self.y + 1], damier[self.x - 1][self.y - 1], damier[self.x - 1][self.y + 1], damier[self.x + 1][self.y - 1]]
        cases_libres = [damier[self.x + 2][self.y + 2], damier[self.x - 2][self.y - 2], damier[self.x - 2][self.y + 2], damier[self.x + 2][self.y - 2]]

        for i in range(len(pion_environnants)) :
            if isinstance(pion_environnants[i], (Dame, Pion)) and not isinstance(cases_libres[i], (Dame, Pion)) :
                if pion_environnants[i].joueur.id != self.joueur.id :
                    return True
        return False

    # On transforme le pion courant en dame
    def promotion(self) :
        dame = Dame(self.id, self.x, self.y, self.joueur)
        self.joueur.perdrePion(self)
        self.joueur.pions.append(dame)
        return dame

    def hors_plateau(self, dpl_x, dpl_y, coef_x, coef_y, damier) :
        case_x = self.x + dpl_x
        case_y = self.y + dpl_y

        if abs(dpl_x) == 1 :
            if (case_x or case_y) > len(damier) - 1 : return True
            if (case_x or case_y) < 0 : return True
        else :
            if (case_x + coef_x or case_y + coef_y) > len(damier) - 1 : return True
            if (case_x + coef_x or case_y + coef_y) < 0 : return True
        return False

    def __eq__(self, other) :
        if self.x == other.x and self.y == other.y and self.couleur == other.couleur and self.joueur == other.joueur :
            return True


class Dame(Pion) :

    DIST_MAX = 9

    def __init__(self, id, x, y, joueur) :
        Pion.__init__(self, id, x, y, joueur)
        self.img = "./assets/crown.png"

    # La Dame peut toujours se déplacer en arrière
    def deplacement_arriere(self, dpl_x, dpl_y, coef_x, coef_y, damier) :
        case_x = self.x + dpl_x
        case_y = self.y + dpl_y
        if (case_x + coef_x or case_y + coef_y) < len(damier) and (case_x + coef_x or case_y + coef_y) >= 0:
            return True

    def terminer_deplacement(self, dpl_x, dpl_y, coef_x, coef_y, damier) :
        # On vérifie si on passe par dessus un pion, si oui on le mange - ok
        nbre_pions = 0
        index = 0
        for i in range(1, abs(dpl_y)) :
            print(nbre_pions)
            if isinstance(damier[self.x + dpl_x + (coef_x * i)][self.y + dpl_y + (coef_y * i)], (Pion, Dame)) and nbre_pions < 1:
                nbre_pions += 1
            index = i
        if nbre_pions == 1 : 
            print("Position du pion mangé :", self.x + dpl_x + coef_x, self.y + dpl_y + coef_y)
            pion_adverse = damier[self.x + dpl_x + (coef_x * index)][self.y + dpl_y + (coef_y * index)]
            self.x += dpl_x
            self.y += dpl_y
            return self.manger(pion_adverse, damier)
        elif nbre_pions == 0 : 
            self.x += dpl_x
            self.y += dpl_y
            return True
        else : return False

    # On vérifie les diagonales, si un enchainement est possible le tour n'est pas passé
    def enchainement(self, damier) :
        for i in range(1, self.DIST_MAX) :
            if (self.x + i + 1 or self.y + i + 1 or self.x - i - 1 or self.y - i - 1) > len(damier) - 1 : return False
            if (self.x + i + 1 or self.y + i + 1 or self.x - i - 1 or self.y - i - 1) < 0 : return False

            pion_environnants = [damier[self.x + i][self.y + i], damier[self.x - i][self.y - i], damier[self.x - i][self.y + i], damier[self.x + i][self.y - i]]
            cases_libres = [damier[self.x + i + 1][self.y + i + 1], damier[self.x - i][self.y - i - 1], damier[self.x - i][self.y + i + 1], damier[self.x + i + 1][self.y - i - 1]]
        
            for i in range(len(pion_environnants)) :
                if isinstance(pion_environnants[i], (Dame, Pion)) and not isinstance(cases_libres[i], (Dame, Pion)) :
                    if pion_environnants[i].joueur.id != self.joueur.id :
                        return True
        return False

        
