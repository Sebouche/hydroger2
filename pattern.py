# Créé par Pierre, le 06/04/2016 en Python 3.2
#kek
from math import *
from random import *
import constantes
"""utiliser un tuple pour donner les arguments dans le constructeur est bcp plus simple pour créer le pattern"""
class Pattern:
    """La classe pattern dont tous les pattern doivent hériter."""
    def __init__(self, mv_x,mv_y):
        self.mv_x = mv_x
        self.mv_y = mv_y

    def deplacer(self, posX, posY):
        """La fonction deplace doit retourner x et y."""
        posX += self.mv_x
        posY += self.mv_y
        return posX, posY


class Patternaccelere(Pattern):

    def __init__(self, mv_x,mv_y,acceleration):
        self.mv_x = mv_x
        self.mv_y = mv_y
        self.acceleration=acceleration


    def deplacer(self, posX, posY):
        """La fonction deplace doit retourner x et y."""
        posX += self.mv_x
        posY += self.mv_y
        self.mv_x=self.mv_x*(1+self.acceleration)
        self.mv_y=self.mv_y*(1+self.acceleration)
        return posX, posY



class PatternPolynome(Pattern):
    """Pattern qui fait se déplacer selon un polynome du second degré."""
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = abs(c)  #je pense pas qu'on aura une ordonnée à l'origine en dehors de l'écran
        if c == abs(c):# le signe de c donne la direction de x
            self.dir = 1
        else:
            self.dir = -1

    def deplacer(self, posX, posY):
        posX += self.dir-constantes.largeur/2
        posY = self.a * posX * posX + self.b * posX + self.c
        return posX+constantes.largeur/2, posY

class PatternCercle(Pattern):
    """Pattern qui fait se déplacer selon un cercle au milieu de l'écran"""
    def __init__(self,centreX,centreY,rayon,angle,vitesse):
        self.centreX=centreX
        self.centreY=centreY
        self.rayon=rayon
        self.angle=angle
        self.vitesse=vitesse/180*pi #en degrés par mouvement et négatif pour tourner dans l'autre sens

    def deplacer(self,posX,posY):
        posX=self.centreX+self.rayon*(cos(self.angle))
        posY=self.centreY+self.rayon*(sin(self.angle))
        self.angle+=self.vitesse
        return posX,posY

class PatternZigZag(Pattern):#je ne suis pas sûr de la syntaxe pour ce pattern
    def __init__(self,Xini,Yini,direction,amplitude):
        self.direction=direction
        self.amplitude=amplitude
        self.mouvement=False
        self.Xini=Xini
        self.Yini=Yini
    def deplacer(self,posX,posY):
        if posY<self.amplitude+self.Yini and self.mouvement==False:
            self.mv_x=self.direction
            self.mv_y=self.direction*self.direction
        else:
            self.mouvement=True
            if posY>self.direction*self.direction*-self.amplitude+self.Yini:
                self.mv_x=self.direction
                self.mv_y=-self.direction*self.direction
            else :
                self.mouvement=False
        posX+=self.mv_x
        posY+=self.mv_y
        return posX,posY




class PatternSinusoidalAmplifie(Pattern):
    def __init__(self,posX,posY,amplitude,dirX,dirY,vitesse):
        self.dirX=dirX
        self.dirY=dirY
        self.vitesse=vitesse
        self.amplitude=amplitude
        self.hyp=sqrt(self.dirX*self.dirX+self.dirY*self.dirY)
        self.angle=acos(self.dirX/self.hyp)
        self.dirU=cos(self.angle)*self.dirX+sin(self.angle)*self.dirY
        self.dirV=cos(self.angle)*self.dirY-sin(self.angle)*self.dirX
        self.Uini=cos(self.angle)*posX+sin(self.angle)*posY
        self.U=self.Uini
        self.V=cos(self.angle)*posY-sin(self.angle)*posX


    def deplacer(self,posX,posY):
        self.U=self.U+self.dirU
        V=self.V+self.amplitude *sin((self.U-self.Uini)/self.dirU/3)
        posX = cos(self.angle)*(self.U)-sin(self.angle)*V
        posY = sin(self.angle)*(self.U)+cos(self.angle)*V
        self.amplitude+=self.vitesse
        return posX,posY



class PatternCibler(Pattern):
    def __init__(self,posX,posY):
        self.cibleX=posX
        self.cibleY=posY

    def deplacer(self,posX,posY):
        if (abs(posX-self.cibleX)>=5 or abs(posY-self.cibleY)>=5):
            distance=sqrt(pow(self.cibleX-posX,2)+pow(self.cibleY-posY,2))
            self.a = (float((self.cibleX-posX)/distance))*2
            self.b = (float((self.cibleY-posY)/distance))*2
            posX+=self.a
            posY+=self.b
            return posX,posY
        else :
            return posX,posY


class PatternComplexe(Pattern):
    def __init__(self,Patterns):
        self.Patterns=Patterns
        self.rang=0
        self.time=0

    def deplacer(self,posX,posY):
        if self.rang<len(self.Patterns)-1:
            if self.time>self.Patterns[self.rang][1]:
                self.rang+=1
                self.time=0
        pattern=self.Patterns[self.rang][0]
        posX,posY=pattern.deplacer(posX,posY)
        self.time+=1
        return posX,posY