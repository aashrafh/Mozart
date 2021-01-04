import cv2
import math

class Box(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = x + w/2, self.y+self.h/2
        self.area = w*h
    
    def overlap(self, other):
        x = max(0, min(self.x+self.w, other.x+other.w) - max(other.x, self.x))
        y = max(0, min(self.y+self.h, other.y+other.h) - max(other.y, self.y))
        area = x*y
        return area/self.area
    
    def distance(self, other):
        return math.sqrt((self.center[0]-other.center[0])**2+(self.center[1]-other.center[1])**2)
    
    def merge(self, other):
        x = min(self.x, other.x)
        y = max(self.y, other.y)
        w = max(self.x+self.w, other.x+other.w) - x
        h = max(self.y+self.h, other.y+other.h) - y
        return Box(x, y, w, h)
    
    def draw(self, img, color, thickness):
        pos = ((int)(self.x), (int)(self.y))
        size = ((int)(self.x + self.w), (int)(self.y + self.h))
        cv2.rectangle(img, pos, size, color, thickness)