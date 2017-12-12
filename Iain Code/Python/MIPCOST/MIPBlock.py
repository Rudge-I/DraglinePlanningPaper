import numpy as np 
import gurobipy as G
import time as time
class Block:
	def __init__(self,Mine,Spoil,Dragline):
		self.Mine = Mine
		self.Spoil = Spoil
		self.Dragline= Dragline

	def set_Spoil(self,NewSpoil):
		self.Spoil = NewSpoil

	def get_Spoil(self):
		return self.Spoil

	def set_spoilvals(self,spoilcap,swell,expand):
		self.spoilcap = spoilcap
		self.swell = swell
		self.expand = expand

	def set_Block(self,start,end):
		self.start = start
		self.end = end
		self.N = range(start, end)
		if start-self.Dragline.get_reach() >= 0:
			stemp = start-self.Dragline.get_reach()
		else:
			stemp = 0
		if end+self.Dragline.get_reach()<= len(self.Spoil):
			etemp = end+self.Dragline.get_reach()
		else:
			etemp = len(self.Spoil)
		self.S = range(stemp,etemp)
		self.stemp = stemp
		self.etemp = etemp
	def killme(self):
		print(self.end-self.start,self.N,self.end-self.start+2*self.Dragline.get_reach(),self.S)

	def Calc_Valid(self):
		self.isValid = np.zeros((self.end-self.start+1,self.end-self.start+2*self.Dragline.get_reach()+1))
		for i in range(self.end-self.start):
			for j in range(i-self.Dragline.get_reach(),i+self.Dragline.get_reach()):
				self.isValid[i,j+self.Dragline.get_reach()] = 1
	def get_isValid(self):
		return self.isValid

	def MoveCost(self,n,s):
		if n == s:
			angle = 90
		if n>s: 
			angle = np.rad2deg(np.arctan(abs(n-s)/self.Dragline.get_reach()))+90
		if n<s: 
			angle = np.rad2deg(np.arctan(abs(n-s)/self.Dragline.get_reach()))

		return(angle*self.Dragline.get_swingtime())+17


	# def MoveCost(Movements,n,s):
	#     angle = 0 
	#     Prop = 15
	#     # Vangle = np.rad2deg(np.arctan(abs(H/(Cur-D)))) #Calculate the lift angle 
	#     if n == s: #The winch will turn 90 deg
	#         angle = 90
	#     if n>s: 
	#         angle = np.rad2deg(np.arctan(abs(n-s)/self.Dragline.get_reach()	))+np.rad2deg(np.arctan(abs(Cur-D)/20))+90
	#     if n<s:
	#         angle = np.rad2deg(np.arctan(abs(A-D)/20))+np.rad2deg(np.arctan(abs(Cur-D)/20))
	#     return angle*Prop+17+Prop*Vangle

	# def MoveCost(self,Movements,n,s):
		# return abs(n-s)*np.ceil(Movements)

	def MIP(self,output=0):
		m = G.Model()
		m.setParam('OutputFlag',output)
		M2S = {(n,s):m.addVar() for n in self.N for s in self.S}
		MCiel = {(n,s):m.addVar(vtype = G.GRB.INTEGER) for n in self.N for s in self.S}
		m.setObjective(G.quicksum((self.MoveCost(n,s)*MCiel[n,s]) for n in self.N for s in self.S),G.GRB.MINIMIZE)
		CreateCieling = {(n,s):M2S[n,s]<=MCiel[n,s] for n in self.N for s in self.S}
		OnlyifValid = {
		(n,s):m.addConstr(M2S[n,s]<= 100*self.isValid[n-self.start,s-self.start-self.Dragline.get_reach()]) for n in self.N for s in self.S
		}

		RemoveOnlyallowed = {
		(n):m.addConstr(G.quicksum(M2S[n,s]*self.Dragline.get_BucketVol() for s in self.S)==self.Mine[n]) for n in self.N
		}

		RemoveOnlyallowedCiel = {
		(n):m.addConstr(G.quicksum(MCiel[n,s]*self.Dragline.get_BucketVol() for s in self.S)>=self.Mine[n]) for n in self.N
		}
		spoilcapacity = {
		(s):m.addConstr(G.quicksum(M2S[n,s]*self.Dragline.get_BucketVol()*self.swell*self.expand for n in self.N)<=self.spoilcap)
		for s in self.S
		}
		m.optimize()
		self.cost = m.ObjVal
		# print(sum(M2S[16,s].x for s in self.S))
		self.potential_spoil = self.Spoil[:self.stemp]+[sum(M2S[n,s].x*self.Dragline.get_BucketVol()*self.swell*self.expand for n in self.N) for s in self.S]+self.Spoil[self.etemp:]


	def BlockCost(self,start,end,Spoil,output=0):
		if end>len(self.Mine):
			end = len(self.Mine)
			# print("Adjusting End Position")
		self.set_Spoil(Spoil)
		if output ==1:
			print("Spoil Set")
		self.set_Block(start, end)
		if output ==1:
			print("Block Set:\t" ,[start,end])
		self.Calc_Valid()
		if output ==1:
			print("Column Generation Done")
		stime = time.time()
		self.MIP(output)
		etime = time.time()-stime
		if output ==1:
			print("MIP Complete")
		return (self.cost,self.potential_spoil,etime)


