import gurobipy as g
import xlwings as x
import numpy as np
import math

wb = x.Workbook()



siteNames = ["1","2","3","4"]
speciesNames = ["A","B","C"]

matrixData = [[1,0,1,1],[0,1,0,0],[0,0,1,1]]


# We want each inner list to be the complete data for a species (a column)



B = 2


# Start up the model
m = g.Model("setCovering")

# Create the decision variables
siteVars = []
for i in siteNames:
	siteVars.append(m.addVar(vtype = g.GRB.BINARY, name = "site%s" % i))

speciesVars = []
for i in speciesNames:
	speciesVars.append(m.addVar(vtype=g.GRB.BINARY, name = "species%s" % i))

	
m.update()

	
# Create the matrix for selection
def construct_variable_matrix():
	global matrixData
	global siteVars



	selVars = matrixData[:]
	for speciesCol in selVars:
		for i in range(len(speciesCol)):
			if speciesCol[i] == 1:
				speciesCol[i] = siteVars[i]
	
	return selVars
	
def countConserved():
	global varMat
	speciesVector = [False,False,False]
	for c in range(len(varMat)):
		print c
		ss = sum(varMat[c])
		if (ss == 1 or ss==2 or ss==3) == True:
			for i in varMat[c]:
				print
			# print "data", varMat[c]
			# print "sum", sum(varMat[c])
			# print "bool", (sum(varMat[c]) >= 0)
			speciesVector[c] = True
	
	print speciesVector
	s = sum(1 for status in speciesVector if status == True)
	print "s",s
	return s


def countConserved2():
	global varMat
	speciesVector = [0,0,0]
	for c in range(len(varMat)):
		
		speciesVector[c] = sum(varMat[c])

	return speciesVector

	
varMat = construct_variable_matrix()
	
m.setObjective(sum(speciesVars), g.GRB.MAXIMIZE)
cList = countConserved2()
#m.setObjective((sum(1 for cons in countConserved2() if math.ceil(cons/4.0) == 1)), g.GRB.MAXIMIZE)

m.addConstr(sum(siteVars) <= 2, 'budg')

for i in range(len(cList)):
	m.addConstr(cList[i] >= speciesVars[i], "specConst%s" % speciesNames[i])

m.update()
m.optimize()



for v in m.getVars():
  print ('%s %g' % (v.varName, v.x))
  print v.x == 1
print m.objVal
print ""
print ""
print construct_variable_matrix()
l = []
for i in siteVars:
	l.append([i.x])
print l
x.Range('A1').value = l