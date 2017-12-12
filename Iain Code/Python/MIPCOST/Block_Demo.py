from DraglineClass import Dragline
from random import *
import matplotlib.pyplot as plt
from MIPBlock import Block
from StripCost import Strip
import numpy as np 
import gurobipy as G
import matplotlib.pyplot as plt

Drag = Dragline(15, 30, 45, 10, 10, 30)



def MineGen(Len):
	M = []
	std = 2
	for i in range(Len):
		# boop = 17
		if i%18 ==0:
			seed(i)
			boop = randint(15,32)
			# boop = 32
		M.append(gauss(boop,std))
	return M



def BlankSpoil(Len):
	return [0 for i in range(Len)]

# Mine = MineGen(50)
# Spoil = BlankSpoil(50)

# BCK = Block(Mine, Spoil, Drag)
# BCK.set_spoilvals(98, 1.3,1.9)
# BCK.set_Block(15, 34)
# BCK.Calc_Valid()
# BCK.get_isValid()
def BlockDemo(start,end):
	Res = BCK.BlockCost(start,end,Spoil)
	# print("--------------------------------------------------------------------------")
	print("Cost of Block:\t",Res[0],'s\n')
	print("Time in MILP:\t", Res[2],'s')
	fig = plt.figure(1)
	plt.subplot(211)
	# print(Res[1])
	plt.plot([i for i in range(50)],Mine,'b-',\
		[start for i in range(round(max(Mine))+5)],[i for i in range(round(max(Mine))+5)],\
		'r--',[end for i in range(round(max(Mine))+5)],[i for i in range(round(max(Mine))+5)],'r--')
	plt.title("Block Cut Example [{} to {}]".format(start,end))
	plt.ylabel("Average Depth (m)")
	plt.xlabel('Mine Section (m)')
	plt.subplot(212)
	plt.title('Resulting Spoil [{} to {}]'.format(start,end))
	plt.ylabel('Spoil Capacity (%)')
	plt.xlabel('Mine Section (m)')
	plt.plot([i for i in range(50)],Res[1],'b-',\
		[start for i in range(100)],[i for i in range(100)],\
		'r--',[end for i in range(100)],[i for i in range(100)],'r--')
	fig.tight_layout()
	plt.show()

# BlockDemo(15, 34)
# BlockDemo(20, 40)
print("Generating")
Mine = MineGen(200)
plt.plot([i for i in range(200)],Mine,'b-')
plt.title("Generated Mine (Random)")
plt.ylabel("Average Depth (m)")
plt.xlabel('Mine Section (m)')
plt.show()