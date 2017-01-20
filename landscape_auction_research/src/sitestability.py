import ast
import sys

def subsetMetric(subLS,superLS):
    
    
    tot = 0
    ovlp = 0.
    for i in range(len(subLS)):
        for j in range(len(subLS[0])):
            print subLS[i][j]
            if subLS[i][j]=='1':
                tot += 1
                if superLS[i][j] == 1:
                    ovlp += 1
    return ovlp/tot


def stabilMetric(subLS, listSuperLS):
    tot = 0
    for s in listSuperLS:
        tot += subsetMetric(subLS,s)
    
    return tot/len(listSuperLS)

f = open(sys.argv[1],'r')
scapes = f.readlines()
f.close()

for i in range(len(scapes)):
    scapes[i] = scapes[i].strip()
    print "Now",i
    print scapes[i]
    
    

for i in range(len(scapes)-1):
    print subsetMetric(scapes[i],scapes[i+1])
    

    