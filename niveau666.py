import atome
from dialogue import Dialog
from pattern import *
import pickle
import time
import niveau




def scenario1(t1,t2,tempspause,phase):
    dialog=0
    ennemi=[]
    temps=t2-t1-tempspause
    if temps<=3 and phase==2:
        #ennemi.append(niveau.Niveau.genererMob(0,atome.AntiHiggs(300,50,0),PatternComplexe([[PatternPolynome(2/1000,5/1000,50),50],[PatternCibler(500,500),1]])))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene(0,0,0),PatternPolynome(2/1000,5/1000,50)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene(768,0,0),PatternPolynome(2/1000,5/1000,-100)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene(0,0,0),PatternPolynome(2/1000,5/1000,150)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene(768,0,0),PatternPolynome(2/1000,5/1000,-200)))
        phase=3
    if temps>6.5 and phase==3:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(370,0,0),Pattern(0,1)))
        phase=4
    if temps>10 and temps<=15 and phase==4:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Oxygene(0,0,0),PatternPolynome(2/1000,5/1000,300)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Oxygene(768,0,0),PatternPolynome(2/1000,5/1000,-300)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(0,100,0),Pattern(1,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Chlore(768,200,0),Pattern(-1,0)))
        phase=5
    if temps>16 and temps<=25 and phase==5:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(0,100,0),Pattern(2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(768,125,0),Pattern(-2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(0,150,0),Pattern(2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Hydrogene2(768,175,0),Pattern(-2,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Azote(0,300,0),PatternZigZag(0,300,1,20)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Azote(768,350,0),PatternZigZag(768,350,-1,20)))
        phase=6
    if temps>25 and temps<=30 and phase==6:
        phase=7
        dialog=1
    if temps>30 and temps<=35 and phase==7:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(242,0,0),Pattern(0,0.5)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(526,0,0),Pattern(0,0.5)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(0,50,0),Pattern(0.5,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(768,100,0),Pattern(-0.5,0)))
        phase=8
    if temps>35 and temps<=40 and phase==8:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(384,0,0),Pattern(0,0.5)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(668,0,0),Pattern(0,0.5)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(0,150,0),Pattern(0.5,0)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Carbone(768,200,0),Pattern(-0.5,0)))
        phase=9
    if temps>55 and temps<=70 and phase==9:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Methane(50,0,0),PatternCibler(100,50)))
        ennemi.append(niveau.Niveau.genererMob(0,atome.Methane(710,0,0),PatternCibler(660,50)))
        phase=10
    if temps>70 and temps<=75 and phase==10:
        phase=True
    if phase==True:
        phase=True
    return ennemi,phase,dialog


def scenario2(t1,t2,tempspause,phase):
    ennemi=[]
    if phase==2:
        ennemi.append(niveau.Niveau.genererMob(0,atome.Diamant(300,0,0),Pattern(0,0)))
        phase=True
    else:
        phase=True
    return ennemi,phase,0