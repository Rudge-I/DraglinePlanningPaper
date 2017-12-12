import json
from DraglineClass import Dragline
from random import *
import matplotlib.pyplot as plt
from MIPBlock import Block
from StripCost import Strip
import numpy as np 
import time as time
import gurobipy as G
import Preproccesing as PrePro
Drag = Dragline(15, 30, 45, 10, 15, 30)



def MineGen(Len):
    M = []
    std = 2
    for i in range(Len):
        if i%7 ==0:
            seed(i)
            boop = randint(15,55)
        M.append(gauss(boop,std))
    return M



def BlankSpoil(Len):
	return [0 for i in range(Len)]

Mine = MineGen(100)
Spoil = BlankSpoil(100)
# BCK = Block(Mine, Spoil, Drag)
# BCK.set_spoilvals(98, 1.3,1.9)
# BCK.set_Block(15, 34)
# BCK.Calc_Valid()
# BCK.get_isValid()
# Res = BCK.BlockCost(15,34,Spoil)
# print(Res[0])
# print(len(Res[1]),len(Spoil))

STR = Strip(Mine, Spoil, Drag)
STR.BlockSettings(98,1.3,1.9)
# STR.printRange()
Starttime = time.time()
#STR.DP(0,100, Spoil)
STR.PrunedCost()
STR.getPrunedResults()
STR.SavePruneDict()

DPTime = time.time()-Starttime

with open('Runtime.txt','w') as file:
	file.write('Time Taken for Prune:{}'.format(DPTime))
# STR.GetDict()
#STR.SaveDict('Run_99.txt')
# A = {1:'one',2:'Two'}
# json.dump(A, open('filename.txt','w'))
