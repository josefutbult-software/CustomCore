import pygame

BLACK = (0, 0, 0)
RED = (200, 0, 0)

class Connection:
    def __init__(self, parent):
        self.state = False
        # ((start x, start y), (end x, end y))
        self.lines = []
        self.rendered = False
        self.parent = parent


    def render(self, screen, screen_position):
        if not self.rendered:  
            parent_position = self.parent.get_position()
            for instance in self.lines:
                pygame.draw.line(screen, 
                        RED if self.state else BLACK, 
                        (instance[0][0] + parent_position[0] + screen_position[0], 
                        instance[0][1] + parent_position[1] + screen_position[1]),
                        (instance[1][0] + parent_position[0] + screen_position[0], 
                        instance[1][1] + parent_position[1] + screen_position[1]),
                        2)
            self.rendered = True


    def auto_line(self, point_a, point_b, offcet=0):
        if point_a[1] != point_b[1]:
            self.lines.append((point_a, 
                (point_a[0] + (point_b[0] - point_a[0])/2 + offcet, point_a[1]))) 
            
            self.lines.append(((point_a[0] + 
                    (point_b[0] - point_a[0])/2 + offcet, point_a[1]), 
                (point_a[0] + (point_b[0] - point_a[0])/2 + offcet, point_b[1]))) 

            self.lines.append((point_b, 
                (point_a[0] + (point_b[0] - point_a[0])/2 + offcet, point_b[1])))
        else:
            self.lines.append((point_a, point_b))


