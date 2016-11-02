from datetime import datetime, timedelta
from scipy import optimize
import numpy as np

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def y(self, x):
        return self.m * x + self.a

    def distance(self, x0, y0):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2

        px = x2-x1
        py = y2-y1

        something = px*px + py*py
        u =  ((x0 - x1) * px + (y0 - y1) * py) / float(something)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = x1 + u * px
        y = y1 + u * py

        dx = x - x0
        dy = y - y0
        dist = (dx*dx + dy*dy)**.5
        return dist
        
def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])
    
def fitLines(xList, yList):
    p, e = optimize.curve_fit(piecewise_linear, xList, yList)
    return p