import tkinter as tk

class Throttle(tk.Canvas):
    def __init__(self, master = None, maxVal = 255, width = 100, height = 200):
        tk.Canvas.__init__(self, master, width=width, height=height, borderwidth=5, background='white', relief='sunken')
        self.width = width
        self.height = height
        self.maxVal = maxVal
        self.value = 0
        self.desiredValue = 0
        self.renderMeter()
        self.renderValue(200)

    def renderMeter(self):
        self.create_rectangle(35, 15, 80, 170, fill="green")
        self.create_text((57, 190), text="THROTTLE", font="Arial 14")

    def renderValue(self, desVal):
        self.desiredValue = desVal

        if self.value < self.desiredValue:
            self.delete("level")
            newVal = self.value + 1
            self.create_rectangle(35, 15, 80, abs(newVal - 170), fill="white", tag="level")
            self.value = newVal
            self.after(1, self.renderValue, self.desiredValue)
        elif self.value > self.desiredValue:
            self.delete("level")
            newVal = self.value - 1
            self.create_rectangle(35, 15, 80, abs(newVal - 170), fill="white", tag="level")
            self.value = newVal
            self.after(1, self.renderValue, self.desiredValue)
