#landscape.py

'''
Created on Sep 17, 2015

@author: zachary
'''
import site
import sys


class Landscape:
    '''
    classdocs
    '''
 
 
    def __init__(self, size):
        '''
        Constructor
        '''
        self.heldSite = None
        self.map = []
        m = 0
        for i in range(size):
            row = []
            for j in range(size):
                k = site.Site((i,j),m)
                row.append(k)
                m = m+1
            self.map.append(row)
        self.size = size
        self.buildNeighbors()
    
    def clone(self):
        newScape = Landscape(self.size)
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                newScape.map[i][j] = site.cloneSite(self.map[j][i])
        
        return newScape
                
    
    def getSite(self,loc):
        return self.map[loc[0]][loc[1]]
    
    def chooseSite(self,loc):
        s = self.map[loc[0]][loc[1]]
        s.choose()
    def unchooseSite(self,loc):
        s = self.map[loc[0]][loc[1]]
        s.unchoose()
        
    def unchooseAll(self):
        for l in self.map:
            for s in l:
                s.unchoose()
    
    def buildNeighbors(self):
        for i in range(self.size):
            for j in range(self.size):
                n = []
                
                try:
                    n.append(self.getSite((i,j-1)))
                except IndexError:
                    pass
                try:
                    n.append(self.getSite((i-1,j)))
                except IndexError:
                    pass
                try:
                    n.append(self.getSite((i+1,j)))
                except IndexError:
                    pass
                try:
                    n.append(self.getSite((i,j+1)))
                except IndexError:
                    pass
             
              
                self.getSite((i,j)).addNeighbors(n)
    def updateEnvVal(self):
        for i in range(len(self.map)):
            for j in range(len(self.map)):
               self.getSite((i,j)).updateValue()
                
                
    def getEnvVal(self):
        self.updateEnvVal()
        enVal = 0
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                enVal = enVal + self.getSite((i,j)).getCurValLS()
        return enVal
    
    def getCost(self):
        cost = 0
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                cost = cost + self.getSite((i,j)).getPrivateValueLS()
        return cost
    
    def printEnvVal(self):
        print self.getEnvVal()
        print self.getCost()
        
    def map_to_choose(self,map):

        self.unchooseAll()
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 1:
                    self.chooseSite((i,j))
        self.updateEnvVal()
    
    def choose_to_map(self):
        
        return [[int(s.getPicked()) for s in l] for l in self.map]
        
    def updateMargVals(self):
        
        for l in self.map:
            for s in l:
                st = s.getPicked()
                s.choose()
                m = self.getEnvVal()
                s.unchoose()
                m = m - self.getEnvVal()
                s.marginalVal = m
                
                if st:
                    s.choose()
                

    
       
    def greedyOptimize(self):

        self.updateMargVals()
        self.updateEnvVal()
        
        maxMargVal = -.01
        maxSite = None
        s = None
        
        minMargVal = 1000000
        minSite = None

        
        for i in range(self.size):
            for j in range(self.size):
                s = self.getSite((i,j))
                if not s.getPicked():
                    if (s.marginalVal-s.privateVal) > maxMargVal:
                        maxMargVal = s.marginalVal-s.privateVal
                        maxSite = s
                if s.getPicked():
                    if (s.marginalVal -s.privateVal) < minMargVal:
                        minMargVal = s.marginalVal - s.privateVal
                        minSite = s

        if minMargVal < maxMargVal:
            minSite.unchoose()
            maxSite.choose()

    def greedyReduce(self):
        
        self.updateMargVals()
        self.updateEnvVal()
        
        minMargVal = 1000000
        minSite = None
        
        for i in range(self.size):
            for j in range(self.size):
                s = self.getSite((i,j))
                if s.getPicked():
                   if s.marginalVal - s.privateVal < minMargVal:
                        minSite = s
                        minSiteLoc = (i,j)
                        minMargVal = s.marginalVal - s.privateVal
        if minMargVal < 1000000:
            minSite.unchoose()
           
    
    def greedyAdd(self):

        self.updateMargVals()
        self.updateEnvVal()
        
        maxMargVal = -.01
        maxSite = None
        s = None
        
        
        for i in range(self.size):
            for j in range(self.size):
                s = self.getSite((i,j))
                if not s.getPicked():
                    if (s.marginalVal) > maxMargVal:
                        maxMargVal = s.marginalVal
                        maxSite = s
                        maxSiteLoc = (i,j)

#         print maxSite, maxSiteLoc, maxSite.getPicked()
        if -.001 < maxMargVal:
            #minSite.unchoose()
            maxSite.choose()
            return maxSiteLoc
        else: return (-1,-1)
        
            
