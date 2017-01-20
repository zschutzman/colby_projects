import gurobipy as g
import xlwings as x
import numpy as np

# Read in Excel data
wb = x.Workbook(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\speciesBinaryMatrix.csv')
siteNames = x.Range('A2:A1170').value

matrixData = x.Range('B2:RJ1170').value

def meets_condition(x):
	if sum(x)>=1:
		return True
	else:
		return False

# We want each inner list to be the complete data for a species (a column)
matrixData = np.asarray(matrixData).T.tolist()


B = 5


# Start up the model
m = g.Model("setCovering")

# Create the decision variables
siteVars = []
for i in siteNames:
	siteVars.append(m.addVar(vtype = g.GRB.BINARY, name = "site%s" % i))

	
m.update()

	
# Create the matrix for selection
def construct_variable_matrix():
	global matrixData
	global siteVars
	
	selVars = []
	
	for species in matrixData:
		l = []
		for i in range(1169):
			l.append(species[i] * siteVars[i])
		selVars.append(l)
	
	return selVars
	

m.addConstr(sum(siteVars) == B, 'budg')

m.update()


m.setObjective((sum(1 for speciesCol in construct_variable_matrix() if meets_condition(speciesCol))), g.GRB.MAXIMIZE)

m.update()


m.optimize()

print sum(siteVars)


	

	




