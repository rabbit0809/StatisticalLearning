import numpy
import tkinter
import math
import tkinter as tk
from tkinter import ttk as ttk
from collections import namedtuple
import sys

Point = namedtuple("Point", "x y")

class CanvasView(tk.Frame):
    Colours = ['red', 'blue', 'green', 'yellow', 'orange']
    def __init__(self, master, vectors, coords):
        super().__init__(master)
        self.canvas = tk.Canvas(self, width=1024, height=1024)
        for vector in vectors:
            self.canvas.create_oval(vector[1][0]-2, vector[1][1]-2, vector[1][0] + 2, vector[1][1] + 2, fill=self.Colours[vector[0]], outline=self.Colours[vector[0]])        
        self.canvas.create_line(coords[0][0], coords[0][1], coords[1][0], coords[1][1], fill="black", width=2)
        self.canvas.pack()
        self.pack()

class parser:
    def __init__(self, handle):
        self.numvars = None
        self.feat_vecs = []
        classes = set()
        for line in handle.readlines():
            y, x = line.split(':')
            x = x.split()
            line_numvars = len(x)
            y = int(y)
            classes.add(y)
            if self.numvars is None:
                self.numvars = line_numvars
            elif self.numvars != line_numvars:
                raise Exception("Inconsistent number of variables in", handle)
            x = [ float(i) for i in x ]
            x.append(500)
            x = numpy.array(x)
            self.feat_vecs.append((y, x))
        self.numclasses = len(classes)
        self.weights = numpy.zeros(self.numvars+1)
        for i in range(0, self.numvars+1):
            self.weights[i] = numpy.random.uniform(-1, 1)

    def draw(self):
        xIntercept = 500 * (-self.weights[2] / self.weights[0])
        yIntercept = 500 * (-self.weights[2] / self.weights[1])
        coords = []
        coords.append((0, yIntercept))
        coords.append((xIntercept, 0))
        print(coords)
        canvas = CanvasView(master=tk.Tk(), vectors=self.feat_vecs, coords=coords)
        canvas.mainloop()

    
    @staticmethod
    def sigmoid(w, x):
        MAX = 200
        MIN = -200
        dot = numpy.dot(w, x)
        clamp = max(MIN, min(MAX, dot))
        return 1 / (1 + math.exp(-clamp))

    def train(self, num_epochs, eta):
        for epoch in range(0, num_epochs):
            dLdm = numpy.zeros(self.numvars + 1)
            err = 0
            for y, x in self.feat_vecs:
                dLdm += ((y - parser.sigmoid(self.weights, x)) * x)/len(self.feat_vecs)
            norm = numpy.sqrt(numpy.dot(dLdm, dLdm))
            if norm == 0:
                print("Converged at epoch", epoch)
                break
            uvect = dLdm / norm
            self.weights += eta * uvect
            #wnorm = numpy.sqrt(numpy.dot(self.weights, self.weights))
            #print("Epoch", epoch, self.weights, "W UV", self.weights/wnorm)
        print("Final weights", self.weights)
        #for y, x in self.feat_vecs:
        #    print(y, parser.sigmoid(self.weights, x))

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], " <file>")
    sys.exit(1)
abs_name = sys.argv[1]
my_parser = parser(open(abs_name, "r"))
my_parser.train(1000, 0.1)
my_parser.draw()
