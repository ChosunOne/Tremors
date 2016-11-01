from datetime import datetime, timedelta

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
        num = (y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1
        denom = ((y2 - y1)**2 + (x2 - x1)**2)**.5
        return num / denom
        
        
    