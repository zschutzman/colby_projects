

import numpy as np
import gurobipy as g
import random

class Site:
	def __init__(self, row, col, speciesVector, cost, variable = 0):
		
		self.row = row
		self.col = col
		self.speciesVector = speciesVector
		self.bdi = sum(speciesVector)
		self.var = variable
		self.value = self.var * self.bdi
		self.cost = cost * self.var
		self.spExpr = self.get_species_expression()
		
	def get_species_expression(self):
		ex = []
		for r in self.speciesVector:
			ex = ex + [r*self.var]
		return ex
		
		
	def assignVariable(self, var):
		self.var = var
		self.value = self.var * self.bdi
		self.cost = self.cost* self.var
		
	def get_connectedness(self, siteList):
		s = 0
		for n in getNeighbors(self, siteList):
			s = s + (self.var * n.var)
		return s
		

		
def getNeighbors(site, siteList):
	l = []
	
	for s in siteList:
		if s.row == site.row and (s.col == site.col - 1 or s.col == site.col + 1):
			l.append(s)
		if s.col == site.col and (s.row == site.row - 1 or s.row == site.row + 1):
			l.append(s)
	return l