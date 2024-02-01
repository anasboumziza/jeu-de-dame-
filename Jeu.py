from Pion import *
import tkinter.font as tkFont


class Jeu:
    def __init__(self, canevas, joueur1, joueur2):
        self.can = canevas
        self.caseSide = 60
        self.jeu = []
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.tour = 1
        self.can.bind("<Button-1>", self.catch_object)
        self.can.bind("<Button1-Motion>", self.move_object)
        self.can.bind("<Button1-ButtonRelease>", self.leave)
        for i in range(10):
            self.jeu.append([""] * 10)

    def PlateauDeJeu(self):
        caseX, caseY = 10, 10
        self.can.create_rectangle(
            caseX,
            caseY,
            caseX + 10 * self.caseSide,
            caseY + self.caseSide,
            fill="#f4e7d3",
        )
        font = tkFont.Font(family="Roboto", size=33, weight="bold")
        self.nomJ2 = self.can.create_text(
            caseX + 5,
            caseY,
            text=self.joueur2.nom,
            anchor="nw",
            font=font,
            fill="#777777",
        )
        caseY = 10 + 11 * self.caseSide
        self.can.create_rectangle(
            caseX,
            caseY,
            caseX + 10 * self.caseSide,
            caseY + self.caseSide,
            fill="#f4e7d3",
        )
        self.nomJ1 = self.can.create_text(
            caseX + 5,
            caseY,
            text=self.joueur1.nom,
            anchor="nw",
            font=font,
            fill="purple",
        )
        caseY = 10 + self.caseSide
        for i in range(10):
            decalage_couleur = 0 if i % 2 == 0 else 1
            for l in range(10):
                couleur = "#FFF" if l % 2 == decalage_couleur else "#888"
                self.can.create_rectangle(
                    caseX,
                    caseY,
                    caseX + self.caseSide,
                    caseY + self.caseSide,
                    fill=couleur,
                    outline="",
                )
                caseX += self.caseSide
            caseY += self.caseSide
            caseX = 10
        self._initialisationPion()
        self.dessinerPions(self.joueur2)
        self.dessinerPions(self.joueur1)

    def _initialisationPion(self):
        idPions = 105
        for i in range(10):
            for l in range(10):
                joueur = self.joueur1
                if i <= 4:
                    joueur = self.joueur2
                elif i >= 6:
                    joueur = self.joueur1
                if i < 4 or i >= 6:
                    if i % 2 == 0:
                        if l % 2 != 0:
                            pion = Pion(idPions, l, i, joueur)
                            joueur.pions.append(pion)
                            self.jeu[l][i] = pion
                            idPions += 1
                    else:
                        if l % 2 == 0:
                            pion = Pion(idPions, l, i, joueur)
                            joueur.pions.append(pion)
                            self.jeu[l][i] = pion
                            idPions += 1

    def dessinerPions(self, joueur):
        for pion in joueur.pions:
            x = 10 + pion.x * self.caseSide
            y = 10 + self.caseSide + pion.y * self.caseSide
            self.can.create_oval(
                x + 5,
                y + 5,
                x + self.caseSide - 5,
                y + self.caseSide - 5,
                fill=pion.joueur.couleur,
                outline="purple",
            )

    def clear(self):
        self.can.delete("all")
        self.caseColor = "white"
        self.jeu = []
        for i in range(10):
            self.jeu.append([""] * 10)

    def catch_object(self, event):
        self.x1, self.y1 = event.x, event.y
        self.select_object = self.can.find_closest(self.x1, self.y1)
        print(self.select_object)
        if self.select_object[0] > 104 and self.select_object[0] < 145:
            self.xInitial = int(self.x1 / self.caseSide)
            self.yInitial = int(self.y1 / self.caseSide) - 1

            if isinstance(self.jeu[self.xInitial][self.yInitial], Pion):
                self.pionEnCours = self.jeu[self.xInitial][self.yInitial]
                print(self.pionEnCours.id)
            self.can.lift(self.select_object)

    def move_object(self, event):
        x2, y2 = event.x, event.y
        dx, dy = x2 - self.x1, y2 - self.y1
        if self.select_object[0] > 104 and self.select_object[0] < 145:
            self.can.move(self.select_object, dx, dy)
            self.x1, self.y1 = x2, y2

    def leave(self, event):
        if self.select_object[0] > 104 and self.select_object[0] < 145:
            if self.x1 < 10 + 10 * self.caseSide and self.y1 < 10 + 11 * self.caseSide:
                self.x1, self.y1 = (
                    10 + int(self.x1 / self.caseSide) * self.caseSide,
                    10 + int(self.y1 / self.caseSide) * self.caseSide,
                )
                newX = int(self.x1 / self.caseSide)
                newY = int(self.y1 / self.caseSide) - 1
                resultatDeplacement = self.pionEnCours.deplacer(
                    newX, newY, self.jeu, self.tour
                )
                # Si le pion peut etre déplacé alors on recentre le pion puis on modifie la position dans le tableau self.jeu
                if resultatDeplacement == True or resultatDeplacement == None:
                    if (self.pionEnCours.joueur.id == 1 and newY == 0) or (
                        self.pionEnCours.joueur.id == 2 and newY == 9
                    ):
                        self.pionEnCours = self.pionEnCours.promotion()
                        self.can.itemconfigure(
                            (self.pionEnCours.id,), outline="red", width="5"
                        )
                    self.can.coords(
                        self.select_object,
                        self.x1 + 5,
                        self.y1 + 5,
                        self.x1 + self.caseSide - 5,
                        self.y1 + self.caseSide - 5,
                    )
                    self.jeu[self.xInitial][self.yInitial] = ""
                    self.jeu[newX][newY] = self.pionEnCours
                    for i in self.joueur1.cimetiere + self.joueur2.cimetiere:
                        y = 15 if i.joueur == self.joueur1 else 15 + 11 * self.caseSide
                        self.can.coords(
                            (i.id,),
                            15 + i.x * self.caseSide,
                            y,
                            10 + i.x * self.caseSide + self.caseSide - 5,
                            y + self.caseSide - 10,
                        )
                    if resultatDeplacement:
                        self.tour = 1 if self.tour == 2 else 2
                        if self.tour == 1:
                            self.can.itemconfigure(self.nomJ1, fill="purple")
                            self.can.itemconfigure(self.nomJ2, fill="gray")
                        elif self.tour == 2:
                            self.can.itemconfigure(self.nomJ2, fill="purple")
                            self.can.itemconfigure(self.nomJ1, fill="gray")
                    self._enleverPionMortDuJeu(self.joueur1)
                    self._enleverPionMortDuJeu(self.joueur2)
                else:
                    x1 = 10 + self.pionEnCours.x * self.caseSide
                    y1 = 10 + self.caseSide + self.pionEnCours.y * self.caseSide
                    self.can.coords(
                        self.select_object,
                        x1 + 5,
                        y1 + 5,
                        x1 + self.caseSide - 5,
                        y1 + self.caseSide - 5,
                    )
                    del self.x1, self.y1, newX, newY
            else:
                x1 = 10 + self.pionEnCours.x * self.caseSide
                y1 = 10 + self.caseSide + self.pionEnCours.y * self.caseSide
                self.can.coords(
                    self.select_object,
                    x1 + 5,
                    y1 + 5,
                    x1 + self.caseSide - 5,
                    y1 + self.caseSide - 5,
                )

            # test de victoire
            if len(self.joueur1.pions) == 0 or len(self.joueur2.pions) == 0:
                font = tkFont.Font(family="Roboto", size=65, weight="bold")
                self.can.create_text(
                    120,
                    120,
                    text=self.joueur2.nom,
                    anchor="w",
                    font=font,
                    fill="#777777",
                )

    def _enleverPionMortDuJeu(self, joueur):
        for pionMort in joueur.cimetiere:
            if (
                isinstance(self.jeu[pionMort.x][pionMort.y], Pion)
                and self.jeu[pionMort.x][pionMort.y].id == pionMort.id
            ):
                self.jeu[pionMort.x][pionMort.y] = ""


class Joueur:
    def __init__(
        self,
        id,
        couleur,
        nom="Joueur",
    ):
        self.id = id
        self.nom = nom
        self.couleur = couleur
        self.pions = []
        self.cimetiere = []

    def ajouterAuCimetiere(self, pion):
        self.cimetiere.append(pion)

    def perdrePion(self, pion):
        for p in self.pions:
            if p == pion:
                self.pions.remove(p)
