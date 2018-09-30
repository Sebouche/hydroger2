from PIL import Image
import atome
from random import *
from dialogue import Dialog
from atome import *
import copy
import constantes
from pattern import *
import pickle
import time
import niveau









def scenario1(t1,t2,tempspause,phase):
    dialog=0
    ennemi=[]
    temps=t2-t1-tempspause
    if temps<=3 and phase==2:
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiOxygene(0,0,0),PatternCibler(309,40)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiOxygene(768,0,0),PatternCibler(459,40)))
        phase=3
    if temps>7 and phase==3:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(0,100,0),Pattern(4,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(768,150,0),Pattern(-4,0)))
        phase=4
    if temps>10 and temps<=18 and phase==4:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(0,100,0),Pattern(4,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(768,150,0),Pattern(-4,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(0,100,0),Pattern(2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(768,200,0),Pattern(-2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(0,0,0),PatternPolynome(2/1000,5/1000,300)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(768,0,0),PatternPolynome(2/1000,5/1000,-300)))
        phase=5
    if temps>27 and temps<=29 and phase==5:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(0,200,0),PatternZigZag(0,300,2,20)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(768,250,0),PatternZigZag(768,350,-2,20)))
        phase=6
    if temps>29 and temps<=31 and phase==6:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Methane(384,0,0),Pattern(0,1)))
        phase=7
    if temps>33 and temps<=37 and phase==7:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Uranium(0,50,0),Pattern(1,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Uranium(768,550,0),Pattern(-1,0)))
        phase=8
    if temps>37 and temps<=40 and phase==8:
        phase=9
    if temps>40 and temps<=50 and phase==9:
        phase=True
    if phase==True:
        phase=True
    return ennemi,phase,dialog


def scenario2(t1,t2,tempspause,phase):
    ennemi=[]
    if phase==2:
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHiggs(300,50,0),Pattern(0,0)))
        phase=True
    else:
        phase=True
    return ennemi,phase,0