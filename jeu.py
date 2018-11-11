# Créé par Pierre, le 05/03/2016 en Python 3.2
from random import *
from fenetre import *
import pygame
from pygame.event import *
from pygame.locals import * #Pour les events.
pygame.init()
from projectiles import *
from pattern import *
from constantes import *
from replay import *
from niveau import *
import time
import tampon
import pickle
from menu import *
import atome
from os import listdir

listeFichiers = [f for f in listdir()]

if "options.pickle" in listeFichiers:
    with open("options.pickle", 'rb') as file:
        donnees = pickle.load(file)
else:
    donnees = [1, 1, 600, 768, [122, 276, 275, 273, 274, 304, 120], 0, 0, [0] * 5, 50, 2]
    with open("options.pickle", 'wb') as file:  # niveauActuel,niveauMaxAtteint,hauteur,largeur,touches,positionx,positiony,meilleur_score,volume,difficultechoisie
        pickle.dump(donnees, file)


constantes.volume=donnees[8]
pygame.mixer.init(frequency=22050, size=-16, channels=25, buffer=4096)
explosion1 = pygame.mixer.Sound("resources/explosion1.wav")
explosion2 = pygame.mixer.Sound("resources/explosion2.wav")
objet1 = pygame.mixer.Sound("resources/objet1.wav")
explosion1.set_volume(0.7*constantes.volume/100)
explosion2.set_volume(0.7*constantes.volume/100)
objet1.set_volume(constantes.volume/100)
audioDialogue=pygame.mixer.Channel(0)
audioDialogue.set_volume(5*constantes.volume/100)
musicDialogue = pygame.mixer.Channel(1)

class Jeu:
    """La classe qui s'occupera de gérer le jeu en lui même"""

    def __init__(self, fenetre, niveau, moleculeJoueur, vitesse): #on lui donnera le niveau qu'on veut jouer (un int, et on ira chercher dans des dossiers).
        self.fenetre = fenetre
        self.niveau = niveau
        self.fenetre.setFond(self.niveau.fond)
        self.ennemyList = [] #les molécules méchantes
        self.ennemyProjectiles = [] #les projectiles des molécules méchantes
        self.projectilesJoueur = [] #les projectiles de la molécule gentille.

        self.continuer = True
        self.moleculeJoueur = moleculeJoueur
        self.moleculeJoueur.hpMax = 20*constantes.coeffdifficulte[constantes.difficultechoisie]
        self.moleculeJoueur.hp = 20*constantes.coeffdifficulte[constantes.difficultechoisie]
        self.pluto=0
        self.delayTirJoueur = 0
        self.score=0
        self.tir = False
        self.boost=1
        self.delayMouvement = 0
        self.typeProjJoueur =[  [(0,0,0,-3)],
                                [(-12,0,0,-3),(12,0,0,-3)],
                                [(-12,5,-0.5,-2.5),(0,0,0,-3),(12,5,0.5,-2.5)],
                                [(-15,5,-0.5,-2.5),(-8,0,0,-3),(8,0,0,-3),(15,5,0.5,-2.5)]]

        self.listeFrame=[]
        self.vitesse = vitesse
        self.finpause=0
        self.debutpause=0
        self.tempspause=0
        self.objet=0
        self.choix=0
        self.temps=-1
        self.moleculeJoueur.posX = constantes.largeur/2
        self.moleculeJoueur.posY = constantes.hauteur-35
        if self.niveau.numero < len(self.typeProjJoueur) :
            self.projAAjouter = self.typeProjJoueur[self.niveau.numero-1]
        else :
            self.projAAjouter = self.typeProjJoueur[-1]
        #self.moleculeJoueur = Atome()  #bon ok, c'est un atome...
        self.framesInvincibilite = 0





    def play(self,niv):
        pygame.time.Clock().tick(15)
        self.continuer = True
        self.clearProj()
        self.clearEnnemis
        self.tir = False
        debut=time.time()
        phase=2
        genere=[]
        while self.continuer:
            current=time.time()
            self.a=True
            er = [] #rect ennemies
            epr = [] #rect des projectiles ennemis
            pjr = [] #rect des projectiles du joueur.
            if niv==0:
                genere,phase,dialog=tampon.Tampon1(constantes.niveauActuel,debut,current,self.tempspause,phase)
            elif niv==1 :
                genere,phase,dialog=tampon.Tampon2(constantes.niveauActuel,debut,current,self.tempspause,phase)
            else:
                dialog=0
                phase=True
            if dialog!=0:
                self.ennemyProjectiles=[]
                self.dialoguer(Niveau.genererdialog(constantes.niveauActuel,dialog),dialog)
            if self.choix==2 and self.temps>=1:
                proj=Matiere(self.pluto.posX,self.pluto.posY,uniform(-3,3),-3,1)
                self.projectilesJoueur.append(proj)
            for i in range(len(genere)):
                self.ennemyList.append(genere[i])
            #La boucle principale du jeu.
            #print("yolo ! On s'amuse bien !")
            #print(self.moleculeJoueur.rect)
            """Mouvement des différentes molecules et projectiles"""
            """if self.delayMouvement < 0 :
                self.delayMouvement = 10
            self.delayMouvement -= 1"""
            newList=[]
            for ennemy in self.ennemyList:
                if ennemy.dead==False:
                    if self.delayMouvement == 0 :
                        ennemy.move()
                    er.append(ennemy.rect)
                    #er.append(ennemy.rect)
                    self.ennemyProjectiles+=ennemy.tir()
                    newList.append(ennemy)
                elif ennemy.hp<=0:#l'ennemi n'a plus d'hp
                    self.score+=20
                    ennemy.__del__()
                    explosion2.play()
                    #On met ici l'animation de mort, c'est à dire l'explosion, peut etre un score plus tard
                else:#l'ennemi sort de l'écran
