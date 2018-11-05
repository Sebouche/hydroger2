import pygame
import constantes


"""
    Attributs à initialiser :
    Pattern
    Pattern de tir
"""


class entite:
    """Classe qui gère les molecules, atomes, et autres entités qui tirent des
    projectiles dans le jeu"""

    def __init__(self, x, y, name):
        self.posX = x
        self.posY = y
        self.dead = False
        self.dying = False
        self.explode = 0
        # self.img = pygame.image.load('resources/photos/' + str(name) + '.png').convert_alpha()
        # self.rect = self.img.get_rect()
        self.hpMax, self.delayTirMax = entite.loadStats(name)
        self.hp = self.hpMax
        self.delayTir = 0
        print("hp : " + str(self.hp) + " delayTirMax : " + str(self.delayTirMax))
        """TODO : chercher les infos supplémentaires dans le fichier adéquat.
            (fonction faite pour)"""

    """ Fonctions de atome """

    def reset(self):
        self.dead = False
        self.dying = False
        self.hp = self.hpMax

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:  # BOOM !
            self.dying = True

    def move(self):
        self.posX, self.posY = self.pattern.deplacer(self.posX, self.posY)
        self.rect.x = self.posX
        self.rect.y = self.posY
        if self.dying and self.explode <= 3:
            self.blowUp()
        if self.posX < -30 or self.posX > 780 or self.posY < -30 or self.posY > 620:
            self.dead = True

    def blowUp(self):
        if self.explode >= 3:
            self.dead = True
        else:  # A changer ?
            self.explodeCoords[0] = constantes.explodeList[self.explode]
            self.explodeCoords[1].append((self.posX, self.posY))
            self.explode += 1

    def __del__(self):
        del self

    def tir(self):
        print("Pew !")
        # Utiliser le pattern de tir pour tirer.

    def loadStats(name):
        with open('resources/entites/' + str(name) + '.txt', 'r') as file:
            stats = file.readlines()
            return int(stats[0]), int(stats[1])
