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
        ennemi.append(niveau.Niveau.genererMob(0,atome.Soufre(0,100,0),Pattern(0.75,0.2)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Soufre(768,100,0),Pattern(-0.75,0.2)))
        phase=3
    if temps>9 and phase==3:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Uranium2(370,0,0),Pattern(0,0.5)))
        phase=4
    if temps>19 and temps<=24 and phase==4:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Oxygene(0,0,0),PatternPolynome(2/1000,5/1000,300)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Oxygene(768,0,0),PatternPolynome(2/1000,5/1000,-300)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(0,100,0),Pattern(1,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(768,200,0),Pattern(-1,0)))
        phase=5
    if temps>30 and temps<=32 and phase==5:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(0,100,0),Pattern(2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(768,125,0),Pattern(-2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(0,150,0),Pattern(2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(768,175,0),Pattern(-2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Azote(0,300,0),PatternZigZag(0,300,1,20)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Azote(768,350,0),PatternZigZag(768,350,-1,20)))
        phase=6
    if temps>36 and temps<=39 and phase==6:
        phase=7
    if temps>39 and temps<=42 and phase==7:
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(242,0,0),Pattern(0,0.5)))
        phase=8
    if temps>45 and temps<=49 and phase==8:
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(384,0,0),Pattern(0,0.5)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(668,0,0),Pattern(0,0.5)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(0,150,0),Pattern(0.5,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHydrogene(768,200,0),Pattern(-0.5,0)))
        phase=9
    if temps>50 and temps<=55 and phase==9:
        phase=True
    if phase==True:
        phase=True
    return ennemi,phase,dialog


def scenario2(t1,t2,tempspause,phase):
    ennemi=[]
    if phase==2:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Faille(200,30,0),Pattern(0,0)))
        phase=True
    else:
        phase=True
    return ennemi,phase,0