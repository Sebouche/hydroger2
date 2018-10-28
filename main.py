﻿# Créé par Pierre, le 07/05/2016 en Python 3.2
import time
import pygame
import sys
import constantes
import pickle
from menu import *
from fenetre import *
from jeu import *
from niveau import *
from atome import *
from os import listdir
from os.path import isfile, join
listeReplay = [f for f in listdir("resources/replay/") if isfile(join('resources/replay', f))]
listeReplay = listeReplay[:-1]


pygame.init()
pygame.mixer.init()

with open("options.pickle", 'rb') as file:
    donnees = pickle.load(file)


constantes.niveauActuel = donnees[0]
constantes.niveauMaxAtteint = donnees[1]
constantes.hauteur=donnees[2]
constantes.largeur=donnees[3]
constantes.touches=donnees[4]
constantes.meilleur_score=donnees[7]
constantes.volume=donnees[8]
constantes.difficultechoisie=donnees[9]


pygame.mixer.init(frequency=22050, size=-16, channels=25, buffer=4096)
try:
    pygame.mixer.music.load('menu.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(constantes.volume/100)
except:
    print("musique du menu introuvable")


fenetre = Fenetre("Hyd'Roger", constantes.largeur, constantes.hauteur)
fond = pygame.image.load("resources/photos/hyd'roger.png").convert()
fenetre.fen.blit(fond, (0,0))
time.sleep(1)
menu = Menu()
if sum(constantes.meilleur_score)>=1500000:
    menu.init(['????????????','Nouvelle Partie', 'Continuer', 'Choix du Niveau', 'Replay','Scores', 'Options', 'Quitter'], fenetre.fen)
else:
    menu.init(['Nouvelle Partie', 'Continuer', 'Choix du Niveau', 'Replay','Scores', 'Options', 'Quitter'], fenetre.fen)
menu.draw()
pygame.key.set_repeat(199,69)
pygame.display.update()
choixNiveau = True
while 1:
    fond = pygame.image.load("resources/photos/hyd'roger.png").convert()
    fenetre.fen.blit(fond, (0,0))
    menu.draw()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                menu.draw(-1)
            if event.key == K_DOWN:
                menu.draw(1)
            if event.key == K_RETURN:
                if len(menu.liste)==8:
                    if menu.get_position() == 0:
                        jeu = Jeu(fenetre, Niveau(666), Hydrogene(384,580,Pattern(0,0)),4.5)
                        constantes.niveauActuel = 1
                        constantes.sauvegarder()
                        jeu.progressInLevel()
                        sombre = pygame.Surface((constantes.largeur, constantes.hauteur))
                        sombre.set_alpha(255)
                        sombre.fill((0, 0, 0))
                        fenetre.fen.blit(sombre, (0,0))
                        pygame.display.flip()
                        menu.draw()
                        pygame.display.update()
                if menu.get_position() == len(menu.liste)-7:                                                                            #marche
                    jeu = Jeu(fenetre, Niveau(1), Hydrogene(384,580,Pattern(0,0)),4.5)
                    constantes.niveauActuel = 1
                    constantes.sauvegarder()
                    jeu.progressInLevel()
                    sombre = pygame.Surface((constantes.largeur, constantes.hauteur))
                    sombre.set_alpha(255)
                    sombre.fill((0, 0, 0))
                    fenetre.fen.blit(sombre, (0,0))
                    pygame.display.flip()
                    menu.draw()
                    pygame.display.update()
                elif menu.get_position() == len(menu.liste)-6:                                                                                #marche
                    jeu = Jeu(fenetre, Niveau(constantes.niveauActuel), Hydrogene(384,580,Pattern(0,0)), 4.5)
                    jeu.progressInLevel()
                    sombre = pygame.Surface((constantes.largeur, constantes.hauteur))
                    sombre.set_alpha(255)
                    sombre.fill((0, 0, 0))
                    fenetre.fen.blit(sombre, (0,0))
                    pygame.display.flip()
                    menu.draw()
                    pygame.display.update()
                elif menu.get_position() == len(menu.liste)-5 :                                                                              #manque plus qu'a mettre constantes.niveauMaxatteint
                    fond = pygame.image.load("resources/photos/hyd'roger.png").convert()
                    fenetre.fen.blit(fond, (0,0))
                    choix = Menu()
                    listeNiveaux = []
                    for a in range(constantes.niveauMaxFait):
                        listeNiveaux.append(str(a+1))

                    choix.init(listeNiveaux, fenetre.fen)
                    choix.draw()
                    pygame.key.set_repeat(199,69)
                    pygame.display.update()
                    while choixNiveau:
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_UP:
                                    choix.draw(-1)
                                if event.key == K_DOWN:
                                    choix.draw(1)
                                if event.key == K_RETURN :
                                    jeu = Jeu(fenetre, Niveau(choix.get_position()+1),Hydrogene(384,580,Pattern(0,0)), 4.5)
                                    constantes.niveauActuel = choix.get_position()+1
                                    jeu.progressInLevel()
                                    sombre = pygame.Surface((constantes.largeur, constantes.hauteur))
                                    sombre.set_alpha(255)
                                    sombre.fill((0, 0, 0))
                                    fenetre.fen.blit(sombre, (0,0))
                                    pygame.display.flip()
                                    choix.draw()
                                    pygame.display.update()
                                    choixNiveau = False
                                if event.key == K_ESCAPE:
                                    choixNiveau = False
                                pygame.display.update()
                            elif event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                    choixNiveau = True
                elif menu.get_position() == len(menu.liste)-4:                                                                                #replay je te les laisse baptiste
                    for a in listeReplay:
                        fenetre.playReplay("resources/replay/"+str(a))
                elif menu.get_position() == len(menu.liste)-3:
                    fond = pygame.image.load("resources/photos/hyd'roger.png").convert()
                    fenetre.fen.blit(fond, (0,0))
                    scores = Menu()
                    liste=[]
                    for i in range(len(constantes.meilleur_score)):
                        liste.append(str(constantes.meilleur_score[i]))
                    scores.init(liste,fenetre.fen)
                    scoresquitter = False
                    while scoresquitter == False:
                        scores.draw()
                        pygame.key.set_repeat(199,69)
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                    scoresquitter =True
                elif menu.get_position() == len(menu.liste)-2:
                    fond = pygame.image.load("resources/photos/hyd'roger.png").convert()
                    fenetre.fen.blit(fond, (0,0))
                    option = Menu()
                    option.init(['Selection des touches','Volume : {}'.format(constantes.volume),'Difficulté : {}'.format(constantes.difficulte[constantes.difficultechoisie]),'Langue: {}'.format(constantes.langue)],fenetre.fen)
                    optionquitter = False
                    while optionquitter == False:
                        option.draw()
                        pygame.key.set_repeat(199,69)
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_UP:
                                    option.draw(-1)
                                if event.key == K_DOWN:
                                    option.draw(1)
                                if event.key == K_RIGHT :
                                    if option.get_position() == 1 and constantes.volume<100 :
                                        constantes.volume+=1
                                        fenetre.fen.blit(fond, (0,0))
                                        option.init(['Selection des touches','Volume : {}'.format(constantes.volume),'Difficulté : {}'.format(constantes.difficulte[constantes.difficultechoisie]),'Langue: {}'.format(constantes.langue)],fenetre.fen)
                                        option.position=1
                                    if option.get_position() == 2 and constantes.difficultechoisie>0 :
                                        constantes.difficultechoisie-=1
                                        fenetre.fen.blit(fond, (0,0))
                                        option.init(['Selection des touches','Volume : {}'.format(constantes.volume),'Difficulté : {}'.format(constantes.difficulte[constantes.difficultechoisie]),'Langue: {}'.format(constantes.langue)],fenetre.fen)
                                        option.position=2
                                    option.draw()
                                    constantes.sauvegarder()
                                if event.key == K_LEFT :
                                    if option.get_position() == 1 and constantes.volume>0 :
                                        constantes.volume-=1
                                        fenetre.fen.blit(fond, (0,0))
                                        option.init(['Selection des touches','Volume : {}'.format(constantes.volume),'Difficulté : {}'.format(constantes.difficulte[constantes.difficultechoisie]),'Langue: {}'.format(constantes.langue)],fenetre.fen)
                                        option.position=1
                                    if option.get_position() == 2 and constantes.difficultechoisie<3 :
                                        constantes.difficultechoisie+=1
                                        fenetre.fen.blit(fond, (0,0))
                                        option.init(['Selection des touches','Volume : {}'.format(constantes.volume),'Difficulté : {}'.format(constantes.difficulte[constantes.difficultechoisie]),'Langue: {}'.format(constantes.langue)],fenetre.fen)
                                        option.position=2
                                    option.draw()
                                    constantes.sauvegarder()
                                if event.key == K_RETURN:
                                    if option.get_position() == 0:

                                        touches = [0,0,0,0,0,0,0]
                                        nomtouches = ["Tir","Gauche","Droite","Haut","Bas","Ralentir","Objet"]
                                        for i in range(len(touches)):
                                            fenetre.fen.blit(fond, (0,0))
                                            fenetre.assombrir()
                                            fenetre.ecrireTexte('Vous allez changer la touche ',250,210)
                                            fenetre.ecrireTexte(nomtouches[i],constantes.largeur/2,constantes.hauteur/2)
                                            pygame.display.update()


                                            while touches[i] == 0 :

                                                event = pygame.event.wait()
                                                if event.type == KEYDOWN:
                                                    touches[i] = event.key

                                        constantes.touches = touches
                                        constantes.sauvegarder()
                                    if option.get_position() == 3:
                                        selectLangue = True
                                        while selectLangue :
                                            for event in pygame.event.get():
                                                constantes.indiceLangue+=1
                                                if constantes.indiceLangue > len(constantes.langueDispo):
                                                    constantes.langueDispo = 0
                                                    selectLangue = False
                                                    """if event.type == KEYDOWN:
                                                    if event.key == K_RIGHT:
                                                        constantes.indiceLangue+=1
                                                        if constantes.indiceLangue > len(constantes.langueDispo):
                                                            constantes.langueDispo = 0
                                                        selectLangue = False
                                                    elif event.key == K_LEFT:
                                                        constantes.indiceLangue-=1
                                                        if constantes.indiceLangue<0 :
                                                            constantes.indiceLangue = len(constantes.langueDispo)
                                                        constantes.langue =constantes.langueDispo[constantes.indiceLangue]
                                                        selectLangue = False"""
                                                    constantes.langue =constantes.langueDispo[constantes.indiceLangue]
                                                    option.liste[3]= "Langue : {}".format(constantes.langue)
                                                    option.draw()
                                                    pygame.display.update()


                                    if option.get_position() == 1:
                                        pass

                                    if option.get_position() == 2:
                                        pass
                                    fenetre.fen.blit(fond, (0,0))
                                    pygame.display.update()
                                if event.key == K_ESCAPE:
                                    optionquitter =True

                elif menu.get_position() == len(menu.liste)-1:                                                                 #marche
                    pygame.quit()
                    sys.exit()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    pygame.time.wait(8)
