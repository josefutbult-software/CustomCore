import pygame
from pygame import Rect
from Component import Component
from Connection import Connection
from ExternalPatch import ExternalPatch
from Junction import Junction
from FullAdder import FullAdder
from TristateGate import TristateGate
from XorGate import XorGate

class EightBitAdder(Component):
    def __init__(self, parent=None, position=(0, 0)):
        super(EightBitAdder, self).__init__(parent=parent,
                name="Eight Bit Adder", 
                rect=Rect(position[0], position[1], 630, 221))
        self.display_frame = True
        
        # External patches
        add_out = ExternalPatch( \
                    parent=self,
                    direction=True,
                    position=(self.get_width(), 104))
        self.external_patches["ADD_OUT"] = add_out

        sub = ExternalPatch( \
                    parent=self,
                    direction=True,
                    position=(self.get_width(), 168))
        self.external_patches["SUB"] = sub

        cout = ExternalPatch( \
                    parent=self,
                    direction=False)
        self.external_patches["COUT"] = cout

        tristates = []
        junctions = []
        fullAdders = []

        for i in range(0, 8):
            # Full adder configuration
            component = FullAdder(parent=self, position=(77 * i + 10, 15))
            self.child_components.append(component)
            fullAdders.append(component)

            patch_a = ExternalPatch( \
                    parent=self,
                    direction=True,
                    position=(self.get_width()/2 - 40 + 5 * i, 0))
            self.external_patches[f"A{i}"] = patch_a
            patch_b = self.child_components[i].external_patches["A"]
            point_y = patch_a.get_relative_position()[1] + 5 * (i if i < 4 else 7 - i) + 5
            lines = [patch_a.get_relative_position(), 
                (patch_a.get_relative_position()[0], point_y),
                (patch_b.get_relative_position_to_parent()[0] - 5, point_y), 
                (patch_b.get_relative_position_to_parent()[0] - 5, 
                    patch_b.get_relative_position_to_parent()[1]),
                patch_b.get_relative_position_to_parent()] 
            
            self.connect(f"a_{i}", patch_a, patch_b, 
                    internal_a=False, lines=lines)
        
        # Carry connection between full adders
        for i in range(1, 8):
            patch_a = self.child_components[i-1].external_patches["Cout"]
            patch_b = self.child_components[i].external_patches["Cin"]
            self.auto_connect(f"C{i-1}-{i}", patch_a, patch_b, offcet=3)

        # Tristate buffer
        for i in range(0, 8):
            tristate = TristateGate(parent=self, position=(77 * i + 26, 100))
            self.child_components.append(tristate) 
            tristates.append(tristate)

            component = self.child_components[i]
            patch_a = component.external_patches["S"]
            patch_b = tristate.external_patches["A"]
            lines = [patch_a.get_relative_position_to_parent(), 
                (patch_a.get_relative_position_to_parent()[0], 
                    patch_a.get_relative_position_to_parent()[1] + 50),
                (patch_b.get_relative_position_to_parent()[0] - 5, 
                    patch_a.get_relative_position_to_parent()[1] + 50), 
                (patch_b.get_relative_position_to_parent()[0] - 5, 
                    patch_b.get_relative_position_to_parent()[1]),
                patch_b.get_relative_position_to_parent()]
            
            self.connect(f"S{i}_tri_a{i}", patch_a, patch_b, lines=lines)
            
            # External connection A configuration
            patch_a = ExternalPatch( \
                    parent=self,
                    direction=False,
                    position=(0, 128 + 5 * i))
            self.external_patches[f"S{i}"] = patch_a
            patch_b = tristate.external_patches["S"]
            lines = [patch_b.get_relative_position_to_parent(), 
                    (patch_b.get_relative_position_to_parent()[0] + 5, 
                        patch_b.get_relative_position_to_parent()[1]),
                    (patch_b.get_relative_position_to_parent()[0] + 5, 
                        patch_a.get_relative_position()[1]), 
                    patch_a.get_relative_position()]

            self.connect(f"tri{i}_s", patch_a, patch_b, lines=lines)
            
        # Junctions for external add_out connection and tristate buffers
        for i in range(1, 8):
            j = Junction(parent=self, position=(( \
                    tristates[i].external_patches["EN"].get_relative_position_to_parent()[0], 
                add_out.get_relative_position()[1]))).one_two_junction()
            self.child_components.append(j)
            junctions.append(j)

            patch_a = tristates[i].external_patches["EN"]
            patch_b = j.external_patches["S1"]
            self.auto_connect(f"en{i}_j", patch_a, patch_b)

            if i != 1: 
                patch_a = junctions[i - 2].external_patches["A"]
                patch_b = junctions[i - 1].external_patches["S2"]
                self.auto_connect(f"j{i}_out", patch_a, patch_b)
        
        # First tristate enable to first junciton
        patch_a = tristates[0].external_patches["EN"]
        patch_b = junctions[0].external_patches["S2"]
        lines = [patch_a.get_relative_position_to_parent(), 
                (patch_a.get_relative_position_to_parent()[0], 
                    patch_b.get_relative_position_to_parent()[1]),
                patch_b.get_relative_position_to_parent()]
        self.connect(f"tri0_j", patch_a, patch_b, lines=lines)
        
        # External connection to last junciton
        patch_a = junctions[-1].external_patches["A"]
        self.auto_connect("j_out", patch_a, patch_b=add_out, internal_b=False)
        
        # Subtract xor gates configuration
        xor = []
        junctions = []
        for i in range(0, 8):
            component = XorGate(parent=self, position=(77 * i + 26, 170))
            self.child_components.append(component)
            xor.append(component)

            patch_a = ExternalPatch( \
                    parent=self,
                    direction=True,
                    position=(self.get_width()/2 - 40 + 5 * i, 
                        self.get_height()))
            self.external_patches[f"B{i}"] = patch_a
            
            patch_b = component.external_patches["B"]
            position_y = patch_b.get_relative_position_to_parent()[1] + 10 + \
                (3 - i if i < 4 else i - 4) * 5
            lines = [patch_b.get_relative_position_to_parent(), 
                (patch_b.get_relative_position_to_parent()[0] - 5, 
                    patch_b.get_relative_position_to_parent()[1]),
                (patch_b.get_relative_position_to_parent()[0] - 5, 
                    position_y), 
                (patch_a.get_relative_position()[0], position_y),
                patch_a.get_relative_position()]

            self.connect(f"b{i}_xor_b", patch_a, patch_b, 
                    internal_a=False, lines=lines)

            patch_a = component.external_patches["S"]
            patch_b = fullAdders[i].external_patches["B"]
            lines = [patch_a.get_relative_position_to_parent(), 
                (patch_a.get_relative_position_to_parent()[0] + 6, 
                    patch_a.get_relative_position_to_parent()[1]),
                (patch_a.get_relative_position_to_parent()[0] + 6, 
                    patch_a.get_relative_position_to_parent()[1] - 12), 
                (patch_b.get_relative_position_to_parent()[0] - 6, 
                    patch_a.get_relative_position_to_parent()[1] - 12),
                (patch_b.get_relative_position_to_parent()[0] - 6, 
                    patch_b.get_relative_position_to_parent()[1]), 
                patch_b.get_relative_position_to_parent()]
            self.connect(f"tri{i}_xor", patch_a, patch_b, lines=lines)
            
            # External sub connection to junctions for all xors
            patch_a = component.external_patches["A"]
            j = Junction(parent=self, 
                    position=(patch_a.get_relative_position_to_parent()[0] - 5, 
                    sub.get_relative_position()[1])).one_two_junction()
            self.child_components.append(j)
            junctions.append(j)
            patch_b = j.external_patches["S1"]
            self.auto_connect(f"xor{i}_sub", patch_a, patch_b, offcet=-3)

            if i > 0:
                patch_a = j.external_patches["S2"]
                patch_b = junctions[i - 1].external_patches["A"]
                self.auto_connect(f"sub{i}_jun", patch_a, patch_b)

        # First sub junction to cin in the first full adder
        patch_a = junctions[0].external_patches["S2"]
        patch_b = fullAdders[0].external_patches["Cin"]
        lines = [patch_a.get_relative_position_to_parent(), 
            (patch_b.get_relative_position_to_parent()[0] - 2, 
                patch_a.get_relative_position_to_parent()[1]),
            (patch_b.get_relative_position_to_parent()[0] - 2,
                patch_b.get_relative_position_to_parent()[1]),
            patch_b.get_relative_position_to_parent()]
        self.connect("sub_xor0", patch_a, patch_b, lines=lines)

        # External connection to last junction
        patch_a = junctions[-1].external_patches["A"]
        self.auto_connect("sub8_jun", patch_a, sub, internal_b=False)
        
        # Cout from last full adder to external connection
        patch_a = fullAdders[-1].external_patches["Cout"]
        cout.set_relative_position((self.get_width(), patch_a.get_relative_position_to_parent()[1]))
        self.auto_connect("cout", patch_a, cout, internal_b=False)
