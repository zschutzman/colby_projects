import gurobipy as g
import xlwings as x
import numpy as np

import timeit
start = timeit.default_timer()

# Read in Excel data

print "Reading in data from Excel ..."
wb = x.Workbook(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\fake_site_data.csv')
siteNames = x.Range('B5:B2504').value
speciesNames = x.Range('F1:IU1').value

speciesPresence = x.Range('F3:IU3').value




matrixData = x.Range('F5:IU2504').value

	
wb.close()
def meets_condition(x):
	if sum(x)>=1:
		return True
	else:
		return False

# We want each inner list to be the complete data for a species (a column)
matrixData = np.asarray(matrixData).T.tolist()


B = 16



	
# Start up the model
print "Setting up model ..."
m = g.Model("setCovering")

# Create the decision variables
print "Creating decision variables ..."
siteVars = []
for i in siteNames:
	siteVars.append(m.addVar(vtype = g.GRB.BINARY, name = "site%s" % i))

speciesVars = []
for i in speciesNames:
	speciesVars.append(m.addVar(vtype=g.GRB.BINARY, name = "species%s" % i))
	
	
m.update()

	
# Create the matrix for selection
def construct_variable_matrix():
	print "Constructing variable matrix ..."
	global matrixData
	global siteVars
	
	selVars = []
	speciesVector = []
	
	for species in matrixData:
		l = []
		for i in range(len(siteVars)):
			l.append(species[i] * siteVars[i])
		selVars.append(l)
		speciesVector.append(sum(l))
	return selVars,speciesVector
	

m.addConstr(sum(siteVars) == B, 'budg')

m.update()


varMat,cList = construct_variable_matrix()

def count_conserved():
	print "Constructing species vector ..."
	global varMat
	
	speciesVector = []

	for c in range(len(varMat)):
		
		speciesVector.append(sum(varMat[c]))

	return speciesVector

	

print "Constructing connectedness metric (Perimeter) ..."
E = 0

# Compile the neighbors list
for i in range(len(siteVars)):

	# Not on the left edge...
	if i % 50 != 0:
		# Add the right neighbor
		E = E + (siteVars[i]*siteVars[i-1])
	
	# Not on the left edge...	
	if i % 50 != 49:
		# Add the right neighbor
		E = E + (siteVars[i]*siteVars[i+1])
		
	# Not on the top edge...
	if i / 50 != 0:
		# Add the up neighbor
		E = E + (siteVars[i]*siteVars[i-50])
	
	# Not on the bottom edge...	
	if i / 50 != 49:
		# Add the down neighbor
		E = E + (siteVars[i]*siteVars[i+50])
		


# alpha is the adjustable weight term.  We can then solve an equation on
# two objectives as a(x) + (1-a)(y).  Alpha is between 0 and 1, inclusive.
alpha = .1

print "Adding species constraints ..."
for i in range(len(cList)):
	m.addConstr(cList[i] >= speciesVars[i], "specConst%s" % speciesNames[i])

	
m.addConstr(sum(speciesVars) >= 50)

print "Optimizing ..."
print "alpha = ",alpha
m.setObjective(E, g.GRB.MAXIMIZE)

m.update()
m.optimize()


# Create an empty array to dump into excel
print "Gathering results ..."
spatialRep = []
for i in range(50):
	l = []
	for j in range(50):
		l.append(0)
	spatialRep.append(l)


	
for v in siteVars:
	if v.x == 1:
		siteNum = int(float((v.varName[4:])))
		print siteNum
		spatialRep[siteNum%50][siteNum/50] = 1
		

dst = x.Workbook(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\fake_site_data_tar.xlsx')
x.Range('A1').value = spatialRep
x.Range('A53').value = "Alpha:"
x.Range('B53').value = alpha
x.Range('A55').value = "Budget:"
x.Range('B55').value = B
x.Range('A57').value = "Conserved:"
s = 0
for v in speciesVars:
	s = s+v.x
x.Range('B57').value = s

stop = timeit.default_timer()
print "TIME: ",stop-start