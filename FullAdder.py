import pygame
from pygame import Rect
from Component import Component
from Connection import Connection
from ExternalPatch import ExternalPatch
from Junction import Junction
from AndGate import AndGate
from OrGate import OrGate
from XorGate import XorGate
from Gate import PADDING

class FullAdder(Component):
    def __init__(self, parent=None, position=(0, 0)):
        super(FullAdder, self).__init__(parent=parent,
                name="Full Adder", 
                rect=Rect(position[0], position[1], 67, 86))
        # self.display_frame = True
        self.child_components.append(XorGate(parent=self, position=(12, 0)))
        self.child_components.append(XorGate(parent=self, position=(37, 16)))
        self.child_components.append(AndGate(parent=self, position=(12, 32)))
        self.child_components.append(AndGate(parent=self, position=(12, 54)))
        self.child_components.append(OrGate(parent=self, position=(37, 43)))
       
        self.external_patches["A"] = ExternalPatch( \
                parent=self,
                direction=True,
                position=(0, 11))
        
        self.external_patches["B"] = ExternalPatch( \
                parent=self,
                direction=True,
                position=(0, 19))
        
        self.external_patches["Cin"] = ExternalPatch( \
                parent=self,
                direction=True,
                position=(0, 35))
       
        self.external_patches["S"] = ExternalPatch( \
                parent=self,
                direction=False,
                position=(self.get_width(), 31))
        
        self.external_patches["Cout"] = ExternalPatch( \
                parent=self,
                direction=False,
                position=(self.get_width(), 58))
        
        # A in junction
        point_a = (self.child_components[0].external_patches["A"].get_relative_position_to_parent()[0]/2 - 2, 11)
        j = Junction(parent=self, position=point_a).one_two_junction()
        self.child_components.append(j)
        
        patch_a = j.external_patches["A"]
        patch_b = self.external_patches["A"]
        self.auto_connect("in_a", patch_a, patch_b, internal_b=False)
 
        patch_a = j.external_patches["S1"]
        patch_b = self.child_components[0].external_patches["A"]
        self.auto_connect("in_a_xor", patch_a, patch_b)
        
        patch_a = self.child_components[3].external_patches["A"]
        patch_b = j.external_patches["S2"]
        self.auto_connect("in_a_and", patch_a, patch_b, offcet=-6)        

        # B in junction
        point_a = (self.child_components[0].external_patches["B"].get_relative_position_to_parent()[0]/2 - 6, 19)
        j = Junction(parent=self, position=point_a).one_two_junction()
        self.child_components.append(j)
        
        patch_a = j.external_patches["A"]
        patch_b = self.external_patches["B"]
        self.auto_connect("in_b", patch_a, patch_b, internal_b=False)
 
        patch_a = j.external_patches["S1"]
        patch_b = self.child_components[0].external_patches["B"]
        self.auto_connect("in_b_xor", patch_a, patch_b)
        
        patch_a = self.child_components[3].external_patches["B"]
        patch_b = j.external_patches["S2"]
        self.auto_connect("in_b_and", patch_a, patch_b, offcet=-8)
      
        # Cin junction
        point_a = (self.child_components[1].external_patches["B"].get_relative_position_to_parent()[0]/2 - 8, 35)
        j = Junction(parent=self, position=point_a).one_two_junction()
        self.child_components.append(j)
        
        patch_a = j.external_patches["A"]
        patch_b = self.external_patches["Cin"]
        self.auto_connect("cin", patch_a, patch_b, internal_b=False)
 
        patch_a = j.external_patches["S1"]
        patch_b = self.child_components[1].external_patches["B"]
        self.auto_connect("cin_xor_b", patch_a, patch_b)
        
        patch_a = self.child_components[2].external_patches["B"]
        patch_b = j.external_patches["S2"]
        self.auto_connect("cin_or_b", patch_a, patch_b, offcet=-3)
        
        # Xor to Xor and And       
        point_a = self.child_components[1].external_patches["A"].get_relative_position_to_parent()
        point_b = self.child_components[0].external_patches["S"].get_relative_position_to_parent()
        point_a = ((point_b[0] - point_a[0])/2 + point_a[0],  
                point_a[1])
        j = Junction(parent=self, position=point_a).one_two_junction()
        self.child_components.append(j)

        patch_a = j.external_patches["A"]
        patch_b = self.child_components[0].external_patches["S"]
        self.auto_connect("xor_s", patch_a, patch_b, offcet=1)
 
        patch_a = j.external_patches["S1"]
        patch_b = self.child_components[1].external_patches["A"]
        self.auto_connect("xor_xor_a", patch_a, patch_b)
        
        patch_a = self.child_components[2].external_patches["A"]
        patch_b = j.external_patches["S2"]
        self.auto_connect("xor_and_a", patch_a, patch_b, offcet=-13)
        
        # And to Or 
        patch_a = self.child_components[3].external_patches["S"]
        patch_b = self.child_components[4].external_patches["B"]
        self.auto_connect("and_or_b", patch_a, patch_b)

        patch_a = self.child_components[2].external_patches["S"]
        patch_b = self.child_components[4].external_patches["A"]
        self.auto_connect("and_or_a", patch_a, patch_b) 
        
        # S out
        patch_a = self.child_components[1].external_patches["S"]
        patch_b = self.external_patches["S"]
        self.auto_connect("s_out", patch_a, patch_b, internal_b=False)
        
        # Cout
        patch_a = self.child_components[4].external_patches["S"]
        patch_b = self.external_patches["Cout"]
        self.auto_connect("c_out", patch_a, patch_b, internal_b=False)