#ennemy.posX<0 or ennemy.posX>768 or ennemy.posY<0 or ennemy.posY>600
                    ennemy.__del__()
                if ennemy.dying:
                    self.fenetre.explosions.append(ennemy.explodeCoords)
                #print(ennemy.rect)
            self.ennemyList=newList

            newList=[]
            for proj in self.ennemyProjectiles:
                if proj.dead==False:
                   proj.move()
                   epr.append(proj.rect)
                   newList.append(proj)
                elif proj.anti==True and proj.dead==True:
                    proj.__del__()
                    nouveau=proj.boom
                    for i in range(len(nouveau)):
                        newList.append(nouveau[i])
                else:
                    proj.__del__()
            self.ennemyProjectiles=newList
            newList=[]
            newList2=[]
            for proj in self.projectilesJoueur:
                indexMechantProjectile=proj.rect.collidelist(epr)
                if indexMechantProjectile!=-1:
                    self.ennemyProjectiles[indexMechantProjectile].colli=True
                    if self.ennemyProjectiles[indexMechantProjectile].colli==True and self.ennemyProjectiles[indexMechantProjectile].indice==666:
                        self.ennemyProjectiles[indexMechantProjectile].move()
                        nouveau=self.ennemyProjectiles[indexMechantProjectile].boom
                        for i in range(len(nouveau)):
                            newList2.append(nouveau[i])
                        self.ennemyProjectiles[indexMechantProjectile].__del__()
                        proj.__del__()
                        proj.dead=True
                        for proje in range(len(self.ennemyProjectiles)):
                            if self.ennemyProjectiles[proje]!=self.ennemyProjectiles[indexMechantProjectile]:
                                newList2.append(self.ennemyProjectiles[proje])
                        self.ennemyProjectiles=newList2
                        newList2=[]
                if proj.dead==False:
                    proj.move()
                    pjr.append(proj.rect)
                    newList.append(proj)
                else:
                    proj.__del__()
            self.projectilesJoueur=newList
            """Calcul des collisions."""
            indexMechant = self.moleculeJoueur.rect.collidelist(er)
            if indexMechant != -1:
                self.moleculeJoueur.hit(1)
                explosion1.play()
                self.ennemyList[indexMechant].hit(3)
            if self.choix==2 and self.temps>=1:
                indexMechant = self.pluto.rect.collidelist(er)
                if indexMechant != -1:
                    self.pluto.hit(1)
                    explosion1.play()
                    self.ennemyList[indexMechant].hit(3)
                indexMechantProjectile = self.pluto.rect.collidelist(epr)
                if indexMechantProjectile != -1:
                    self.pluto.hit(self.ennemyProjectiles[indexMechantProjectile].degats)
                    explosion1.play()
                    self.ennemyProjectiles[indexMechantProjectile].dead=True
            indexMechantProjectile = self.moleculeJoueur.rect.collidelist(epr)
            if self.framesInvincibilite > 0 :
                self.framesInvincibilite-= 1

            if indexMechantProjectile != -1 and self.framesInvincibilite == 0:
                if self.choix!=1 or self.temps <= 0:
                    self.moleculeJoueur.hit(self.ennemyProjectiles[indexMechantProjectile].degats)
                    self.framesInvincibilite = 50
                explosion1.play()
                self.ennemyProjectiles[indexMechantProjectile].dead=True #On supprime le projectile, s'il a touché sa cible.
                if self.score>=20:
                    self.score-=20
                else:
                    self.score=0

            for proj in self.projectilesJoueur:
                index = proj.rect.collidelist(er)
                if index != -1:
                    self.score+=1
                    self.ennemyList[index].hit(3*self.boost)
                    if self.temps<0:
                        self.objet+=1
                    proj.dead=True
            """Events incoming !"""
            event = pygame.event.poll()
            if event.type == NOEVENT:
                #print('Pas d\'event !')
                pass
            elif event.type == KEYDOWN:
                #print("Touche appuyée.")
                """Lorsqu'on appuie sur une touche. Ces valeurs ne sont là qu'a titre d'exemple, il faudra qu'on les modifies."""
                if event.key == constantes.touches[3]:
                    self.moleculeJoueur.pattern.mv_y = -1.2 * self.vitesse
                elif event.key == constantes.touches[4]:
                    #print("C'est la touche bas.")
                    self.moleculeJoueur.pattern.mv_y = 1.2 * self.vitesse
                elif event.key == constantes.touches[1]:
                    self.moleculeJoueur.pattern.mv_x = -1.2 * self.vitesse
                elif event.key == constantes.touches[2]:
                    self.moleculeJoueur.pattern.mv_x = 1.2 * self.vitesse
                if event.key == constantes.touches[0] :
                    self.tir =True
                if event.key == constantes.touches[5] :
                    self.vitesse = 2
                if event.key == constantes.touches[6] and self.objet>=constantes.charge[self.choix]:
                    phase=True
                    self.objet=0
                    self.traitement_objet(self.choix,0)
            elif event.type == KEYUP:
                """Lorsqu'on relâche une touche."""
                #print("Touche relachée !")
                if event.key == constantes.touches[3] and self.moleculeJoueur.pattern.mv_y<0:
                    self.moleculeJoueur.pattern.mv_y = 0
                elif event.key == constantes.touches[4] and self.moleculeJoueur.pattern.mv_y>0:
                    self.moleculeJoueur.pattern.mv_y = 0
                elif event.key == constantes.touches[1] and self.moleculeJoueur.pattern.mv_x<0:
                    self.moleculeJoueur.pattern.mv_x = 0
                elif event.key == constantes.touches[2] and self.moleculeJoueur.pattern.mv_x>0:
                    self.moleculeJoueur.pattern.mv_x = 0
                if event.key == constantes.touches[0]:
                    self.tir = False
                if event.key == constantes.touches[5] :
                    self.vitesse = 4.5
                if event.key == K_ESCAPE:
                    self.pause()
                """if event.key == K_r:
                    replay = Replay((constantes.largeur,constantes.hauteur),self.listeFrame)
                    nom = replay.nom
                    replay.saveReplay()
                    self.fenetre.playReplay(nom)"""
            elif event.type == QUIT:
                self.fenetre.fermer()
                self.continuer = False

            self.delayTirJoueur -= 1
            if self.tir == True and self.delayTirJoueur <=0 :
                self.shootJoueur(self.choix,self.temps)


            if len(self.ennemyList) <= 0 and phase==True:
                self.continuer = False
            elif self.moleculeJoueur.dead:
                self.continuer = False
                self.ennemyList = []
            self.moleculeJoueur.move()
            if self.choix==2 and self.temps>=1:
                self.pluto.move()
                if self.pluto.dead:
                    self.temps=0
            constantes.positionx=self.moleculeJoueur.posX
            constantes.positiony=self.moleculeJoueur.posY
            constantes.sauvegarder()
            self.sauverpositions()
            if self.moleculeJoueur.dying:
                self.fenetre.explosions.append(self.moleculeJoueur.explodeCoords)
            if self.moleculeJoueur.posX<5:
                self.moleculeJoueur.posX=5
            elif self.moleculeJoueur.posX>constantes.largeur-20:  #changer encore ici
                self.moleculeJoueur.posX=constantes.largeur-20
            if self.moleculeJoueur.posY <5:
                self.moleculeJoueur.posY=5
            elif self.moleculeJoueur.posY>constantes.hauteur-20:
                self.moleculeJoueur.posY=constantes.hauteur-20
            self.actualiser()
            if constantes.recordOn :
                self.listeFrame.append(pygame.image.tostring(self.fenetre.fen,"RGB"))
                if len(self.listeFrame)>500 :
                    self.listeFrame = self.listeFrame[-500:]
            if self.temps== 0:
                self.traitement_objet(self.choix,1)
            self.temps-=1


    def actualiser(self):
        self.fenetre.entites.extend(self.ennemyList)
        self.fenetre.entites.extend(self.ennemyProjectiles)
        self.fenetre.entites.extend(self.projectilesJoueur)
        if self.framesInvincibilite/2 == int(self.framesInvincibilite/2) :
            self.fenetre.entites.append(self.moleculeJoueur)
        if self.choix==2 and self.temps>=1:
            self.fenetre.entites.append(self.pluto)
        self.fenetre.rafraichir(self.moleculeJoueur.hp,self.moleculeJoueur.hpMax,self.objet,self.choix)

    def dialoguer(self, dialog,placeDialog):
        self.debutpause=time.time()
        """sombre = pygame.Surface((self.fenetre.largeur, self.fenetre.hauteur))
        sombre.set_alpha(128)
        sombre.fill((0, 0, 0))"""
        perso = []
        for liste in dialog.characters:
            img = pygame.image.load(liste[1]).convert_alpha()
            perso.append([liste[0], img, liste[2]])
        for p in perso:
            #print(p)
            #print(p[1].get_rect())
            rect = p[1].get_rect()
            rect.x, rect.y = p[2]
            p[2] = (rect.x, self.fenetre.hauteur - 100 - rect.height)
            if p[2][0] == 500 :
                p[2]= (constantes.largeur-rect.width,self.fenetre.hauteur-100-rect.height)
            self.fenetre.rafraichir(self.moleculeJoueur.hp,self.moleculeJoueur.hpMax,self.objet,self.choix)
        while dialog.notFinished:
            self.finpause=time.time()
            punchline = dialog.getPunchline()
            try :   #virer cette ligne quand tous les dialogues auront été faits
                audio = pygame.mixer.Sound("resources/niveau/{2}/{3}/{0},{1}.wav".format(placeDialog,dialog.counter,self.niveau.numero,constantes.langue))
                """volume = audioDialogue.get_volume()
                multiplier = 1/volume
                audioDialogue.set_volume(multiplier*(1-punchline[1])+0.4,multiplier*(punchline[1])+0.4)"""
                audioDialogue.play(audio)
            except:
                pass
            posX, posY = perso[punchline[1]][2]

            #print(punchline[1][0])
            #pygame.draw.rect(self.fenetre.fen, pygame.Color(0, 0, 0, 0), pygame.Rect(0, 0, self.fenetre.largeur, self.fenetre.hauteur))
            #self.fenetre.fen.blit(sombre, (0,0))
            self.fenetre.assombrir()
            self.fenetre.fen.blit(perso[punchline[1]][1], (posX, posY))
            self.fenetre.dessinerCadre(0, self.fenetre.hauteur-100, 100, self.fenetre.largeur)
            self.font = self.fenetre.font
            surface = self.font.render(perso[punchline[1]][0], 0, pygame.Color(255, 0, 0, 0))
            self.fenetre.dessinerCadre(posX+50, posY-25, 30, surface.get_rect().width+10)
            self.fenetre.ecrireTexte(perso[punchline[1]][0], posX + 55, posY - 20)
            self.fenetre.ecrireTexte(punchline[0], 25, self.fenetre.hauteur-80)
            event = pygame.event.wait()
            #audio = pygame.mixer.Sound("resources/temporaire/"+str(dialog.counter)+".wav")
            #audioDialogue(audio)
            reading = True
            while reading:
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == constantes.touches[0]:
                        reading = False
                    if event.key == K_LEFT:
                        reading = False
                        dialog.counter-=2
                        if dialog.counter<0:
                            dialog.counter = 0

            self.fenetre.rafraichir(self.moleculeJoueur.hp,self.moleculeJoueur.hpMax,self.objet,self.choix)
            self.fenetre.fen.blit(perso[punchline[1]][1], (posX, posY))
        self.tempspause+=self.finpause-self.debutpause
        audioDialogue.stop()
        musicDialogue.stop()

    def progressInLevel(self):
        self.sauverpositions()
        play = True
        while play:
            self.fenetre.setFond(self.niveau.fond)
            self.introLevel()
            self.choixobjet()
            self.dialoguer(self.niveau.firstDialog,1)
            try:
                pygame.mixer.music.load(self.niveau.pathMusicLevel)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(constantes.volume/100)
            except:
                print("musique du niveau {} introuvable".format(self.niveau.numero))
            self.tempspause=0
            self.play(0)
            pygame.mixer.music.pause()
            if self.moleculeJoueur.dead == False:
                self.dialoguer(self.niveau.middleDialog,1)
                self.tempspause=0
                try:
                    pygame.mixer.music.load(self.niveau.pathMusicBoss)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(constantes.volume/100)
                except:
                    print("musique du boss du niveau {} introuvable".format(self.niveau.numero))
                #self.niveau.boss.posX = (constantes.largeur-self.niveau.boss.rect.width)/2
                #self.niveau.boss.posY = 10
                #self.niveau.boss.rect.x = self.niveau.boss.posX
                #self.niveau.boss.rect.y = self.niveau.boss.posY
                #self.ennemyList = [self.niveau.boss]
                self.play(1)
                self.score+=10000*(len(constantes.coeffdifficulte)-constantes.coeffdifficulte[constantes.difficultechoisie])
                pygame.mixer.music.pause()
            if self.moleculeJoueur.dead == False:
                self.dialoguer(self.niveau.lastDialog,2)
                self.tempspause=0
                self.outroLevel()
                if self.score>constantes.meilleur_score[constantes.niveauActuel-1]:
                    constantes.meilleur_score[constantes.niveauActuel-1]=self.score
                constantes.niveauActuel = self.niveau.numero+1
                if constantes.niveauMaxFait < constantes.niveauActuel :
                    constantes.niveauActuel = 1
                    constantes.sauvegarder()
                    self.niveau.numero = 0
                    self.fenetre.generiqueFin()
                if constantes.niveauActuel>constantes.niveauMaxAtteint :
                    constantes.niveauMaxAtteint = constantes.niveauActuel
                constantes.sauvegarder()
                self.fenetre.selectNextLevel(self.score)
                self.score=0
                key = self.waitForSelection()
                if key == K_RETURN:
                    print("On a appuyé sur entrée !")
                    self.changeNiveau(1) #on lui donne 1 quand on veut le niveau suivant.
                elif key == K_ESCAPE:
                    print("On a appuyé sur Echap !")
                    play = False
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.load("resources/game_over.wav")
                pygame.mixer.music.play(1)
                self.fenetre.selecContinuer()
                key = self.waitForSelection()
                if key == K_ESCAPE:
                    play = False
                elif key == K_RETURN:
                    self.moleculeJoueur.reset()
                    self.clearProj()
                    self.ennemyList = []
                    self.changeNiveau(0) #Et 0 quand on recharge le niveau.
                    pygame.mixer.music.pause()
                    self.progressInLevel()


    def waitForSelection(self):
        while 1:
            event = pygame.event.wait()
            if event.type == KEYUP:
                if event.key == K_RETURN or event.key == K_ESCAPE:
                    return event.key

    def stop(self):
        #si on veut faire des choses particulières une fois qu'on arrête le jeu.
        self.continuer = false

    def changeNiveau(self, plus):
        """Cette fonction s'occupera de charger tout ce dont on a besoin d'un niveau :
            mobs, probas..."""
        #print("Hop, on change de niveau :", str(self.niveau.numero+1))
        self.niveau = Niveau(self.niveau.numero + plus)
        if self.niveau.numero < len(self.typeProjJoueur) :
            self.projAAjouter = self.typeProjJoueur[self.niveau.numero-1]
        else :
            self.projAAjouter = self.typeProjJoueur[-1]

    def pause(self):
        pause = True
        self.debutpause=time.time()
        self.fenetre.afficherPause()
        score='Score :'+str(self.score)
        self.fenetre.ecrireTexte(score,constantes.largeur/2-35,constantes.hauteur/2+25)
        while pause:
            self.finpause=time.time()
            event = pygame.event.wait()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pause = False
                if event.key == K_r:
                    replay = Replay((constantes.largeur,constantes.hauteur),self.listeFrame)
                    nom = replay.nom
                    replay.saveReplay()
                    self.fenetre.ecrireTexte("Replay Sauvegardé !",10,100)
        self.tempspause+=self.finpause-self.debutpause


    def clearProj(self):
        for a in self.ennemyProjectiles :
            a.dead = True
        for proj in self.projectilesJoueur:
            proj.dead = True
    def clearEnnemis(self):
        for a in self.ennemyList :
            a.dead = True

    def shootJoueur(self,choix,temps):
        if choix==3 and temps>=1:
            for a in self.projAAjouter :
                proj = Laserbleu(a[0]+self.moleculeJoueur.posX,a[1]+self.moleculeJoueur.posY,a[2],a[3],0)
                proj.img = constantes.laser4.convert_alpha()
                self.projectilesJoueur.append(proj)
        else:
            for a in self.projAAjouter :
                proj = Projectile(a[0]+self.moleculeJoueur.posX,a[1]+self.moleculeJoueur.posY,a[2],a[3])
                proj.img = constantes.projectilesList[0].convert_alpha()
                self.projectilesJoueur.append(proj)
        self.delayTirJoueur=2

    def introLevel(self):
        self.framesInvincibilite = 0
        self.moleculeJoueur.posX = constantes.largeur/2
        self.moleculeJoueur.posY = constantes.hauteur + 10
        self.moleculeJoueur.pattern.mv_x = 0
        self.moleculeJoueur.pattern.mv_y = -1
        x = 0
        for x in range(100):
            self.moleculeJoueur.move()
            self.actualiser()
            #time.sleep(0.001)
        self.moleculeJoueur.pattern.mv_y = 0

        self.shootJoueur(self.choix,self.temps)
        while len(self.projectilesJoueur) > 0:
            for proj in self.projectilesJoueur:
                proj.move()
                if proj.dead:
                    self.projectilesJoueur.remove(proj)
            self.actualiser()

    def outroLevel(self):
        self.framesInvincibilite = 0
        pygame.mixer.music.load('resources/fanfare.wav')
        pygame.mixer.music.play(1)
        self.clearProj()
        self.play(3)
        self.moleculeJoueur.pattern.mv_y = -5
        self.moleculeJoueur.pattern.mv_x = 0
        while self.moleculeJoueur.dead == False:
            self.moleculeJoueur.move()
            self.actualiser()
        self.moleculeJoueur.reset()
        self.moleculeJoueur.pattern.mv_y = 0
            #time.sleep(0.001)

    def choixobjet(self):
        menu = Menu()
        menu.init(constantes.objets_dispo[0:constantes.niveauActuel], self.fenetre.fen,1)
        menu.position_affichage=(768/2-30*constantes.niveauActuel,200)
        menu.draw()
        pygame.key.set_repeat(199,69)
        pygame.display.update()
        choisi=False
        self.fenetre.afficherObjet(menu.get_position())
        #self.fenetre.afficherObjet(self.niveau.numero)
        while choisi==False:
            menu.draw()
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    menu.draw(-1)
                    self.fenetre.afficherObjet(menu.get_position())
                if event.key == K_RIGHT:
                    menu.draw(1)
                    self.fenetre.afficherObjet(menu.get_position())
                if event.key == K_RETURN or event.key == constantes.touches[0]:
                    choisi =True
                    self.choix=menu.get_position()
            pygame.display.update()
        choisi=False

    def traitement_objet(self,n,p):
        if p==0:
            if n==0:
                self.moleculeJoueur.img=pygame.image.load('resources/photos/superoger.png').convert_alpha()
                self.temps=500
                self.boost=2
                objet1.play()
            elif n==1:
                self.moleculeJoueur.img=pygame.image.load('resources/photos/bouclieroger.png').convert_alpha()
                self.moleculeJoueur.rect = self.moleculeJoueur.img.get_rect()
                self.temps=500
                self.boost=0.5
                self.vitesse=3
                self.score-=1000
            elif n==2:
                self.pluto=atome.Plutonium2(0,600,PatternPolynome(2/1000,5/1000,200))
                self.temps=10000000
                self.score-=1000
            """elif n==3:
            elif n==4:"""
        else :
            if n==0 or n==1:
                self.moleculeJoueur.img=pygame.image.load('resources/photos/hydrogene.png').convert_alpha()
                self.moleculeJoueur.rect = self.moleculeJoueur.img.get_rect()
                self.temps=-1000
                self.boost=1
                self.vitesse=4.5
            elif n==2:
                self.temps=-1000
            """elif n==3:
            elif n==4:"""


    def sauverpositions(self) :
        """
        rect=[]
        for ennemi in self.ennemyList:
            rect.append((ennemi.posX,ennemi.posY))
        with open("positions.pickle", 'wb') as file:
            pickle.dump([rect],file)
        """
        constantes.ennemis = self.ennemyList
