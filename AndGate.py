import pygame
from pygame import Rect
from Gate import Gate

class AndGate(Gate):

    def __init__(self, parent, position=(0, 0)): 
        super(AndGate, self).__init__(parent=parent,
                name="And", 
                position=position,
                imagepath="img/and.png")

    def compute(self):
        self.connections["S"].state = self.connections["A"].state & \
            self.connections["B"].state
