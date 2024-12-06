class var_obj():
    def  __init__(self, name, assignment):
        self.name = name
        self.assignment = assignment

    def get_name(self):
        return self.name

    def get_assignment(self):
        return self.assignment
    
    def get_type(self):
        return type(self.assignment)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def change_assignment(self, assignment):
        self.assignment = assignment

    def get_scope(self):
        return self.scope

    def __str__(self):
        return f"Object: {self.name}, Assignment: {self.assignment}"
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)