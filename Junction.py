import pygame
from pygame import Rect
from Component import Component
from Connection import Connection
from ExternalPatch import ExternalPatch

from Connection import BLACK, RED

class Junction(Component):
    def __init__(self, parent, position=(0, 0)):
        super(Junction, self).__init__(parent=parent,
                name="Junction", 
                rect=Rect(position[0], position[1], 0, 0),
                padding=0)
        self.state = False

    def compute(self):
        for key, patch in self.external_patches.items():
            if patch.direction and patch.external_connection is not None and \
                    patch.external_connection.state:
                self.state = True
                for key, patch in self.external_patches.items():
                    if patch.external_connection is not None:
                        patch.external_connection.state = True
                return

        self.state = False
        for key, patch in self.external_patches.items():
            if patch.external_connection is not None:
                patch.external_connection.state = False
    
    def render(self, screen, screen_position):
        position = self.get_position()
        pygame.draw.circle(screen, RED if self.state else BLACK, 
                (position[0] + 1 + screen_position[0], 
                    position[1] + 1 + screen_position[1]), 3)
    

    def append(self, name, direction, connection=None):
        self.external_patches[name] = ExternalPatch(parent=self,
                direction=direction)
        self.external_patches[name].external_connection = connection


    def one_two_junction(self):       
        self.append(name="A", direction=True)
        self.append(name="S1", direction=False)
        self.append(name="S2", direction=False)
        return self
   
   
    def two_one_junction(self): 
        self.append(name="A", direction=True)
        self.append(name="B", direction=True)
        self.append(name="S", direction=False)
        return self
