## max connectedness constrained to number of species preserved (no value)
## pick sites ignorant of cost
## do we care about max connectedness given a budget


## MODEL FOR 400 SITES, 125 SPECIES

import xlwings as x
import gurobipy as g
import numpy as np
import siteClass
import sys


def modelSolve(B, alpha, filetag =  None):
	
	if filetag == None:
		filetag = '%d_%d' % (B, alpha)
	
	print "Reading in data from Excel ..."
	# Open data workbook
	wb = x.Workbook(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\fake_site_data_smaller.csv')

	# Extract the data
	siteNames = x.Range('B5:B404').value
	siteXcoords = x.Range('E5:E404').value
	siteYcoords = x.Range('F5:F404').value

	costs = x.Range('C5:C404').value
	speciesNames = x.Range('G1:EA1').value
	speciesPresence = x.Range('G3:EA3').value
	matrixData = x.Range('G5:EA404').value

	# Close data workbook
	wb.close()

	# Manipulate the data to reflect species values
	matrixData = np.asarray(matrixData).T
	speciesPresence = np.asarray(speciesPresence)
	matrixData = matrixData/speciesPresence[:,None]


	# matrixData is now in the same format as the original data, with each inner list (row)
	# as the complete species data for each site.
	matrixData = matrixData.T

	# Initialize the model
	m = g.Model("BDI Clustering")

	# Construct the site objects and variables
	print "Constructing site objects ..."
	sites = []
	siteVars = []
	costVars= []
	for i in range(len(siteNames)):
		v = m.addVar(vtype = g.GRB.BINARY, name = "site_no_%s" % siteNames[i])
		siteVars.append(v)
		sites.append(siteClass.Site(siteXcoords[i], siteYcoords[i], matrixData[i], costs[i], v))
	for s in sites:
		costVars.append(s.cost)

	m.update()
		
	# Get the connectedness and BDI expressions
	print "Constructing connectedness and BDI expressions ..."
	connExpr = 0
	bdiExpr = 0
	for s in sites:
		connExpr = connExpr + s.get_connectedness(sites)
		bdiExpr = bdiExpr + s.value
		
	m.update()




	# Budget
	m.addConstr(sum(siteVars) == B)
	#Budget constraint
	m.update()
	m.remove(m.getConstrs()[0])
	m.addConstr(sum(costVars) == B)

	print "SOLVING.  ALPHA = ",alpha, "BUDGET = ",B

	m.update()
	m.setObjective((alpha)*(connExpr) + (1-alpha)*(bdiExpr), g.GRB.MAXIMIZE)
	m.update()
	m.optimize()




	# Construct output matrix
	print "Constructing Excel output ..."
	spatialRep = []
	for i in range(20):
		l = []
		for j in range(20):
			l.append(0)
		spatialRep.append(l)
		
	for v in siteVars:
		if v.x == 1:
			siteNum = int(float((v.varName[8:])))
			spatialRep[siteNum%20][siteNum/20] = 1

	wb = x.Workbook(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\fake_site_data_tar.xlsx')

	x.Range('A1').value = spatialRep
	x.Range('X1').value = B
	x.Range('X2').value = connExpr.getValue()
	x.Range('X3').value = bdiExpr.getValue()
	x.Range('X4').value = alpha

	wb.save(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\results\fake_site_data_tar_%s.xlsx' % filetag)
	r = x.Workbook(r'C:\Users\zachary\Dropbox\Summer Research Systematic Conservation SHARED\gurobiModels\results\fake_site_data_tar_%s.xlsx' % filetag)
	r.close()

	
if __name__ == '__main__':
	modelSolve(int(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
