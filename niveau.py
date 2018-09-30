# Créé par Pierre, le 05/03/2016 en Python 3.2
#from PIL import Image
import atome
from random import *
from dialogue import Dialog
import copy
import constantes
from pattern import *
import pickle
import time


class Niveau:


    def __init__(self, numero):
        self.numero=numero
        self.pathMusicLevel = str("resources/niveau/" + str(numero) + "/music.wav")
        self.pathMusicBoss = str("resources/niveau/" + str(numero) + "/musicBoss.wav")

        with open("resources/niveau/"+str(numero)+"/firstDialog.pickle", 'rb') as file:
            firstDialog = pickle.load(file)
        with open("resources/niveau/"+str(numero)+"/middleDialog.pickle", 'rb') as file:
            middleDialog = pickle.load(file)
        with open(str("resources/niveau/"+str(numero)+"/lastDialog.pickle"), 'rb') as file:
            lastDialog = pickle.load(file)

        self.firstDialog = firstDialog
        self.middleDialog = middleDialog
        self.lastDialog = lastDialog

        self.fond = ("resources/niveau/" + str(numero) + "/fond.jpg")
        #self.totalMobsLeft = 0

    def genererdialog(niveau,numero2):
        with open("resources/niveau/"+str(niveau)+"/"+str(numero2)+".pickle", 'rb') as file:
            dialog = pickle.load(file)
        return dialog
    def genererMob(self,typeat,parametres):
        pattern=100
        ennemi=typeat
        ennemi.pattern=parametres
        #self.totalMobsLeft -= 1
        if pattern == 0 : #pattern normal
            ennemi.pattern = Pattern(1,0)
        if pattern == 1 : #pattern normal
            ennemi.pattern = Pattern(-1,0)

        elif pattern == 10 : #pattern polynome
            ennemi.pattern = PatternPolynome(parametres)
            """if ennemi.pattern.dir == -1 :
                ennemi.posX=constantes.largeur
            elif ennemi.pattern.dir == 1 :
                ennemi.posX=0"""
            #ennemi.pattern=PatternPolynome(-1/1000,1/200,150)


        elif pattern == 2 : #pattern cercle
            ennemi.pattern = PatternCercle(randint(-200,constantes.largeur+200),randint(-100,constantes.hauteur-200),1,1,1)
            ennemi.pattern = PatternCercle(randint(0,constantes.largeur),randint(0,constantes.hauteur-200),1,1,1)
            rand= randint(1,3)
            if rand== 1 :
                ennemi.posY= -5-ennemi.rect.height
                ennemi.posX= randint(-5,constantes.largeur)
            else:
                ennemi.posY= randint(-5,constantes.hauteur-100)
                if rand==2:
                    ennemi.posX=-5-ennemi.rect.width
                else :
                    ennemi.posX=constantes.largeur+5
            ennemi.pattern.rayon=sqrt(pow(ennemi.posX-ennemi.pattern.centreX,2)+pow(ennemi.posY-ennemi.pattern.centreY,2))
            #print(ennemi.posX,ennemi.posY,ennemi.pattern.centreX,ennemi.pattern.centreY,ennemi.pattern.rayon)
            ennemi.pattern.vitesse=randint(3,10)/ennemi.pattern.rayon/6*pi
            if ennemi.posX<ennemi.pattern.centreX and ennemi.posY>ennemi.pattern.centreY or ennemi.posX>ennemi.pattern.centreX and ennemi.posY<ennemi.pattern.centreY :   #je suis pas sûr pour cette condition encore mais elle semble bonne
                ennemi.pattern.vitesse=-ennemi.pattern.vitesse  #en gros on inverse le sens dans les 2 cas où c'est nécessaire
            ennemi.pattern.angle=abs(acos((ennemi.posX-ennemi.pattern.centreX)/ennemi.pattern.rayon))
            if ennemi.posY-ennemi.pattern.centreY<0:
                ennemi.pattern.angle=-ennemi.pattern.angle


        elif pattern == 3 : #zigzag
            ennemi.pattern= PatternZigZag(randint(10,30),randint(1,5))
            rand= randint(1,3)
            if rand== 1 :
                ennemi.posY= -5-ennemi.rect.height
                ennemi.posX= randint(-5,constantes.largeur)
                ennemi.pattern.mv_x = 0
                ennemi.pattern.mv_y = 1
            else:
                ennemi.posY= randint(-5,constantes.hauteur-100)
                ennemi.pattern.mv_y = 0
                if rand==2:
                    ennemi.posX=-5-ennemi.rect.width
                    ennemi.pattern.mv_x = 1
                else :
                    ennemi.posX=constantes.largeur+5
                    ennemi.pattern.mv_x = -1
            ennemi.pattern.compteur = -150

        elif pattern == 4 :

            ennemi.pattern = PatternSinusoidal(randint(10,50)*3,(randint(0,1)-0.5)*2,randint(10,constantes.hauteur-50)-150)
            if ennemi.pattern.direction == -1 :
                ennemi.posX=constantes.largeur+5




        ennemi.rect.x = ennemi.posX
        ennemi.rect.y = ennemi.posY

        return ennemi




