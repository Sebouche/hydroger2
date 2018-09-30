# Créé par Pierre, le 03/03/2016 en Python 3.2
from math import *
import constantes
from random import *
import pygame
import pickle
import pattern

class Projectile:
    """Classe des projectiles tirés par les atomes."""

    def __init__(self, posX, posY, mv_x, mv_y,patterne=0):
        """Constructeur 'tout simple'..."""
        self.posX = posX
        self.posY = posY
        self.mv_x = mv_x*8
        self.mv_y = mv_y*8
        self.patterne=patterne
        self.dead=False
        self.indice=3
        self.anti=False
        self.colli=False
        self.img = constantes.projectilesList[randint(1,7)].convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.degats = 1

    def __del__(self):
        del self

    def move(self):
        if self.patterne==0:
            self.posX += self.mv_x
            self.posY += self.mv_y
        else:
            self.posX,self.posY=self.patterne.deplacer(self.posX,self.posY)
        self.rect.x = self.posX
        self.rect.y = self.posY
        #self.rect.move_ip(self.mv_x, self.mv_y) #On fait bouger le rectangle !
        if self.posY<-20 or self.posY>constantes.hauteur+20 or self.posX<-20 or self.posX>constantes.largeur+20:
            self.dead=True

class Matiere:

    def __init__(self, posX, posY, mv_x, mv_y,etat):
        self.etat=etat
        self.posX = posX
        self.posY = posY
        self.mv_x = mv_x*8
        self.mv_y = mv_y*8
        self.dead=False
        self.indice=4
        self.anti=False
        self.colli=False
        self.img = pygame.image.load('resources/photos/matiere_noire.png').convert_alpha()
        if self.etat==2:
            self.img = pygame.image.load('resources/photos/matiere_noire2.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.degats = 2
        self.fin=0

    def __del__(self):
        del self

    def move(self):
        self.posX += self.mv_x
        self.posY += self.mv_y
        self.rect.x = self.posX
        self.rect.y = self.posY
        if self.etat==1:
            self.fin+=1
        if self.fin==400:
            self.dead=True
        if self.posY<-20 or self.posY>constantes.hauteur+20 or self.posX<-20 or self.posX>constantes.largeur+20:
            self.dead=True


class Antiprojectile(Projectile):
    def __init__(self, posX, posY, mv_x, mv_y,patterne=0):
        Projectile.__init__(self, posX, posY, mv_x, mv_y,patterne)
        self.anti=True
        self.colli=False
        self.indice=5
        self.img = pygame.image.load('resources/photos/antiphoton.png').convert_alpha()
        self.degats = 1
        self.boom=[]
    def move(self):
        Projectile.move(self)
        if self.posY<=0 or self.posY>=constantes.hauteur-15 or self.posX<=0 or self.posX>=constantes.largeur-15:
            self.dead=True
            self.boom=[Projectile(self.posX, self.posY, randint(1,3)/4,randint(-3,-1)/4), Projectile(self.posX, self.posY,randint(1,3)/4,randint(1,3)/4), Projectile(self.posX, self.posY,randint(-3,-1)/4,randint(1,3)/4), Projectile(self.posX, self.posY,randint(-3,-1)/4,randint(-3,-1)/4)]


class Scatter(Projectile):
    def __init__(self, posX, posY, mv_x, mv_y):
        Projectile.__init__(self, posX, posY, mv_x, mv_y)
        self.indice=666
        self.anti=True
        self.colli=False
        self.img = pygame.image.load('resources/photos/scatterphoton.png').convert_alpha()
        self.degats = 3
        self.boom=[]
    def move(self):
        Projectile.move(self)
        if self.colli==True:
            self.boom=[Antiprojectile(self.posX, self.posY, randint(1,3)/4,randint(-3,-1)/4), Antiprojectile(self.posX, self.posY,randint(1,3)/4,randint(1,3)/4), Antiprojectile(self.posX, self.posY,randint(-3,-1)/4,randint(1,3)/4)]
        elif self.posY<=0 or self.posY>=constantes.hauteur-15 or self.posX<=0 or self.posX>=constantes.largeur-15:
            self.dead=True
            self.boom=[Projectile(self.posX, self.posY, randint(1,3)/4,randint(-3,-1)/4), Projectile(self.posX, self.posY,randint(1,3)/4,randint(1,3)/4), Projectile(self.posX, self.posY,randint(-3,-1)/4,randint(1,3)/4), Projectile(self.posX, self.posY,randint(-3,-1)/4,randint(-3,-1)/4)]

class Laser:

    def __init__(self, posX, posY, mv_x, mv_y,rtImg,rebond):
        self.posX = posX
        self.posY = posY
        self.mv_x = mv_x*6
        self.mv_y = mv_y*6
        self.rtImg = rtImg
        self.rebond = rebond
        self.dead=False
        self.anti=False
        self.indice=9
        self.colli=False
        self.degats = 1
        self.imgrt= constantes.laser.convert_alpha()
        self.img= pygame.transform.rotate(self.imgrt,self.rtImg)
        self.rect = self.img.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def __del__(self):
        del self

    def move(self):
        self.posX += self.mv_x
        self.posY += self.mv_y
        self.rect.x = self.posX
        self.rect.y = self.posY
        if self.posX<=0 or self.posX>=constantes.largeur and self.rebond<5:
            self.rebond += 1
            self.mv_x = -self.mv_x
            self.mv_y = self.mv_y
            self.rtImg =-(abs(self.mv_x)/(self.mv_x+0.00001))*90
            if self.mv_y==0:
                self.rtImg=180
            self.img= pygame.transform.rotate(self.img,self.rtImg)
            self.rect = self.img.get_rect()
        if self.posY<=0 or self.posY>=constantes.hauteur and self.rebond<5:
            self.rebond = self.rebond+1
            self.mv_x=self.mv_x
            self.mv_y=-self.mv_y
            self.rtImg = -(abs(self.mv_y)/self.mv_y)*90
            if self.mv_x==0:
                self.rtImg=180
            self.img= pygame.transform.rotate(self.img,self.rtImg)
            self.rect = self.img.get_rect()
        if self.posY<-20 or self.posY>constantes.hauteur+20 or self.posX<-20 or self.posX>constantes.largeur+20:
                self.dead=True

class Laser2:

    def __init__(self, posX, posY, mv_x, mv_y,rtImg,tp):
        self.posX = posX
        self.posY = posY
        self.mv_x = mv_x*6
        self.mv_y = mv_y*6
        self.rtImg = rtImg
        self.tp = tp
        self.dead=False
        self.colli=False
        self.indice=10
        self.anti=False
        self.degats = 1
        self.imgrt= constantes.laser2.convert_alpha()
        self.img= pygame.transform.rotate(self.imgrt,self.rtImg)
        self.rect = self.img.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def __del__(self):
        del self

    def move(self):
        self.posX += self.mv_x
        self.posY += self.mv_y
        self.rect.x = self.posX
        self.rect.y = self.posY
        if self.posX<=0 or self.posX>=constantes.largeur and self.tp<5:
            self.tp += 1
            self.posX= constantes.largeur-self.posX
            self.mv_x = self.mv_x*1.2
            self.mv_y = self.mv_y*1.2
            self.posX =self.posX
        if self.posY<=0 or self.posY>=constantes.hauteur and self.tp<5:
            self.tp += 1
            self.posY=constantes.hauteur-self.posY
            self.mv_x=self.mv_x*1.2
            self.mv_y=self.mv_y*1.2
        if self.posY<-20 or self.posY>constantes.hauteur+20 or self.posX<-20 or self.posX>constantes.largeur+20:
                self.dead=True



class Laserbleu:
    def __init__(self, posX, posY, mv_x, mv_y,rtImg):
        self.posX = posX
        self.posY = posY
        self.mv_x = mv_x*6
        self.mv_y = mv_y*6
        self.rtImg = rtImg
        self.dead=False
        self.colli=False
        self.indice=12
        self.anti=False
        self.degats = 1
        self.imgrt= constantes.laser4.convert_alpha()
        self.img= pygame.transform.rotate(self.imgrt,self.rtImg)
        self.rect = self.img.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def __del__(self):
        del self

    def move(self):
        self.posX += self.mv_x
        self.posY += self.mv_y
        self.rect.x = self.posX
        self.rect.y = self.posY
        liste=[]
        with open("positions.pickle", 'rb') as file:
            positions=pickle.load(file)
        donnees=positions[0]
        if len(donnees)!=0:
            for i in range(len(donnees)):
                self.ancienposX=donnees[i][0]
                self.ancienposY=donnees[i][1]
                distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                self.a = (float((self.ancienposX-self.posX)/distance))*2
                self.b = (float((self.ancienposY-self.posY)/distance))*2
                liste.append(distance)
            indice=liste.index(min(liste))
            self.ancienposX=donnees[indice][0]
            self.ancienposY=donnees[indice][1]
            distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
            self.a = (float((self.ancienposX-self.posX)/distance))*2
            self.b = (float((self.ancienposY-self.posY)/distance))*2
            if self.a<=self.mv_x:
                self.mv_x=self.mv_x-1
            if self.a>self.mv_x:
                self.mv_x=self.mv_x+1
            if self.b<=self.mv_y:
                self.mv_y=self.mv_y-1
            if self.b>self.mv_y:
                self.mv_y=self.mv_y+1
            self.rtImg+=1
            self.img= pygame.transform.rotate(self.imgrt,self.rtImg)
            #self.rect = self.img.get_rect()
        if self.posY<-20 or self.posY>constantes.hauteur+20 or self.posX<-20 or self.posX>constantes.largeur+20:
            self.dead=True


class Muon:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.dead=False
        self.colli=False
        self.indice=18
        self.anti=False
        self.degats = 1
        self.img= pygame.image.load('resources/photos/muon.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def __del__(self):
        del self

    def move(self):
        self.posX += self.mv_x
        self.posY += self.mv_y
        self.rect.x = self.posX
        self.rect.y = self.posY
        liste=[]
        with open("positions.pickle", 'rb') as file:
            positions=pickle.load(file)
        donnees=positions[0]
        if len(donnees)!=0:
            for i in range(len(donnees)):
                self.ancienposX=donnees[i][0]
                self.ancienposY=donnees[i][1]
                distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
                self.a = (float((self.ancienposX-self.posX)/distance))*2
                self.b = (float((self.ancienposY-self.posY)/distance))*2
                liste.append(distance)
            indice=liste.index(min(liste))
            self.ancienposX=donnees[indice][0]
            self.ancienposY=donnees[indice][1]
            distance=sqrt(pow(self.ancienposX-self.posX,2)+pow(self.ancienposY-self.posY,2))
            self.a = (float((self.ancienposX-self.posX)/distance))*2
            self.b = (float((self.ancienposY-self.posY)/distance))*2
            if self.a<=self.mv_x:
                self.mv_x=self.mv_x-1
            if self.a>self.mv_x:
                self.mv_x=self.mv_x+1
            if self.b<=self.mv_y:
                self.mv_y=self.mv_y-1
            if self.b>self.mv_y:
                self.mv_y=self.mv_y+1
            self.rtImg+=1
            self.img= pygame.transform.rotate(self.imgrt,self.rtImg)
            #self.rect = self.img.get_rect()
        if self.posY<-20 or self.posY>constantes.hauteur+20 or self.posX<-20 or self.posX>constantes.largeur+20:
            self.dead=True