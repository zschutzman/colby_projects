#site.py

'''
Created on Sep 17, 2015

@author: zachary
'''

import randomSeeded
import copy


def cloneSite(s):
    newSite = Site(s.loc,s.index)
    newSite.values = s.values[:]
    newSite.curVal = newSite.values[0]
    newSite.privateVal = copy.deepcopy(s.privateVal)
    newSite.nbrs = []
    
    return newSite

class Site:
    '''
    classdocs
    '''

    def __init__(self, loc, idx):
        '''
        Constructor
        '''
        
        
        self.loc = loc
        self.index = idx
        self.pastBids = []
        self.pastSales = []
        self.sold = False
        self.lastBid = None
        self.curVal = None
        self.picked = False
        
        self.varVal = 0
        self.selVar = None
        self.varCost = 0
        
        self.values = []
        
        for v in range(5):
            self.values.append(randomSeeded.random.randint(1,13))
        
        self.values.sort() 
        self.curVal = self.values[0]
        for i in range(4):
            self.values[i+1] = self.curVal
        
        self.privateVal = randomSeeded.random.randint(2,12)
        self.marginalVal = 0
        
        
        
        
    def addNeighbors(self, nbrs):
        
        self.nbrs = []
        
        for n in nbrs:
            self.nbrs.append(n)
            
    def getPicked(self):
        return self.picked
            
    def updateValue(self):
        self.curVal = self.values[sum(s.getPicked() for s in self.nbrs)]
        
    def getCurVal(self):
        self.updateValue()
        return self.curVal
    def getCurValLS(self):
        self.updateValue()
        return self.curVal * self.getPicked()  
    def getValues(self):
        return self.values
    def getBids(self):
        return self.pastBids
    def getSales(self):
        return self.pastSales
    def getSuccessfulBids(self):
        return [a*b for a,b in zip(self.pastBids,self.pastSales)]
    def getPrivateValue(self):
        return self.privateVal
    def getPrivateValueLS(self):
        return self.privateVal * self.getPicked()
    def getLocation(self):
        return self.loc
    def getNeighbors(self):
        return self.nbrs
    def choose(self):
        self.picked = True
    def unchoose(self):
        self.picked = False
    def setVar(self, v):
        self.selVar = v
        self.varVal = v * self.getCurVal()
        self.varCost = v * self.privateVal
    
    def getNumPickedNeighbors(self):
        return sum([n.getPicked() for n in self.nbrs])
        
        
      
             