import pygame
from pygame import Rect
from Component import Component
from Connection import Connection
from EightBitAdder import EightBitAdder
from TristateGate import TristateGate
from FullAdder import FullAdder
from AndGate import AndGate

class ParentComponent(Component):
    def __init__(self):
        super(ParentComponent, self).__init__(name="Custom Core", 
                rect=Rect(100, 100, 1346,738))
        self.display_frame = True

        component = EightBitAdder(parent=self, position=(50, 50))
        self.child_components.append(component)
        

        for instance in ["add_out", "sub", "cout"]:
            position = component.external_patches[instance.upper()].get_relative_position_to_parent()
            connection = Connection(parent=self)
            self.connections[instance] = connection
            component.external_patches[instance.upper()].external_connection = connection
            connection.lines.append((position, (position[0] + 30, position[1])))
      
        a = []
        b = []
        for i in range(0, 8):
            position = component.external_patches[f"A{i}"].get_relative_position_to_parent()
            connection = Connection(parent=self)
            a.append(connection)
            self.connections[f"a{i}"] = connection
            component.external_patches[f"A{i}"].external_connection = connection
            connection.lines.append((position, (position[0], position[1] - 30)))
            
            position = component.external_patches[f"B{i}"].get_relative_position_to_parent()
            connection = Connection(parent=self)
            b.append(connection)
            self.connections[f"b{i}"] = connection
            component.external_patches[f"B{i}"].external_connection = connection
            connection.lines.append((position, (position[0], position[1] + 30)))
            
        a[0].state = True
        b[0].state = True
        
        self.connections["add_out"].state = True 
        self.connections["sub"].state = True 


