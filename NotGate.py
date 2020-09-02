import pygame
from pygame import Rect
from math import pi
from Component import Component, BLACK
from Connection import Connection
from ExternalPatch import ExternalPatch

PADDING = 3
IMAGEPATH = "img/not.png"

class NotGate(Component):

    def __init__(self, parent, position): 
        super(NotGate, self).__init__(parent=parent,
                name="Not", 
                rect=Rect(position[0], position[1], 20+PADDING*2, 20+PADDING*2))
        self.image = pygame.image.load(IMAGEPATH)

        self.connections["A"] = Connection(parent=self)
        self.connections["S"] = Connection(parent=self)

        self.external_patches["A"] = ExternalPatch( \
                parent=self,
                connection=self.connections["A"],
                direction=True,
                position=(PADDING, 9+PADDING))

        self.external_patches["S"] = ExternalPatch( \
                parent=self,
                connection=self.connections["S"],
                direction=False,
                position=(self.rect.width-PADDING, 9+PADDING))

    def render(self, screen, screen_position):
        screen.blit(self.image, 
                (self.rect.left + PADDING + screen_position[0], 
                    self.rect.top + PADDING + screen_position[1]))
    
    def compute(self):
        self.connections["S"].state = not self.connections["A"].state



