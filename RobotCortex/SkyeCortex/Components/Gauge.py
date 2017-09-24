import tkinter as tk
from PIL import ImageTk, Image
import math

class Gauge(tk.Canvas):
    def __init__(self, master, title, imgFile, maxVal = 100, width = 200, height = 200, radius = 75):
        tk.Canvas.__init__(self, master, width=width, height=height, borderwidth=0, highlightthickness=0)
        self.width = width
        self.height = height
        self.title = title
        self.file = imgFile
        self.maxVal = maxVal
        self.bFactor = 230
        self.mFactor = -275/maxVal
        self.value = 0
        self.radius = radius
        self.desiredValue = 0
        self.centerX = int(self.width/2)
        self.centerY = int(self.height/2) - 5
        self.renderImage()
        self.renderNeedle(40)

    def getX(self, deg):
        return self.centerX + self.radius * math.cos(math.radians(deg))
        
    def getY(self, deg):
        return self.centerY - self.radius * math.sin(math.radians(deg))

    def renderImage(self):
        self.image = Image.open(self.file)
        self.tkimage = ImageTk.PhotoImage(self.image.resize((self.width, self.height), Image.ANTIALIAS))
        self.canvas_obj = self.create_image(self.centerX, self.centerY + 5, image=self.tkimage)
#       self.create_text(150, 180, text="mph", fill="white", font="Arial 14")
        self.create_text(self.centerX, self.centerY + 60, text=self.title, fill="black", font="Arial 12")
#       self.create_text(195, 200, text="100", fill="white", font="Arial 14")
#       self.create_text(100, 200, text="0", fill="white", font="Arial 14")
#       self.create_text(75, 135, text="20", fill="white", font="Arial 14")
#       self.create_text(225, 135, text="80", fill="white", font="Arial 14")
#       self.create_text(180, 80, text="60", fill="white", font="Arial 14")
#       self.create_text(120, 80, text="40", fill="white", font="Arial 14")

    def renderNeedle(self, desVal):
        self.desiredValue = desVal

        if self.value < self.desiredValue:
            self.delete("needle")
            newVal = self.value + 1
            degree = self.mFactor * newVal + self.bFactor
            line = self.create_line(self.centerX, self.centerY, self.getX(degree), self.getY(degree), fill="#ff4800", width=3, tag="needle")
            self.value = newVal
            self.after(1, self.renderNeedle, self.desiredValue)
        elif self.value > self.desiredValue:
            self.delete("needle")
            newVal = self.value - 1
            degree = self.mFactor * newVal + self.bFactor
            line = self.create_line(self.centerX, self.centerY, self.getX(degree), self.getY(degree), fill="#ff4800", width=3, tag="needle")
            self.value = newVal
            self.after(1, self.renderNeedle, self.desiredValue)
