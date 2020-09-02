import pygame
from pygame import Rect
from math import pi
from Component import Component, BLACK
from Connection import Connection
from ExternalPatch import ExternalPatch

PADDING = 3

class Gate(Component):

    def __init__(self, parent, name, position, imagepath): 
        super(Gate, self).__init__(parent=parent,
                name=name, 
                rect=Rect(position[0], position[1], 20+PADDING*2, 20+PADDING*2))
        self.image = pygame.image.load(imagepath)
        
        self.connections["A"] = Connection(parent=self)
        self.connections["B"] = Connection(parent=self)
        self.connections["S"] = Connection(parent=self)

        self.external_patches["A"] = ExternalPatch( \
                parent=self,
                connection=self.connections["A"],
                direction=True,
                position=(PADDING, 8))

        self.external_patches["B"] = ExternalPatch( \
                parent=self,
                connection=self.connections["B"],
                direction=True,
                position=(PADDING, 16))

        self.external_patches["S"] = ExternalPatch( \
                parent=self,
                connection=self.connections["S"],
                direction=False,
                position=(28-PADDING*2, 12))


    def render(self, screen, screen_position):
        screen.blit(self.image, 
                (self.get_position()[0] + PADDING + screen_position[0], 
                    self.get_position()[1] + PADDING + screen_position[1]))
