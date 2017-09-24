import tkinter as tk

class AttitudeIndicator(tk.Canvas):
    def __init__(self, master = None, width=285, height=265):
        tk.Canvas.__init__(self, master, width=width, height=height, background='light gray', borderwidth=0, highlightthickness=0)
        self.width = width
        self.height = height
        self.positionX = 0
        self.positionY = 0
        self.desiredValueX = 0
        self.desiredValueY = 0
        self.renderGrid()
        self.renderBubble(10, 10)

    def renderGrid(self):
        self.create_rectangle(0,0, 280, 260, fill="black") #dark blue #5D7AB5 #2E509E
        self.create_line(0, 130, 280, 130, fill="white", width=2)
        self.create_line(140, 0, 140, 260, fill="white", width=2)
        self.create_oval(105, 95, 175, 165, outline="white", width=2) #100, 90, 180, 170
        self.create_oval(90, 80, 190, 180, outline="white", width=2) #100, 90, 180, 170

    def drawCircle(self, desX, desY):
        self.create_oval(110 + desX, 100 - desY, 170 + desX, 160 - desY, fill="dark red", tag="bubble") #cyan

    def renderBubble(self, desValX, desValY):
        self.desiredValueX = desValX
        self.desiredValueY = desValY
        self.delete("bubble")
        self.drawCircle(desValX, desValY)
        
