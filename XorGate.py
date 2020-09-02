import pygame
from pygame import Rect
from Gate import Gate

class XorGate(Gate):

    def __init__(self, position, parent=None): 
        super(XorGate, self).__init__(parent=parent,
                name="Xor", 
                position=position,
                imagepath="img/xor.png") 

   
    def compute(self):
        self.connections["S"].state = self.connections["A"].state ^ \
            self.connections["B"].state
