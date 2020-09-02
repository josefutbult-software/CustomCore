from Connection import Connection

class ExternalPatch():
    def __init__(self, parent, direction, position=(0, 0), connection=None):
        self.parent = parent
        self.internal_connection = connection
        self.external_connection = None
        self.direction = direction
        self._position = position
        
    
    def get_relative_position_to_parent(self):
        component_position = self.parent.get_relative_position()
        return (self._position[0] + component_position[0] + self.parent.padding, 
                self._position[1] + component_position[1] + self.parent.padding)


    def get_relative_position(self):
        return self._position
    

    def set_relative_position(self, position):
        self._position = position


    def get_position(self): 
        parent_position = self.parent.get_position()
        return (self._position[0] + parent_position[0],
                self._position[0] + parent_position[1])
        

    def input_connection(self):
        if self.direction and self.internal_connection is not None:
            if self.external_connection is not None:
                self.internal_connection.state = self.external_connection.state
            else:
                self.internal_connection.state = False


    def output_connection(self):
        if not self.direction and \
            self.external_connection is not None and \
            self.internal_connection is not None:
            self.external_connection.state = self.internal_connection.state
