from tkinter import *
from Jeu import *

class Menu:
    def __init__(self, fenetre, canvas, imgBg, imgPlay, imgRules, imgNext):
        self.fen = fenetre
        self.can = canvas
        self.imgBg = imgBg
        self.imgPlay = imgPlay
        self.imgRules = imgRules
        self.imgNext = imgNext
        can.create_image(w, h, image=self.imgBg, anchor="se")
        self.init_buttons()

    def init_buttons(self):
        buttonPosX = h / 2
        buttonPosY = w / 2
        playB = Button(
            self.fen, command=self.setOptions, image=self.imgPlay, borderwidth=0
        )
        playB.pack()
        playB.place(x=buttonPosX, y=buttonPosY, anchor="center")

    def setOptions(self):
        for l in (
            self.fen.grid_slaves() + self.fen.pack_slaves() + self.fen.place_slaves()
        ):
            if not isinstance(l, Canvas):
                l.destroy()
        self.fen.title("md4")
        title = Label(self.fen, text="Préparation de la partie")
        title.config(width=200)
        title.pack()
        self.buttonPosX = h / 2
        self.buttonPosY = w / 2
        self.nomJoueur1 = StringVar()
        self.nomJoueur2 = StringVar()
        entryJoueur1 = self.makeentry(
            self.fen, "Nom du joueur 1 :", text="test1", textvariable=self.nomJoueur1
        )
        entryJoueur2 = self.makeentry(
            self.fen, "Nom du joueur 2 :", text="test", textvariable=self.nomJoueur2
        )
        start = Button(
            self.fen, command=self.ClearPlay, image=self.imgNext, borderwidth=0
        )
        start.pack()

    def makeentry(self, parent, texte, **options):
        Label(self.fen, text=texte).pack()
        entry = Entry(parent, **options).pack()
        return entry

    def ClearPlay(self):
        for l in (
            self.fen.grid_slaves() + self.fen.pack_slaves() + self.fen.place_slaves()
        ):
            l.destroy()
        self.startGame(self.nomJoueur1.get(), self.nomJoueur2.get())
        """ self.can.delete("all")
        self.caseColor = 'white'
        self.jeu = []
        for i in range(10):
            self.jeu.append(['']*10)"""

    def startGame(self, nomJ1, nomJ2):
        self.fen.title("dame")
        self.fen.geometry("%dx%d+%d+%d" % (740, 740, 600, 180))
        nomJ1 = "Joueur 1" if nomJ1 == "" else nomJ1
        nomJ2 = "Joueur 2" if nomJ2 == "" else nomJ2
        j1 = Joueur(1, "white", nomJ1)
        j2 = Joueur(2, "black", nomJ2)
        can1 = Canvas(self.fen, bg="dark grey", height=740, width=740)
        can1.pack(side=LEFT)
        j = Jeu(can1, j1, j2)
        # can1 = Canvas(fenGame, bg='white', height=740, width=740)can1.pack(side=LEFT)
        bou1 = Button(self.fen, text="Damier", command=j.PlateauDeJeu())
        bou1.pack(side=TOP)
        bou2 = Button(self.fen, text="clear", command=j.clear)
        bou2.pack(side=TOP)


fenMenu = Tk()
fenMenu.title("dame")
fenMenu.resizable(0, 0)
global x, y, ws, hs
h = 740
w = 740
ws = fenMenu.winfo_screenwidth()
hs = fenMenu.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
fenMenu.geometry("%dx%d+%d+%d" % (w, h, x, y))
can = Canvas(fenMenu, width=w, height=h)
can.pack(side=LEFT)
can.place(in_=fenMenu, x=0)
imageBg = PhotoImage(file="assets/Checkers.png")
imagePlay = PhotoImage(file="assets/Play.png").subsample(5, 5)
imageRules = PhotoImage(file="assets/Rules.png").subsample(5, 5)
imageNext = PhotoImage(file="assets/Next.png").subsample(7, 7)
monMenu = Menu(fenMenu, can, imageBg, imagePlay, imageRules, imageNext)
fenMenu.mainloop()
fenMenu.destroy()
