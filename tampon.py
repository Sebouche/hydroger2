import niveau1
import niveau2
import niveau3
import niveau4
import niveau5
import niveau666

def Tampon1(niveau,debut,current,tempspause,phase) :
    if niveau==1:
        genere,phase,dialog=niveau1.scenario1(debut,current,tempspause,phase)
    if niveau==2:
        genere,phase,dialog=niveau2.scenario1(debut,current,tempspause,phase)
    if niveau==3:
        genere,phase,dialog=niveau3.scenario1(debut,current,tempspause,phase)
    if niveau==4:
        genere,phase,dialog=niveau4.scenario1(debut,current,tempspause,phase)
    if niveau==5:
        genere,phase,dialog=niveau5.scenario1(debut,current,tempspause,phase)
    if niveau==666:
        genere,phase,dialog=niveau666.scenario1(debut,current,tempspause,phase)
    return genere,phase,dialog

def Tampon2(niveau,debut,current,tempspause,phase) :
    if niveau==1:
        genere,phase,dialog=niveau1.scenario2(debut,current,tempspause,phase)
    if niveau==2:
        genere,phase,dialog=niveau2.scenario2(debut,current,tempspause,phase)
    if niveau==3:
        genere,phase,dialog=niveau3.scenario2(debut,current,tempspause,phase)
    if niveau==4:
        genere,phase,dialog=niveau4.scenario2(debut,current,tempspause,phase)
    if niveau==5:
        genere,phase,dialog=niveau5.scenario2(debut,current,tempspause,phase)
    if niveau==666:
        genere,phase,dialog=niveau666.scenario1(debut,current,tempspause,phase)
    return genere,phase,dialog