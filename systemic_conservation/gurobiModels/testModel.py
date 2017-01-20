import gurobipy as gp
m = gp.Model('testModel')

s = [1,2,0,4,3,2]

vars = []

for i in range(6):
    vars.append(m.addVar(vtype = gp.GRB.BINARY, name = "site%s" % i))


m.update()

print sum(s)

dec = []
for i in range(len(vars)):
    dec.append(vars[i] * s[i])

m.update()

x = vars[0]


m.setObjective(sum(dec), gp.GRB.MAXIMIZE)

m.addConstr(sum(vars) <= 2, 'budg')

m.update()

m.optimize()

for v in m.getVars():
  print ('%s %g' % (v.varName, v.x))

print('obj:  %g' % m.objVal)





