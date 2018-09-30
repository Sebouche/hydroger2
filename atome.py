# Créé par Baptiste Noblet, le 02/03/2016 en Python 3.2
import pygame
pygame.init()
from math import *
from projectiles import *
from random import *
from pattern import *
import constantes
#from PIL import Image

class Atome:

    def __init__(self,  posX, posY,pattern) :

        self.posX = posX
        self.posY = posY
        self.dead=False
        self.pattern=pattern
        self.dying = False
        self.explode = 0
        self.explodeCoords = [None, []]

    def reset(self):
        self.dead = False
        self.dying = False
        self.dying = 0
        self.hp = self.hpMax

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            #print("Boooom !")
            self.dying = True

    def move(self):
        """self.posX += self.mv_x
        self.posY += self.mv_y
        self.rect = self.rect.move(self.mv_x, self.mv_y)"""
        self.posX, self.posY = self.pattern.deplacer(self.posX, self.posY)
        self.rect.x = self.posX
        self.rect.y = self.posY
        if self.dying and self.explode <= 3:
            self.blowUp()
        if self.posX<-30 or self.posX>780 or self.posY<-30 or self.posY>620:
            self.dead=True

        """#TODO: ici, prendre la décision de tirer ou non.
        if self.posX+self.largeur<-50 or self.posX>constantes.largeur+50 or self.posY+self.hauteur<-50 or self.posY>constantes.hauteur+50:     #changer valeur ici aussi
            self.dead=True   #pas besoin de passer par hit, il n'y aura pas d'animation comme c'est hors de l'écran
"""

    def blowUp(self):
        #print("Ca a explosé une fois !")
        if self.explode >= 3:
            self.dead=True
        else:
            self.explodeCoords[0] = constantes.explodeList[self.explode]                     #a changer
            self.explodeCoords[1].append((self.posX,self.posY))
            self.explode += 1


    def __del__(self):
        del self

    def tir(self):
        print("Pew !")
        #Redéfinissez cette fonction dans les classes filles.


class Hydrogene(Atome):

    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=20
        self.delayTirMax=500
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/hydrogene.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.compteur = 0
        self.cible = randint ( -3,3)

    def tir(self):
        if self.delayTir<0:
            if self.compteur == 5 :
                self.delayTir=self.delayTirMax
                self.compteur = 0
                self.cible = randint ( -3,3)
            else :
                self.compteur += 1
                self.delayTir = 30
                return [Projectile(self.posX,self.posY ,self.cible/5, 0.5)]
        else:
            self.delayTir-=10
        """x1, y1 = 0, 0
        #x2, y2 = jeu.moleculeJoueur.posX,jeu.moleculeJoueur.posY
        x2,y2=200,300
        distance=sqrt(pow(x2-x1,2)+pow(y2-y1,2))
        a = float((x2-x1)/distance)
        b = float((y2-y1)/distance)
        return [Projectile(self.posX, self.posY, int(a*2), int(b*2))]"""
        return []


class Hydrogene2(Atome):

    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=20
        self.delayTirMax=100
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/hydrogene.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.cible = randint ( -3,3)

    def tir(self):
        if self.delayTir<0:
            self.delayTir = 100
            self.cible = randint ( -3,3)
            return [Projectile(self.posX,self.posY ,self.cible/5, randint(1,5)/10 )]
        else:
            self.delayTir-=10
        return []


