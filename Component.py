import pygame
from pygame import Rect
from Connection import Connection
from ExternalPatch import ExternalPatch

DEFAULT_PADDING = 3
BLACK = (0, 0, 0)

class Component:
    def __init__(self, 
            name, 
            parent=None, 
            rect=Rect(0, 0, 0, 0), 
            padding=DEFAULT_PADDING):
        
        self.parent = parent
        self.name = name
        self.display_frame = False
        self.display_name = False
        self.padding = padding
    
        self._rect = rect

        self.child_components = []
        self.connections = {}
        self.external_patches = {}


    def get_relative_position(self):
        return (self._rect.left, self._rect.top)


    def get_relative_position_to_parent(self):
        component_position = self.parent.get_relative_position()
        return (self._rect.left + component_position[0] + self.parent.padding, 
                self._rect.top + component_position[1] + self.parent.padding)


    def get_position(self): 
        if self.parent is not None:
            parent_position = self.parent.get_position()
            return (self._rect.left + parent_position[0] + self.padding,
                    self._rect.top + parent_position[1] + self.padding)
        else:
            return (self._rect.left, self._rect.top)
    

    def get_width(self):
        return self._rect.width


    def get_height(self):
        return self._rect.height


    def render(self, screen, screen_position):
        pass


    def _render(self, screen, screen_position):
        for instance in self.child_components:
            instance._render(screen, screen_position)

        for key, instance in self.connections.items():
            instance.render(screen, screen_position)

        self.render(screen, screen_position)

        if self.display_frame:
            position = self.get_position()
            pygame.draw.rect(screen, BLACK, Rect(position[0] + screen_position[0], 
                position[1] + screen_position[1], self.get_width(), self.get_height()), 
                self.padding)
 

    def compute(self):
        pass


    def _compute(self):
        for key, instance in self.external_patches.items():
            try:
                instance.input_connection()
            except Exception as e:
                print(f'Error in computing external connection {key} ' + 
                        f'in component {type(self).__name__}')
                raise e

        for instance in self.child_components:
            instance._compute()
        
        try:
            self.compute()
        except Exception as e:
            print(f'Error in computing {type(self).__name__}')
            raise e

        for key, instance in self.external_patches.items():
            try:
                instance.output_connection()
            except Exception as e:
                print(f'Error in computing external connection {key} ' + 
                        f'in component {type(self).__name__}')
                raise e            


    def clear(self):
        for key, instance in self.connections.items():
            instance.rendered = False

        for instance in self.child_components:
            instance.clear()

    
    def connect(self, name, patch_a, patch_b, 
            internal_a=True, internal_b=True, lines=None): 
        connection = Connection(parent=self)
        self.connections[name] = connection
        if internal_a:
            patch_a.external_connection = connection
        else:
            patch_a.internal_connection = connection
        
        if internal_b:
            patch_b.external_connection = connection
        else:
            patch_b.internal_connection = connection 
        
        if lines is not None:
            for i in range(0, len(lines) - 1):
                connection.lines.append((lines[i], lines[i + 1]))
        else:
            return connection


    def auto_connect(self, name, patch_a, patch_b, 
            internal_a=True, internal_b=True, offcet=0): 
        connection = self.connect(name, patch_a, patch_b, internal_a, internal_b)
        
        if internal_a:
            point_a = patch_a.get_relative_position_to_parent()
        else:
            point_a = patch_a.get_relative_position()
        
        if internal_b:
            point_b = patch_b.get_relative_position_to_parent()
        else:
            point_b = patch_b.get_relative_position()

        connection.auto_line(point_a, point_b, offcet)

