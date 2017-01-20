import sys
import landscape
import time
import Tkinter as tk
import genalg
#import model


class AuctionVis(tk.Frame):
    def __init__(self, master=None, ls = None):
        
        tk.Frame.__init__(self,master)
        
        self.pack()
        self.createCanvas()
        
        if ls != None:
            self.addLandscape(ls)
            
        #self.addModel(self.ls,1200)
        
        self.addButtons()
        self.updateText()

        self.c.bind("<Button-1>",self.click)
        
        
    
    def createCanvas(self):
        
        
        self.c = tk.Canvas(self.master, width = 600,height=600)
        self.c.pack()
        
        
    def addButtons(self):
        self.QUIT = tk.Button(self)
        self.QUIT['text'] = "QUIT"
        self.QUIT['fg'] = "black"
        self.QUIT['command'] = self.quit
        
        self.QUIT.pack({"side":"left"})
        
        self.VAL = tk.Button(self)
        self.VAL['text']="Print Env. Val"
        self.VAL['fg'] = "dark green"
        self.VAL['command'] = self.ls.printEnvVal
        
        self.VAL.pack({"side":"left"})
    
        self.UT = tk.Button(self)
        self.UT['text']="Update Text"
        self.UT['fg'] = "dark blue"
        self.UT['command'] = self.updateText
        
        self.UT.pack({"side":"left"})
        
        self.GT = tk.Button(self)
        self.GT['text']="Greedy Test"
        self.GT['fg'] = "dark red"
        self.GT['command'] = self.greedySelection
        
        self.GT.pack({"side":"left"})  
        
        self.ST = tk.Button(self)
        self.ST['text']="To String"
        self.ST['command']=self.mapString
        
        self.ST.pack({"side":"left"})   
        

    def mapString(self):
        l = []
        for i in range(self.ls.size):
            m = []
            for j in range(self.ls.size):   
                if self.ls.getSite((i,j)).getPicked():
                    m.append(1)
                else:
                    m.append(0)
            l.append(m)
        print l
    def addLandscape(self, scape):
        self.ls = scape
        
        x = 50
        y = 50
        
        self.textList = []
        self.boxList = []
        
        for i in range(self.ls.size):
            l = []
            b = []
            for j in range(self.ls.size):
                b.append(self.c.create_rectangle(x,y,x+35,y+35,activefill='orange', fill = 'brown'))
                l.append(self.c.create_text(x+17,y,text = "0\n0", font="Times 7", anchor="n"))
                x = x + 36
            self.textList.append(l)
            self.boxList.append(b)
            x = 50
            y = y + 36
        self.c.pack()

        
    def click(self, event):
        a = self.c.find_withtag('current')
        if self.c.type(a) == "rectangle":
            x = (int(self.c.coords(a)[0])-50)/36
            y = (int(self.c.coords(a)[1])-50)/36

            s = self.ls.getSite((y,x))
            if s.getPicked():
                s.unchoose()
                self.c.itemconfig('current',fill = 'brown')
            else:
                s.choose()
                self.c.itemconfig('current',fill='green')
             
        self.updateText()  
        
    def updateText(self):
        for i in range(self.ls.size):
            for j in range(self.ls.size):
                s = self.ls.getSite((i,j))
                st = s.getPicked()
                s.choose()
                m = self.ls.getEnvVal()
                s.unchoose()
                m = m - self.ls.getEnvVal()
                
                s.marginalVal = m
                
                if st:
                    s.choose()
                else:
                    s.unchoose()
                
                self.c.itemconfig(self.textList[i][j], text="e="+str(s.getCurVal()) + "\n"+"p="+str(s.privateVal)+"\n"+"m="+str(m))
    
    def greedySelection(self):
        
      
        maxMargVal = -.01
        maxSiteIdx = None
        maxSite = None
        s = None
        
        for i in range(self.ls.size):
            for j in range(self.ls.size):
                s = self.ls.getSite((i,j))
                if (s.marginalVal - s.privateVal > maxMargVal) and (s.getPicked() == False):
                    maxSite = s
                    maxSiteIdx = (i,j)
                    maxMargVal = s.marginalVal-s.privateVal
        if s == None: return
        maxSite.choose()
        print maxSiteIdx
        self.c.itemconfig(self.boxList[maxSiteIdx[0]][maxSiteIdx[1]],fill="green")
        self.updateText()
   
            
           
    
root = tk.Tk()
l = landscape.Landscape(15)
app = AuctionVis(master = root,ls = l)
app.updateText()
app.mainloop()
root.destroy()