class Carbone(Atome):

    def __init__(self, posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.tirNum = -1
        self.hp=150
        self.delayTirMax=250
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/carbone.png').convert_alpha()
        self.rect = self.img.get_rect()


    def tir(self):
        if self.delayTir<0:
            self.tirNum = -self.tirNum
            self.delayTir=self.delayTirMax
            if self.tirNum == -1:
                return [Projectile(self.posX, self.posY, -0.5, 0), Projectile(self.posX, self.posY, 0.5, 0), Projectile(self.posX, self.posY, 0, 0.25), Projectile(self.posX, self.posY, 0, -0.25)]
            elif self.tirNum == 1:
                return [Projectile(self.posX, self.posY, -0.5, -0.5), Projectile(self.posX, self.posY, 0.5, -0.5), Projectile(self.posX, self.posY, 0.25, 0.25), Projectile(self.posX, self.posY, -0.25, 0.25)]
        else:
            self.delayTir-=10
        return []



class Oxygene(Atome):

    def __init__(self, posX, posY,pattern):
        Atome.__init__(self, posX, posY,pattern)
        self.tirNum = 0
        self.hp=40
        self.delayTirMax=75
        self.delayTir=randint(0,self.delayTirMax)
        self.angle=10
        self.img = pygame.image.load('resources/photos/oxygene.png').convert_alpha()
        self.rect = self.img.get_rect()


    def tir(self):
        if self.delayTir<0:
        #self.angle = #angle entre chaques tirs
            self.tirNum += 0.02
            self.delayTir=self.delayTirMax
            return [Projectile(self.posX, self.posY, cos((self.angle*self.tirNum))*pi/5, sin((self.angle*self.tirNum))*pi/5)]
        else:
            self.delayTir-=10
        return []



class Azote(Atome):

    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=50
        self.delayTirMax=350
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/azote.png').convert_alpha()
        self.rect = self.img.get_rect()

    def tir(self):
        if self.delayTir<0:
            self.delayTir=self.delayTirMax
            return[Projectile(self.posX,self.posY, 0,0.5),Projectile(self.posX,self.posY,0.25,0.5),Projectile(self.posX,self.posY,-0.25,0.5)]
        else:
            self.delayTir-=10
        return []


class Chlore(Atome):

    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=200
        self.delayTirMax=1000
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/chlore.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.compteur = 0


    def tir(self):
        if self.delayTir<0:
        #distanceCible = int(sqrt(pow(xCible-self.x,2)+pow(yCible-self.y,2)))
        #print(distanceCible)
            if self.compteur == 30 :
                self.delayTir=self.delayTirMax
                self.compteur = 0

            else :
                self.cible = randint ( -3,3)
                self.compteur += 1
                self.delayTir = 1
                return [Projectile(self.posX,self.posY ,self.cible/100, 0.15 )]
        else:
            self.delayTir-=10
        return []


class Soufre(Atome):

    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=500
        self.delayTirMax=1000
        self.delayTir=100
        self.img = pygame.image.load('resources/photos/soufre.png').convert_alpha()
        self.rect = self.img.get_rect()

    def tir(self):
        if self.delayTir<0:
            self.delayTir=self.delayTirMax
            return [Laser(self.posX,self.posY, 0,1,0,1),Laser(self.posX,self.posY,0.5,0.5,45,1),Laser(self.posX,self.posY,-0.5,0.5,-45,1)]
        else:
            self.delayTir-=10
        return []



class Uranium(Atome):

    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=200
        self.delayTirMax=1000
        self.delayTir=100
        self.img = pygame.image.load('resources/photos/uranium.png').convert_alpha()
        self.rect = self.img.get_rect()

    def tir(self):
        if self.delayTir<0:
            self.delayTir=self.delayTirMax
            return [Laser2(self.posX,self.posY, 0,1,0,2),Laser2(self.posX,self.posY,0.5,0.5,45,2),Laser2(self.posX,self.posY,-0.5,0.5,-45,2)]
        else:
            self.delayTir-=10
        return []

class Uranium2(Atome):

    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=250
        self.delayTirMax=100
        self.delayTir=100
        self.img = pygame.image.load('resources/photos/uranium.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.compteur=10

    def tir(self):
        if self.delayTir<0:
            if self.compteur<=30:
                self.delayTir=30
                self.compteur+=1
                return [Projectile(self.posX,self.posY, (uniform(-3,3)*(self.compteur/10))/8,(uniform(1,3)*(self.compteur/10))/8)]
            else:
                self.compteur=10
        else:
            self.delayTir-=10
        return []
class Boson(Atome):

    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=5000
        self.delayTirMax=100
        self.delayTir=1
        self.img = pygame.image.load('resources/photos/boson.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.attaque = 0
        self.tirprojectiles= 0
        self.tirlasers= 0
        self.tirbashp= 0

    def tir(self):
        if self.delayTir<0:
            self.attaque = randint(1,5)
            if self.attaque == 1 and self.tirprojectiles==0 and self.tirlasers==0 and self.tirbashp==0:
                self.delayTir = self.delayTirMax
                return [Laser(self.posX,self.posY, 0,1,0,2),Laser(self.posX,self.posY,0.5,0.5,45,2),Laser(self.posX,self.posY,-0.5,0.5,45,2),Laser(self.posX,self.posY, -0.5,-0.5,0,2),Laser(self.posX,self.posY,0.5,-0.5,45,2),Laser(self.posX,self.posY,0,-1,45,2),Laser(self.posX,self.posY, 1,0,0,2),Laser(self.posX,self.posY,-1,0,45,2)]
            elif (self.attaque == 2 or self.tirprojectiles>0) and self.tirlasers==0 and self.tirbashp==0:
                if self.tirprojectiles<50:
                    directiontir = randint(-100,100)
                    self.tirprojectiles += 1
                    self.delayTir = 1
                    return [Projectile(self.posX,self.posY,directiontir/100,1)]
                elif self.tirprojectiles>=50:
                    self.delayTir = 200
                    self.tirprojectiles = 0
                return []
            elif (self.attaque == 3 or self.tirlasers>0) and self.tirprojectiles==0 and self.tirbashp==0:
                if self.tirlasers<10:
                    directiontir = randint(-100,100)
                    self.tirlasers += 1
                    self.delayTir = 1
                    return [Laser(self.posX,self.posY,directiontir/100,1,45,2)]
                elif self.tirlasers>=10:
                    self.delayTir = 1000
                    self.tirlasers = 0
                return []
            elif self.attaque == 4 and self.tirprojectiles==0 and self.tirlasers==0 and self.tirbashp==0:
                self.delayTir= 500
                return []
            elif (self.attaque == 5 or self.tirbashp>0) and self.tirprojectiles==0 and self.tirlasers==0:
                if self.tirbashp<500:
                    directiontir = randint(-20,20)
                    self.tirbashp += 1
                    self.delayTir = 1
                    return [Projectile(self.posX,self.posY,directiontir/100,0.1)]
                elif self.tirbashp>=500:
                    self.delayTir= self.delayTirMax
                    self.tirbashp=0
                return []
        else:
            self.delayTir-=10
        return []

class Diamant(Atome):
    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=10000
        self.delayTirMax=1000
        self.delayTir=1
        self.img = pygame.image.load('resources/photos/diamant.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.compteur=0
        self.tirs=0
    def tir(self):
        if self.compteur==100 and self.hp>9000:
            self.compteur=0
            return[Projectile(350,200,0, 0.6 ),Projectile(375,200,0, 0.6 ),Projectile(400,200,0, 0.6 ),Projectile(425,200,0, 0.6 ),Projectile(450,200,0, 0.6 )]
        elif self.delayTir<=0:
            projectile=[]
            if self.hp>9000 and self.hp<=10000:
                for i in range(0,768,48):
                    x=i
                    y=100
                    projectile.append(Projectile(x,y,0, 0.3 ))
                self.delayTir=300
                return projectile
            if self.hp>5000 and self.hp<=9000:
                for j in range(0,-2,-1):
                    espace=randint(12,22)
                    if self.hp>5000 and self.hp<=9000:
                        for i in range(0,600,25):
                            if espace*25==i:
                                projectile.append(Projectile(999,999,0, 0.3 ))
                            else :
                                x=j*-768
                                y=i
                                if j==0:
                                    projectile.append(Projectile(x,y,0.3, 0 ))
                                else:
                                    projectile.append(Projectile(x,y,-0.3, 0 ))
                self.delayTir=300
                if self.hp>5000 and self.hp<=7000:
                    for j in range(0,-2,-1):
                        for i in range(32,720,16):
                            x=i
                            y=j*-600
                            if j==0:
                                projectile.append(Projectile(x,y,0, 0.1 ))
                            else:
                                projectile.append(Projectile(x,y,0, -0.1 ))
                    self.delayTir+=400
                return projectile
            if self.hp>3000 and self.hp<=5000:
                for i in range(30):
                    directiontir = randint(-80,80)
                    projectile.append(Projectile(self.posX+100,self.posY+100,directiontir/100,0.8))
                self.delayTir=100
                return projectile
            if self.hp<=3000:
                if self.tirs<100:
                    directiontir = randint(-100,100)
                    delayTir=6
                    self.tirs+=1
                    return [Projectile(self.posX+100,self.posY+100,directiontir/100,0.6)]
                else:
                    self.tirs=0
                    self.delayTir=100
        else:
            self.delayTir-=1
            self.compteur+=1
        return []



class Plutonium(Atome):
    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,posX,posY,pattern)
        self.hp=11000
        self.delayTirMax=1000
        self.delayTir=1
        self.img = pygame.image.load('resources/photos/plutonium.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.tirNum=0
        self.angle=10
        self.compteur=0
        self.ancienposX=self.posX
        self.ancienposY=self.posY
        self.a=0
        self.b=0
        self.cote=1
        self.compteur2=0
    def tir(self):
        if self.delayTir<=0:
            if self.hp>9000 and self.hp<=11000:
                if self.compteur<3:
                    self.compteur+=1
                    renvoi=[]
                    for i in range(40):
                        self.tirNum += 0.02
                        renvoi.append(Matiere(self.posX, self.posY, cos((self.angle*self.tirNum))*pi/4, sin((self.angle*self.tirNum))*pi/4,0))
                    self.tirNum=0
                    self.delayTir=100
                    return renvoi
                else:
                    self.angle=randint(10,80)
                    self.compteur=0
                    self.delayTir=500
            if self.hp>8000 and self.hp<=9000:
                if (abs(self.posX-self.ancienposX)>=3 and abs(self.posY-self.ancienposY)>=3):
                    self.pattern=Pattern(self.a*3,self.b*3)
                    self.compteur+=1
                    if self.compteur>=40:
                        return [Matiere(self.posX, self.posY,0,0,1)]
                        self.compteur=0
                else:
                    self.pattern=Pattern(0,0)
                    self.ancienposX=constantes.positionx
                    self.ancienposY=constantes.positiony
                    distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                    self.a = (float((self.ancienposX-self.posX)/distance))*2
                    self.b = (float((self.ancienposY-self.posY)/distance))*2
                    self.delayTir=300
                    return [Matiere(self.posX, self.posY, self.a/2.5, self.b/2.5,2)]
            if self.hp>6000 and self.hp<=8000:
                if (abs(self.posX-384)>=3 and abs(self.posY-50)>=3):
                    directionX=384
                    directionY=50
                    distance=sqrt(pow(directionX-self.posX,2)+pow(directionY-self.posY,2))
                    self.a = (float((directionX-self.posX)/distance))*2
                    self.b = (float((directionY-self.posY)/distance))*2
                    self.pattern=Pattern(self.a*3,self.b*3)
                else:
                    self.pattern=Pattern(0,0)
                    if self.compteur<20:
                        directiontir = randint(-100,100)
                        self.compteur += 1
                        self.delayTir = 40
                        return [Matiere(self.posX,self.posY,directiontir/100,1,2)]
                    elif self.compteur>=20:
                        self.delayTir = 400
                        self.compteur = 0
            if self.hp>4000 and self.hp<=6000:
                self.ancienposX=constantes.positionx
                self.ancienposY=constantes.positiony
                distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                self.a = (float((self.ancienposX-self.posX)/distance))*2
                self.b = (float((self.ancienposY-self.posY)/distance))*2
                self.delayTir=70
                return [Matiere(self.posX, self.posY,self.a/2,self.b/2,0)]
            if self.hp>3000 and self.hp<=4000:
                self.ancienposX=constantes.positionx
                self.ancienposY=constantes.positiony
                distance1=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                self.a = (float((self.ancienposX-self.posX)/distance1))*2
                self.b = (float((self.ancienposY-self.posY)/distance1))*2
                distance2=sqrt(pow(self.ancienposX-(self.posX+40),2)+pow(self.ancienposY-(self.posY+40),2))
                self.c = (float((self.ancienposX-(self.posX+40))/distance2))*2
                self.d = (float((self.ancienposY-(self.posY))/distance2))*2
                self.delayTir=70
                return [Matiere(self.posX, self.posY,self.a/2.5,self.b/2.5,0),Matiere(self.posX+40, self.posY+40,self.c/2,self.d/2,0)]
            if self.hp>0 and self.hp<=3000:
                r=[]
                if self.compteur==10:
                    for i in range(0,20):
                        r.append(Matiere(self.posX,self.posY,cos(pi*i/20)*0.6,sin(pi*i/20)*0.6,1))
                if self.compteur<20:
                    if self.cote%2!=0:
                        if self.cote==1:
                            distance=sqrt(pow(constantes.positionx-20,2)+pow(constantes.positiony-(100+self.compteur*20),2))
                            a = (float((constantes.positionx-20)/distance))*2
                            b = (float((constantes.positiony-(100+self.compteur*20))/distance))*2
                            p=Projectile(20,100+self.compteur*20,1,1,PatternComplexe([[Pattern(0,0),30],[Pattern(a*2.5,b*2.5),1]]))
                            p.img=pygame.image.load("resources/photos/photon_vert.png")
                        else:
                            distance=sqrt(pow(constantes.positionx-748,2)+pow(constantes.positiony-(100+self.compteur*20),2))
                            a = (float((constantes.positionx-748)/distance))*2
                            b = (float((constantes.positiony-(100+self.compteur*20))/distance))*2
                            p=Projectile(748,100+self.compteur*20,1,1,PatternComplexe([[Pattern(0,0),30],[Pattern(a*2.5,b*2.5),1]]))
                            p.img=pygame.image.load("resources/photos/photon_vert.png")
                    else:
                        if self.cote==2:
                            distance=sqrt(pow(constantes.positionx-(128+self.compteur*25.6),2)+pow(constantes.positiony-15,2))
                            a = (float((constantes.positionx-(128+self.compteur*25.6))/distance))*2
                            b = (float((constantes.positiony-15)/distance))*2
                            p=Projectile(128+self.compteur*25.6,15,1,1,PatternComplexe([[Pattern(0,0),30],[Pattern(a*2.5,b*2.5),1]]))
                            p.img=pygame.image.load("resources/photos/photon_violet.png")
                        else:
                            distance=sqrt(pow(constantes.positionx-(128+self.compteur*25.6),2)+pow(constantes.positiony-585,2))
                            a = (float((constantes.positionx-(128+self.compteur*25.6))/distance))*2
                            b = (float((constantes.positiony-585)/distance))*2
                            p=Projectile(128+self.compteur*25.6,585,1,1,PatternComplexe([[Pattern(0,0),30],[Pattern(a*2.5,b*2.5),1]]))
                            p.img=pygame.image.load("resources/photos/photon_violet.png")
                    self.delayTir=50
                    self.compteur+=1
                    r.append(p)
                    if self.hp>0 and self.hp<=1000:
                        if self.compteur2<5 and self.compteur2>=0:
                            self.ancienposX=constantes.positionx
                            self.ancienposY=constantes.positiony
                            distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                            self.a = (float((self.ancienposX-self.posX)/distance))*2
                            self.b = (float((self.ancienposY-self.posY)/distance))*2
                            r.append(Matiere(self.posX, self.posY, self.a/2, self.b/2,1))
                            self.compteur2+=1
                        elif self.compteur2<0:
                            self.compteur2+=1
                        else:
                            self.compteur2=-10
                    return r

                else:
                    self.compteur=0
                    self.cote=(self.cote+1)%4
        else:
            self.delayTir-=10
        return []


class Plutonium2(Atome):
    def __init__(self,posX,posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=10000
        self.img = pygame.image.load('resources/photos/plutonium.png').convert_alpha()
        self.rect = self.img.get_rect()

class AntiHydrogene(Hydrogene):

    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=80
        self.delayTirMax=100
        self.compteur=0
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/anti_hydrogene.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.cible = randint ( -3,3)


    def tir(self):
        if self.delayTir<0:
                self.cible = randint ( -3,3)
                self.delayTir = 200
                return [Antiprojectile(self.posX,self.posY ,self.cible/5, 0.5 )]
        else:
            self.delayTir-=10
        return []




class AntiAzote(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=200
        self.delayTirMax=100
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/anti_azote.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.ancienposX=self.posX
        self.ancienposY=self.posY


    def tir(self):
        if self.delayTir<0:
            self.ancienposX=constantes.positionx
            self.ancienposY=constantes.positiony
            distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
            self.a = (float((self.ancienposX-self.posX)/distance))*2
            self.b = (float((self.ancienposY-self.posY)/distance))*2
            self.delayTir=50
            return [Scatter(self.posX, self.posY, self.a/4, self.b/4)]
        else:
            self.delayTir-=1
        return []


class AntiOxygene(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=160
        self.delayTirMax=100
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/anti_oxygene.png').convert_alpha()
        self.rect = self.img.get_rect()
    def tir(self):
        if self.delayTir<0:
            proj=[]
            for i in range(-1,3,2):
                for j in range(-1,3,2):
                    proj.append(Antiprojectile(self.posX,self.posY,i,j))
            self.delayTir=100
            return proj
        else:
            self.delayTir-=1
        return []


class AntiCarbone(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=400
        self.delayTirMax=100
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/anti_carbone.png').convert_alpha()
        self.rect = self.img.get_rect()
    def tir(self):
        if self.delayTir<0:
            proj=[]
            proj.append(Antiprojectile(self.posX,self.posY,0,0,PatternPolynome(randint(1,2)/1000,randint(1,2)/1000,randrange(-1,1,2))))
            self.delayTir=20
            return proj
        else:
            self.delayTir-=1
        return []


class Methane(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=400
        self.delayTirMax=100
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/methane.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.ancienposX=self.posX
        self.ancienposY=self.posY
    def tir(self):
        if self.delayTir<0:
            self.ancienposX=constantes.positionx
            self.ancienposY=constantes.positiony
            distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
            self.a = (float((self.ancienposX-self.posX)/distance))*2
            self.b = (float((self.ancienposY-self.posY)/distance))*2
            self.delayTir=60
            proj=[]
            y=atan(self.b/(self.a+0.00001))-pi/2
            for i in range(1,11):
                if self.posX<=self.ancienposX:
                    x=y+(pi/10)*i
                else:
                    x=y-(pi/10)*i
                proj.append(Projectile(self.posX+35*cos(x),self.posY+35*sin(x),self.a/2,self.b/2))
            return proj
        else:
            self.delayTir-=1
        return []


class H20(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=1000
        self.delayTirMax=100
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/Eau.png').convert_alpha()
        self.rect = self.img.get_rect()

    def tir(self):
        if self.delayTir<0:
            proj=[]
            for i in range(30):
                x=uniform(-3,3)/2
                y=uniform(1,3)/2
                proj.append(Projectile(self.posX,self.posY,x,y))
            self.delayTir=70
            return proj
        else:
            self.delayTir-=1
        return []





class AntiHiggs(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=15000
        self.delayTirMax=30
        self.delayTir=randint(0,self.delayTirMax)
        self.img = pygame.image.load('resources/photos/anti_higgs1.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.ancienposX=self.posX
        self.ancienposY=self.posY
        self.compteur = 1
        self.compteur2 = 0
        self.sens = 1
        self.e=uniform(-1,1)
        self.g=randint(-100,100)
        self.f=randint(1,100)
        self.direction=1

    def tir(self):
        proj=[]
        if self.delayTir<0:
            if self.hp>13000 and self.hp<=15000:
                if self.compteur2<25:
                    self.compteur2+=1
                #self.compteur = self.compteur+self.sens*0.1
                    b=Projectile(self.posX,self.posY,0, 0,PatternSinusoidalAmplifie(self.posX,self.posY,20,3*self.e,2,0))
                    b.img=constantes.projectilesList[2].convert_alpha()
                    c=Projectile(self.posX,self.posY,0, 0,PatternSinusoidalAmplifie(self.posX,self.posY,20,3*self.g/100,2,0))
                    c.img=constantes.projectilesList[2].convert_alpha()
                    proj.append(b)
                    proj.append(c)
                else :
                    self.e=uniform(-1,1)
                    self.g=randint(-100,100)
                    self.f=randint(1,100)
                    self.delayTir = 5
                    self.compteur+=1
                    self.compteur2=0
                    if self.f<=50:
                        a=randint(-100,100)/100
                        proj.append(Laser(self.posX,self.posY,a,1,asin(a/sqrt(a*a+1))/pi*180,3))
            elif self.hp>11000 and self.hp<=13000:
                self.compteur+=self.sens
                b=Projectile(self.posX,self.posY,0, 0,PatternSinusoidalAmplifie(self.posX,self.posY,20,self.compteur/10,15,self.compteur/10))
                b.img=constantes.projectilesList[4].convert_alpha()
                c=Projectile(self.posX,self.posY,0, 0,PatternSinusoidalAmplifie(self.posX,self.posY,20,15+self.compteur/10,15+self.compteur,self.compteur/10))
                c.img=constantes.projectilesList[4].convert_alpha()
                d=Projectile(self.posX,self.posY,0, 0,PatternSinusoidalAmplifie(self.posX,self.posY,20,-15+self.compteur/10,15+self.compteur,self.compteur/10))
                d.img=constantes.projectilesList[4].convert_alpha()
                proj.append(b)
                proj.append(c)
                proj.append(d)
                if abs(self.compteur)>=100:
                    self.sens=-self.sens
            elif self.hp>9000 and self.hp<=11000:
                if self.compteur== 120:
                    self.delayTir=100
                    self.compteur = 0
                    self.compteur2+=1
                    self.sens=-self.sens
                    self.direction=(self.direction+1)%4
                else :
                    self.compteur+=1
                    self.delayTir = 0
                    if self.direction//2==0:
                        proj=Projectile(self.compteur2%2*30+self.compteur//12*60,self.compteur2%2*30+self.compteur%10*60,0,0,PatternComplexe([[Pattern(0,0),120-self.compteur],[PatternSinusoidalAmplifie(self.compteur2%2*30+self.compteur//12*60,self.compteur2%2*30+self.compteur%10*60,5,self.sens*2,0,0),1]]))
                    else:
                        proj=Projectile(self.compteur2%2*30+self.compteur//12*60,self.compteur2%2*30+self.compteur%10*60,0,0,PatternComplexe([[Pattern(0,0),120-self.compteur],[PatternSinusoidalAmplifie(self.compteur2%2*30+self.compteur//12*60,self.compteur2%2*30+self.compteur%10*60,5,0,self.sens*2,0),1]]))
                    if self.compteur2%2==0:
                        proj.img = constantes.projectilesList[1].convert_alpha()
                    else:
                        proj.img = constantes.projectilesList[7].convert_alpha()
                    return [proj]
            elif self.hp>7000 and self.hp<=9000:
                a=Projectile(self.posX+50,self.posY,0,0,Patternaccelere(uniform(-1,1),uniform(-1,1),0.01))
                a.img=constantes.projectilesList[1].convert_alpha()
                b=Projectile(self.posX-50,self.posY,0,0,Patternaccelere(uniform(-1,1),uniform(-1,1),0.01))
                b.img=constantes.projectilesList[7].convert_alpha()
                proj.append(a)
                proj.append(b)
        else:
            self.delayTir-=1
        return proj




        """if self.delayTir<-100000000000:
            self.ancienposX=constantes.positionx
            self.ancienposY=constantes.positiony
            distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
            self.a = (float((self.ancienposX-self.posX)/distance))*2
            self.b = (float((self.ancienposY-self.posY)/distance))*2
            self.delayTir=60
            proj=[]
            y=atan(self.b/(self.a+0.00001))-pi/2
            print(y)
            for i in range(1,11):
                if self.posX<=self.ancienposX:
                    x=y+(pi/10)*i
                else:
                    x=y-(pi/10)*i
                proj.append(Projectile(self.posX+35*cos(x),self.posY+35*sin(x),self.a/2,self.b/2))
            return proj"""


class Faille(Atome):
    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=20000
        self.delayTirMax=500
        self.delayTir=20
        self.img = pygame.image.load('resources/photos/faille.png').convert_alpha()
        self.rect = self.img.get_rect()
    def tir(self):
        if self.delayTir<0:
            self.delayTir = 1
            self.cible = randint ( -3,3)
            if randint(0,10)==10:
                return [Antiprojectile(self.posX+randint(0,398),self.posY+50+randint(0,20) ,self.cible/5, randint(1,5)/10 )]
            return [Projectile(self.posX+randint(0,398),self.posY+50+randint(0,20) ,self.cible/5, randint(1,5)/10 )]
        else:
            self.delayTir-=1
        return []

class AntiRoger(Atome):

    def __init__(self , posX, posY,pattern):
        Atome.__init__(self,  posX, posY,pattern)
        self.hp=2000
        self.hptemp=2000
        self.delayTirMax=500
        self.delayTir=20
        self.img = pygame.image.load('resources/photos/antiroger.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.ancienposX=constantes.positionx
        self.ancienposY=constantes.positiony
        distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
        self.a = (float((self.ancienposX-self.posX)/distance))*2
        self.b = (float((self.ancienposY-self.posY)/distance))*2
        self.compteur=0
        self.fin=True

    def tir(self):
        proj=[]
        if self.delayTir<0:
            if self.hp>1800 and self.hp<=2000:
                a=randint(-1,0)
                direction=1
                if a==-1:
                    direction=a
                b=Projectile(randint(1,767),-a*595,0,direction*uniform(0.3,1))
                b.img=pygame.image.load('resources/photos/antiphoton2.png').convert_alpha()
                proj.append(b)
                self.delayTir=3
            if self.hp>1600 and self.hp<=1800:
                if abs(self.posX-self.ancienposX)>=3 and self.fin==True:
                    self.pattern=Pattern(self.a*3,0)
                else:
                    self.fin=False
                    if self.compteur<=40:
                        self.pattern=Pattern(0,0)
                        for i in range(2):
                            a=Projectile(self.posX,self.posY+15*self.compteur,0,0,PatternComplexe([[Pattern(0,0),100-self.compteur],[Pattern(uniform(-1,1)*2,uniform(-1,1)*2),1]]))
                            a.img=pygame.image.load('resources/photos/antiphoton2.png').convert_alpha()
                            proj.append(a)
                        self.compteur+=1
                    else:
                        self.compteur=0
                        self.delayTir=80
                        self.fin=True
                        self.ancienposX=constantes.positionx
                        self.ancienposY=constantes.positiony
                        distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                        self.a = (float((self.ancienposX-self.posX)/distance))*2
                        self.b = (float((self.ancienposY-self.posY)/distance))*2
        else :
            self.delayTir-=1
        if self.hp!=self.hptemp:
            self.hptemp=self.hp
            proj.append(Antiprojectile(self.posX,self.posY,uniform( -3,3)/5,0.5))
        return proj