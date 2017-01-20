

import numpy as np
import gurobipy as g

class Site:
	def __init__(self, row, col, speciesVector, variable = 0):
		
		self.row = row
		self.col = col
		self.speciesVector = speciesVector
		self.bdi = sum(speciesVector)
		self.var = variable
		self.value = self.var * self.bdi
		
		
	def assignVariable(self, var):
		self.var = var
		self.value = self.var * self.bdi
		
	def get_connectedness(self):
		s = 0
		for n in getNeighbors(self):
			s = s + (self.var * n.var)
		return s
		

		
def getNeighbors(site, siteList):
	l = []
	
	for s in sitesList:
		if s.row == site.row and (s.col == site.col - 1 or s.col == site.col + 1):
			l.append(s)
		if s.col == site.col and (s.row == site.row - 1 or s.row == site.row + 1):
			l.append(s)
	return l