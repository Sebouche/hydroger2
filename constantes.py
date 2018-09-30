# Créé par Pierre, le 17/03/2016 en Python 3.2
import pygame
import pickle
pygame.init()
"""Constantes projectiles"""
projectilesList = [ pygame.image.load("resources/photos/photon_bleu_clair_pour_le_joueur2.png"),
                    pygame.image.load("resources/photos/photon_bleu.png"),
                    pygame.image.load("resources/photos/photon_jaune.png"),
                    pygame.image.load("resources/photos/photon_rose.png"),
                    pygame.image.load("resources/photos/photon_sombre.png"),
                    pygame.image.load("resources/photos/photon_vert.png"),
                    pygame.image.load("resources/photos/photon_violet.png"),
                    pygame.image.load("resources/photos/photon_rouge.png")]

laser = pygame.image.load("resources/photos/laserjaune.png")
laser2 = pygame.image.load("resources/photos/laservert.png")
laser3 = pygame.image.load("resources/photos/lasernoir.png")
laser4 = pygame.image.load("resources/photos/laserbleu.png")

"""Les sprites des explosions"""
explodeList = [pygame.image.load("resources/photos/explosion_v1.1.bmp"),
               pygame.image.load("resources/photos/explosion_v2.2.bmp"),
               pygame.image.load("resources/photos/explosion_v3.bmp")]


objets_dispo=[pygame.image.load("resources/photos/objet1.png"),
                pygame.image.load("resources/photos/objet2.png"),
                pygame.image.load("resources/photos/objet3.png"),
                pygame.image.load("resources/photos/objet4.png"),
                pygame.image.load("resources/photos/objet1.png")]
texte=["Augmente temporairement la puissance de Roger",
        "Roger se protege avec une armure de carbones",
        "Le plutonium vient au secours de Roger",
        "Roger tire temporairement des lasers",
        "Roger ralentit le temps"]
positionx=0
positiony=0


inversionverticale=1
inversionhorizontale=1

charge=[200,400,60,700,300]

meilleur_score=[0,0,0,0,0]


touches = [122, 276, 275, 273, 274, 304,0]      #touches = [tir,gauche,droite,haut,bas,controle,objet]
#Quand vous voulez récupérer l'image d'un photon : projectilesList[index]

#lycee
largeur,hauteur= 768, 600
#pas lycee
#largeur,hauteur=1280,720


recordOn=True
niveauActuel=1
niveauMaxAtteint=1
niveauMaxFait = 5


volume=100
difficulte={3:"Facile",2:"Normal",1:"Difficile",0:"Impossible"}
difficultechoisie=0
coeffdifficulte=[0.5,1,2,3]

def sauvegarder() :
        """if niveauMaxAtteint > niveauMaxFait :
            niveauMaxAtteint = niveauMaxFait"""
        with open("options.pickle", 'wb') as file:
            pickle.dump([niveauActuel,niveauMaxAtteint,hauteur,largeur,touches,positionx,positiony,meilleur_score,volume,difficultechoisie],file)


indiceLangue = 1
langueDispo = ['FR','JP','DE','PL']
langue = langueDispo[indiceLangue]