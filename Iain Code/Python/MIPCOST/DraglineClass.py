from gurobipy import *

class Dragline:
	def __init__(self,reach,swingtime,liftime,BucketVol,minBlock,maxBlock):
		self.reach = reach
		self.BucketVol = BucketVol
		self.swingtime = swingtime
		self.liftime = liftime
		self.minBlock = minBlock
		self.maxBlock = maxBlock


	def set_reach(self,reach):
		self.reach= reach

	def set_swingtime(self,swingtime):
		self.swingtime= swingtime

	def set_lifttime(self,liftime):
		self.liftime= liftime

	def set_BucketVol(self,BucketVol):
		self.BucketVol= BucketVol

	def get_reach(self):
		return self.reach

	def get_swingtime(self):
		return self.swingtime

	def get_lifttime(self):
		return self.liftime

	def get_BucketVol(self):
		return self.BucketVol

	def set_minBlock(self,minBlock):
		self.minBlock = minBlock

	def get_minBlock(self):
		return self.minBlock
	
	def set_maxBlock(self,minBlock):
		self.maxBlock = minBlock

	def get_maxBlock(self):
		return self.maxBlock






