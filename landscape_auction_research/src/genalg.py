#genalg.py

import math
import sys
import randomSeeded
import landscape
import time
from multiprocessing import Process
import copy


class Solver:
    def __init__(self, ls, obj = "ValMax", constr = sys.maxsize):
        
        self.ls = ls
        self.numSites = ls.size * ls.size
        self.siteMap = list(self.ls.map)
        self.siteMapCopy = list(self.siteMap)
        
        self.sites = []
        for i in range(ls.size):
            for j in range(ls.size):
                self.sites.append(self.siteMap[i][j])
        
        self.objective = obj
        self.constraint = constr
        
        if self.objective == "ValMax":
            self.bound = self.valmax_bound()
        
        self.solTemp = [0] * self.numSites
        self.curSols = []
        self.survSols = []
        
        self.bestSols = []
                       
            
    def valmax_bound(self):
        
        self.sites.sort(key=lambda x: x.privateVal)
        
        siteCount = 0
        cost = 0
        while cost <= self.constraint:
            s = self.sites[siteCount]
            cost = cost + s.privateVal
            siteCount += 1
            
        return siteCount

    def generate_random_map(self,sels):
        
        unshuff = [1]*sels + [0]*(225-sels)
        randomSeeded.random.shuffle(unshuff)
        randMap = [unshuff[k:k+15] for k in range(0,len(unshuff),15)]
        
        return randMap
    def stable(self, c, v):
        
        if abs((self.prevCost - float(c))/c) < .0075 and abs((self.prevVal - float(v))/v) < .0075:
            return True
        return False
        
    def valmax_sol2(self):
        
        rands = []
        self.curSols = []
        
        if self.survSols == []:
#             a = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]
#             self.ls.map_to_choose(a)
#             rands.append((a,self.ls.getEnvVal(),self.ls.getCost(),'a'))
            for i in range(self.bound):
                for j in range(20):
                    m = self.generate_random_map(i+1)
                    self.ls.map_to_choose(m)
                    rands.append((m,self.ls.getEnvVal(),self.ls.getCost(),'r'))
                    
            rands.sort(key = lambda x: x[1], reverse = True)
            rands = [t for t in rands if t[2] <= self.constraint]
            mvc = rands[:]
#             print "initial randoms generated, sorted, and filtered"
        
        
            mvc.sort(key = lambda x: x[1], reverse = True)        
            p = min(150, len(mvc))
            gen_cur = mvc[:p]
            self.survSols = gen_cur[:]
            
        for s in self.survSols[:25]:
            if s[0] not in [c[0] for c in self.survSols[:25]]:
                self.curSols.append(s)
            
        
        
        p = len(self.survSols)
        pmap = [s[0] for s in self.survSols]
        for i in range(len(pmap)):
            pmap[i] = [val for sublist in pmap[i] for val in sublist]   
        
        pmap = [sum(x) for x in zip(*pmap)]
        pmap = [x/float(p) for x in pmap]
        
#         print "probabilities generated" 
        
        probMaps = []
        while len(probMaps) < 50:
            probs = [randomSeeded.random.random() for i in range(225)]
            for r in xrange(225):
                if probs[r] < pmap[r]:
                    probs[r] = 1
                else:
                    probs[r] = 0
            probs = [probs[k:k+15] for k in range(0,len(probs),15)]
            self.ls.map_to_choose(probs)
            if self.ls.getCost() <= self.constraint:
                probMaps.append(probs)
        
        for m in probMaps:
            self.ls.map_to_choose(m)
            self.curSols.append((m,self.ls.getEnvVal(),self.ls.getCost(),'p'))
        
#         print "probabilistic solutions generated"
         
        rands = []
        for i in range(self.bound,self.bound/2,-1):
            for j in range(25):
                m = self.generate_random_map(i)
                self.ls.map_to_choose(m)
                rands.append((m,self.ls.getEnvVal(),self.ls.getCost(),'r'))
                 
        rands.sort(key = lambda x: x[1], reverse = True)
        rands = [t for t in rands if t[2] <= self.constraint]
         
        self.curSols = self.curSols + rands[:75]
         
#         print "random solutions generated"
        
        
        
        ######
        tSols = self.survSols[:min(25,len(self.survSols)-1)]
        count = 0
        gt = time.time()
        for s in tSols:
            self.prevCost = sys.maxsize
            self.prevVal = sys.maxsize
            if count == 1:
                pass
#                   print "one greedy time: ", time.time() - gt
            count += 1
#             print count, " greedy"
            self.ls.map_to_choose(s[0])
            loops = 0
            while self.ls.getCost() <= self.constraint and loops < 7:
                loops += 1
#                 print "stability: ", self.stable(self.ls.getCost(), self.ls.getEnvVal())
                self.prevCost = self.ls.getCost()
                self.prevVal = self.ls.getEnvVal()
