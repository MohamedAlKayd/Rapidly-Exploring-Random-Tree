# Libraries
from tkinter import *
import _tkinter
from PIL import Image
from PIL import ImageTk
from PIL import ImageChops
import sys, os

# Global Variables
trace = 0
MARK="marker"  # tag value for 'mark' item

# Class 1
class checkbox(Frame):

    # Class 1 Function 1
    def __init__(self, master, label="?" ):
        Frame.__init__(self, None)
        self.pack()
        self.var = IntVar()
        c = Checkbutton(
            text=label,
            variable=self.var,
            command=self.getValue)
        c.pack(side=LEFT)

    # Class 1 Function 2
    def getValue(self, event=0):
        return self.var.get()
        
from tkinter.messagebox import askokcancel # get canned std dialog

# Class 2
class Quitter(Frame):                          # subclass our GUI
    
    # Class 2 Function 1
    def __init__(self, who, parent=None, quitLabel="Quit" ):           # constructor method
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text=quitLabel, command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
        self.who = who

    # Class 2 Function 2
    def quit(self):
        ans = askokcancel('Confirmation', "Are you sure?")
        if ans: 
            Frame.quit(self)
            self.who.canvas.quit()
            self.who.root.destroy()
            #sys.exit(0)
            return(1)

# Class 3
#class CanvasEventsDemo: 
class SelectRect: 

    # Class 3 Function 1
    def __init__(self, xmin=0,ymin=0,xmax=1000,ymax=1000, nrects=1, keepcontrol=0,
          optionboxes=0, 
          infoboxes=0, 
          quitLabel="Done",
          imfile=None, 
          parent=None,
          rescale=1.0):
        self.threadstarted=0
        W=1024
        H=768
        self.W=W
        self.H=H
        self.TICRADIUS=3
        self.TICDIAM = self.TICRADIUS*2
        datawidth  = xmax-xmin
        dataheight = ymax-ymin
        self.xscale = rescale;
        self.yscale = rescale;

        self.xmin = xmin
        self.ymin = ymin

        try:
            self.root = Tk()
            self.root.title('Env Map')
        except _tkinter.TclError:
            os.putenv("DISPLAY",":0.0")
            self.root = Tk()
            self.root.title('Env Map')

        self.width = datawidth
        self.height = dataheight
        canvas = Canvas(self.root, width=self.width, height=self.height) # , bg='beige')
        self.canvas = canvas
        # label = Label(self.root ,  image=self.img)
        self.imageid = 0
        if imfile: self.putImage(imfile)
        self.canvas.pack()


        canvas.bind('<ButtonPress-1>', self.onStart)      # click
        canvas.bind('<B1-Motion>',     self.onGrow)       # and drag
        canvas.bind('<ButtonRelease>', self.released)      # click
        #canvas.bind('<Double-1>',      self.onClear)      # delete all
        #canvas.bind('<ButtonPress-3>', self.onMove)       # move latest

        self.canvas.master.bind('<KeyPress-Left>', self.moveleft)
        self.canvas.master.bind('<KeyPress-Right>', self.moveright)
        self.canvas.master.bind('<KeyPress-Up>', self.moveup)
        self.canvas.master.bind('<KeyPress-Down>', self.movedown)
        self.canvas.master.bind('<KeyRelease-Left>', self.stoptimer)
        self.canvas.master.bind('<KeyRelease-Right>', self.stoptimer)
        self.canvas.master.bind('<KeyRelease-Up>', self.stoptimer)
        self.canvas.master.bind('<KeyRelease-Down>', self.stoptimer)
        self.alarmrate = 100
     
        
        self.drawn   = None    # last object drawn
        self.objList = [ ]     # list of existing saved objects
        self.kinds  = [canvas.create_oval, canvas.create_rectangle]
        self.rect   = [ ]      # list of coords for rectangles drawn (up to maximum of nrects)
        self.nrects = nrects   # max number of rectangles to keep (oldest deleted if too many)
        self.optionCheck = [ ] # check box items
        if optionboxes:
            for i in optionboxes:
                self.optionCheck.append(checkbox(canvas,i))
        self.canvas.pack()
        if infoboxes:
            for i in range(len(infoboxes)):
                t = self.canvas.create_text((20,20+30*i),anchor=SW,text=infoboxes[i],fill="grey")
        
        if quitLabel: Quitter(who=self,quitLabel=quitLabel)      # quit button

        if keepcontrol: 
            self.root.mainloop()

    # Class 3 Function 2
    def movemore(self):
        global vx, vy;
        self.domove(vx,vy)

    # Class 3 Function 3
    def domove(self,x,y):
        global vx, vy
        if self.alarmrate<95:
           x *= 2
           y *= 2
        vx=x
        vy=y
        if self.imageid: self.canvas.move(self.imageid,x,y)
        for i in self.objList: self.canvas.move(i,x,y)
        self.alarm = self.canvas.after(self.alarmrate, self.movemore)
        self.alarmrate = self.alarmrate-1
        if self.alarmrate<50: self.alarmrate=50

    # Class 3 Function 4
    def stoptimer(self,event):
        self.canvas.after_cancel(self.alarm)
        self.alarmrate = 100

    # Class 3 Function 5
    def startmove(self,x,y):
        self.domove(x,y)
        self.ghosttimer = self.canvas.after(100, self.ghostFlicker)

    # Class 3 Function 6
    def ghostFlicker(self):
        # flicker background image as a low-budget transparency hack
        try: self.flicker += 1
        except: self.flicker = 0
        if self.flicker%2: self.canvas.lift(self.imageGhostid)
        else: self.canvas.lower(self.imageGhostid)
        if (self.flicker>1000):
            # stop flickering until re-triggered
            self.flicker=0
            return
        self.ghosttimer = self.canvas.after(100, self.ghostFlicker)

    # Class 3 Function 7
    def moveleft(self,event): self.startmove(-1,0)

    # Class 3 Function 8
    def moveright(self,event): self.startmove(1,0)

    # Class 3 Function 9
    def moveup(self,event): self.startmove(0,-1)

    # Class 3 Function 10
    def movedown(self,event): self.startmove(0,1)

    # Class 3 Function 11
    def getRect(self):
        for i in range(len(self.rect)): 
            self.rect[i][0] = self.rect[i][0]/self.xscale
            self.rect[i][1] = self.rect[i][1]/self.yscale
            self.rect[i][2] = self.rect[i][2]/self.xscale
            self.rect[i][3] = self.rect[i][3]/self.yscale
        return self.rect
    
    # Class 3 Function 12
    def clear(self):
       self.canvas.delete(MARK)

    # Class 3 Function 13
    def getOptions(self):
        ret = [ ]
        for i in self.optionCheck:
            ret.append( i.getValue() )  
        return ret
    
    # Class 3 Function 14
    def putImage(self,p,x=0,y=0):
        """ Display from filename p or image buffer p """
        if type(p)==type("x"):
            p = Image.open(p)
        self.xscale = self.width/float(p.size[0])
        self.yscale = self.height/float(p.size[1])
        p = p.resize((self.width,self.height),resample=Image.NEAREST)

        self.imgdata = p # keep a copy to avoid garbage collection
        self.img = ImageTk.PhotoImage(p) #, width=W, height=H )
        if self.imageid: self.canvas.delete(self.imageid)
        self.imageid = self.canvas.create_image( x, y, anchor=NW, image=self.img )
        self.canvas.pack()
        self.putImageGhost(x,y)

    # Class 3 Function 15
    def putImageGhost(self,x=0,y=0):
        """ This is a background version of the image that can be used for alignment. """
        self.ghost = ImageChops.invert(self.imgdata)
        self.imgGhost = ImageTk.PhotoImage(self.ghost)
        self.imageGhostid = self.canvas.create_image( x, y, anchor=NW, image=self.imgGhost )
        self.canvas.lower(self.imageGhostid)
        self.canvas.pack()

    # Class 3 Function 16
    def putImageBuffer(self,p,x=0,y=0):
        self.xscale = self.width/float(p.size[0])
        self.yscale = self.height/float(p.size[1])
        p = p.resize((self.width,self.height),resample=Image.NEAREST)
        self.img = ImageTk.PhotoImage(p)
        self.imgdata = p # keep a copy to avoid garbage collection
        if self.imageid: self.canvas.delete(self.imageid)
        self.imageid = self.canvas.create_image( x, y, anchor=NW, image=self.img )
        self.canvas.pack()
    
    # Class 3 Function 17
    def button_click_exit_mainloop (self,event):
        event.widget.quit() # this will cause mainloop to unblock.

    # Class 3 Function 18
    def zoomin(self, event):
        self.xscale = self.xscale * 1.1;
        self.yscale = self.yscale * 1.1;
    
    # Class 3 Function 19
    def zoomout(self, event):
        self.xscale = self.xscale / 1.1;
        self.yscale = self.yscale / 1.1;
    
    # Class 3 Function 20
    def markit(self,x,y, symbol=1, r=0):

        if r>0:
            x1 = (x*self.xscale-self.xmin) - r
            y1 = (y*self.yscale-self.ymin) - r
            x2 = x1+r+r
            y2 = y1+r+r
        
        else:
            x1 = 5 + (x*self.xscale-self.xmin)- self.TICRADIUS
            y1 = 5 + (y*self.yscale-self.ymin)- self.TICRADIUS
            x2 = x1+self.TICDIAM
            y2 = y1+self.TICDIAM
        
        if symbol: self.canvas.create_oval(int(x1),int(y1),int(x2),int(y2),tag=MARK)
        
        else: self.canvas.create_rectangle(int(x1),int(y1),int(x2),int(y2),tag=MARK)

    # Class 3 Function 21
    def create_text(self, x,y, **kwargs):
        x =  (x-self.xmin)*self.xscale
        y =  (y-self.ymin)*self.yscale
        self.canvas.create_text(int(x),int(y) , fill="green", **kwargs )
        self.root.update()

    # Class 3 Function 22
    def delete(self,x=ALL):
        self.canvas.delete(x)

    # Class 3 Function 23
    # Draws a line between 2 or more
    def polyline(self,pointlist,style=0, tags=[] ):
         """ Draw a line between two of more points """
         ip = []
         for i in pointlist:
             x = (i[0]-self.xmin)*self.xscale
             y = (i[1]-self.ymin)*self.yscale
             ip = ip + [ x, y ]
         ip = list(map(int,ip))

         if style==0: self.canvas.create_line(ip,fill='red', width=1, tags=tags)
         elif style==1: self.canvas.create_line(ip, fill='green', width=2, tags=tags)
         elif style==2: self.canvas.create_line(ip,fill='blue', width=2, tags=tags)
         elif style==3: self.canvas.create_line(ip,fill='black', width=3, tags=tags)
         elif style==4: self.canvas.create_line(ip,fill='yellow', width=3, tags=tags)
    
    # Class 3 Function 24
    def released(self,filename):
        if self.drawn: 
            self.rect.append( self.canvas.coords(self.drawn)[:] )
            self.objList.append( self.drawn )
            if len(self.rect) > self.nrects:
                self.rect = self.rect[1:] 
                self.canvas.delete( self.objList[0] )
                self.objList = self.objList[1:]
                
            self.canvas.itemconfig(self.drawn, tag='bounds', fill="", outline='blue')
            
    # Class 3 Function 25
    def onStart(self, event):
        self.shape = self.kinds[1]
        self.start = event
        self.drawn = None
    
    # Class 3 Function 26
    def onGrow(self, event):                            
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
        self.canvas.itemconfig(objectId, tag='bounds', fill='blue')
        self.drawn = objectId
    
    # Class 3 Function 27
    def showRect(self,rect,fill='green',outline='red'):
        self.shape = self.kinds[1]
        objectId = self.shape(rect[0]*self.xscale, rect[1]*self.yscale, 
                              rect[2]*self.xscale, rect[3]*self.yscale)
        self.canvas.itemconfig(objectId, tag='bounds', outline='black', fill=fill)
    
    # Class 3 Function 28
    def onClear(self, event):
        event.widget.delete('all')                        
    
    # Class 3 Function 29
    def updateLoop(self):
        print ("Enter infinite loop updateLoop(). Use a/z")
        while 1:
            self.canvas.master.bind('<KeyPress-a>', self.zoomin)
            self.canvas.master.bind('<KeyPress-z>', self.zoomout)
            self.root.update()
    
    # Class 3 Function 30
    def events(self):
        self.root.update()
    
    # Class 3 Function 31
    def onMove(self, event):
        if self.drawn:                               
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event

    # Class 3 Function 32    
    def mainloop(self):
        self.root.mainloop()

# Main
if __name__ == '__main__':
    import time
    cv = SelectRect(nrects=2,infoboxes=["Hello world"],keepcontrol=1)
    print (cv.getRect())