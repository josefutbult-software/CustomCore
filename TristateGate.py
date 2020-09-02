import pygame
from pygame import Rect
from math import pi
from Component import Component, BLACK
from Connection import Connection
from ExternalPatch import ExternalPatch

PADDING = 3
IMAGEPATH = "img/buffer.png"

class TristateGate(Component):

    def __init__(self, parent, position): 
        super(TristateGate, self).__init__(parent=parent,
                name="Tristate", 
                rect=Rect(position[0], position[1], 20+PADDING*2, 20+PADDING*2))
        self.image = pygame.image.load(IMAGEPATH)

        self.connections["A"] = Connection(parent=self)
        self.connections["EN"] = Connection(parent=self)
        self.connections["S"] = Connection(parent=self)

        self.external_patches["A"] = ExternalPatch( \
                parent=self,
                connection=self.connections["A"],
                direction=True,
                position=(PADDING, 9+PADDING))

        self.external_patches["EN"] = ExternalPatch( \
                parent=self,
                connection=self.connections["EN"],
                direction=True,
                position=(self.get_width()/2, PADDING + 5))

        self.external_patches["S"] = ExternalPatch( \
                parent=self,
                connection=self.connections["S"],
                direction=False,
                position=(self.get_width()-PADDING, 9+PADDING))

    def render(self, screen, screen_position):
        screen.blit(self.image, 
                (self.get_position()[0] + PADDING + screen_position[0], 
                    self.get_position()[1] + PADDING + screen_position[1]))
    
    def compute(self):
        if self.connections["EN"].state:
            self.connections["S"].state = self.connections["A"].state