#                 print "loops: ", loops
#                 print self.ls.getCost(), self.ls.getEnvVal()
                self.ls.greedyOptimize()
                self.ls.updateEnvVal()
            
            count = 0
            while self.ls.getCost() > self.constraint:
  
                self.ls.greedyReduce()
               
                
            while (self.ls.getCost() + 12 <= self.constraint) and count < 7:
#                 print "greedy add: ",count
#                 print "cost, value, numsites: ", self.ls.getCost(), self.ls.getEnvVal(), sum([sum(l) for l in self.ls.choose_to_map()])
                count += 1
                self.ls.updateEnvVal()
                if self.ls.greedyAdd() == None:
                    continue
                
                
            self.curSols.append((self.ls.choose_to_map(),self.ls.getEnvVal(),self.ls.getCost(),'g'))
            
        
        
#         print "greedily modified solutions generated"
        #######
        
        
        self.curSols.sort(key = lambda x: x[1], reverse = True)
        stt = time.time()
        sol_maps = [s[0] for s in self.survSols]
        
        mut_genes = []
        for i in range(25):
            x = randomSeeded.random.betavariate(1,5)
            ind = len(self.survSols)-1
            ind = ind*x
            ind = int(ind)

            mut_genes.append(ind)
#         print "mutation selections:", mut_genes
        drt = time.time()
        
#         print "draw time: ", drt-stt   
            
#         print "sol_maps length", len(sol_maps)
   
        mut_sol_maps = []
        
        for i in mut_genes:

            mut_sol_maps.append(sol_maps[i])

        
            for m in mut_sol_maps:
                d = randomSeeded.numpy.random.binomial(225,.08)
                for i in range(d):
                    m[randomSeeded.random.randint(0,14)][randomSeeded.random.randint(0,14)]
                self.ls.map_to_choose(m)         
                self.curSols.append((m,self.ls.getEnvVal(),self.ls.getCost(),'m'))             
                
                
        tmt = time.time()
#         print "total mutation time: ", tmt-stt
        
        self.curSols.sort(key = lambda x: x[1], reverse = True)
        self.curSols = [t for t in self.curSols if t[2] <= self.constraint]
        
        
        i = 0
        while i < len(self.curSols):
            if self.curSols[i][0] not in [c[0] for c in self.bestSols]:
                self.bestSols.append(self.curSols[i])
                break
            i += 1
        self.survSols = self.curSols[:min(150,len(self.curSols))]
               
        
#         print "FINISHED", [s[1] for s in self.curSols[:15]]
        
   
 

def main(constraintVal):
    
    global ls
    t1 = time.time()
    copyScape = copy.copy(ls)
    
    solver = Solver(copyScape, constr = constraintVal)
    
    print solver.bound, "bound"
    mrp = (0,0)
    while (solver.ls.getCost() < solver.constraint) and mrp != (-1,-1):
        mrp = solver.ls.greedyAdd()
  
        solver.ls.updateEnvVal()
    if solver.ls.getCost() > solver.constraint:
        print "IT HAPPENED", mrp
        solver.ls.unchooseSite(mrp)
        solver.ls.updateEnvVal()
              
          
    gc = solver.ls.getCost()
    gv = solver.ls.getEnvVal()
    print "Greedy cost, greedy val",gc,gv
  
    print "greedyMap", solver.ls.choose_to_map()
    t2 = time.time()  
    print "GREEDY TIME: ",t2-t1
    a = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]
   
    print "sum", sum([sum(x) for x in a])
    solver.ls.map_to_choose(a)
       
    solver.ls.printEnvVal()
    print solver.ls.getEnvVal()
    print solver.ls.getCost()
    print "cosnstr type", type(solver.constraint)
    print "cost type", type(solver.ls.getCost())
#     start = time.time()
#      
#     global it
#      
#     for i in range(7):
#         print "iteration", i
#         it = i
#         solver.valmax_sol2()
#         solver.bestSols.sort(key = lambda x: x[1], reverse = True)
#         #print solver.bestSols[0][1:]
#     print [s[1:] for s in solver.bestSols]
#          
#     stop = time.time()
#          
#     print "time: ", stop-start
#     print "constraint", solver.constraint
#     print solver.bestSols[0]
#         
#     solver.ls.map_to_choose(solver.bestSols[0][0])
#         
#     return solver.ls   
ls = landscape.Landscape(15)
def mainLoop():
    Pros = []
    

    for i in range(50):
        l = 325+(i*25)
        p = Process(target = main,args=(l,))
        Pros.append(p)
        p.start()
 
    for t in Pros:
        t.join()      
   
       
if __name__ == "__main__":
    print randomSeeded.seed
    mainLoop()
 
    import winsound
    winsound.Beep(554,1000)    
                        

    