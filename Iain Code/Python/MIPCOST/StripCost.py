import json
# from tqdm import tqdm 
from MIPBlock import Block
from DraglineClass import Dragline
from Preproccesing import PrePro
import time as time 
class Strip:
	def __init__(self,Mine,Spoil,Dragline):
		self.Mine = Mine
		self.Spoil = Spoil
		self.Dragline = Dragline
		self.Blk = Block(self.Mine,self.Spoil,self.Dragline)
		print('Pruning Starting')
		ST = time.time()
		self.Prune = PrePro(0,len(self.Mine),self.Dragline.get_minBlock(),self.Dragline.get_maxBlock())
		self.Prunelst = self.Prune.Prune()
		print('Pruning Completed in:\t',time.time()-ST,' seconds')
		self.dict = {}
		self.prunedict = {}
		self.Prunefinal = {}
		self.count = 0

	def BlockSettings(self,spoilcap,swell,expand):
		self.Blk.set_spoilvals(spoilcap,swell,expand)

	def DP(self,position,end,spoil):
		self.count +=1
		print("Resource Constrained Dynamic Program \t Called:\t",self.count,'  times')
		print("Distance Remainging  :\t" ,end-position)
		if position>end-self.Dragline.get_minBlock():
			position = end
			# print("FUCK")
			return (10000000000000000000000000,0,[])

		if position == end:
			# print(value, sep, end, file, flush)
			return (0,0,[])
		# if end <= position:
			# self.dict[position,end,str(spoil)] = 100000000
			# return self.dict[position,end,str(spoil)]
		if (position,end,str(spoil)) not in self.dict:
			self.dict[position,end,str(spoil)] = min((10000+self.Blk.BlockCost(position,position+Action,spoil)[0]+
				self.DP(position+Action,end,self.Blk.BlockCost(position,position+Action,spoil)[1])[0]
				,Action,self.Blk.BlockCost(position,position+Action,spoil)[1])
			for Action in range(self.Dragline.get_minBlock(),self.Dragline.get_maxBlock()))
		return self.dict[position,end,str(spoil)]

	def PrunedCost(self):
		counter = 0
		for solution in (self.Prunelst):
			counter+=1
			if counter %100 == 0:
			    print('Percent Complete:\t',counter/len(self.Prunelst)*100,'%')
			for Block in range(len(solution)):
				position = sum([solution[i] for i in range(Block)])-solution[Block]
				combo = ''
				if Block > 0:
					combo = str([solution[i] for i in range(Block-1)])
				if combo in self.prunedict:
					oldspoil = self.prunedict[combo][1]
					blockcalc = self.Blk.BlockCost(position,position+solution[Block],oldspoil)
					cost = self.prunedict[combo][0]+blockcalc[0]+10000
				else:
					oldspoil = self.Spoil
					blockcalc = self.Blk.BlockCost(position,position+solution[Block],oldspoil)
					cost = blockcalc[0]+10000
				newcombo = str([solution[i] for i in range(Block)])
				self.prunedict[newcombo] = [cost,blockcalc[1]]
			self.Prunefinal[str(solution)] = self.prunedict[str([solution[i] for i in range(Block)])]
		
	def getPrunedResults(self):
		sortprune= sorted(self.Prunesinal, key = lambda key: d[key][0])
		print('Optimal Cost:\t',self.Prunefinal[sortprune[0]])
		print('Optimal Method:\t',sortprune[0])				

	def GetDict(self):
		return self.dict
	def SaveDict(self,filename='RCDP_Out.txt'):
		json.dump(self.dict, open(filename,'w'))

	def SavePruneDict(self,filename='Prune_Out.txt'):
		json.dump(self.Prunefinal, open(filename,'w'))
	def LoadDict(self,filename='RCDP_Out.txt'):
		self.dict = json.load(open(filename))

	def ReturnOptimalSolution(self):
		return None 

	def printRange(self):
		print(self.Dragline.get_minBlock(),self.Dragline.get_maxBlock())




