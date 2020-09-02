import pygame
from pygame import Rect
from Gate import Gate

class OrGate(Gate):

    def __init__(self, position, parent=None): 
        super(OrGate, self).__init__(parent=parent,
                name="Or", 
                position=position,
                imagepath="img/or.png") 

   
    def compute(self):
        self.connections["S"].state = self.connections["A"].state | \
            self.connections["B"].state
