class var_obj():
    def  __init__(self, name, x, y, assignment):
        self.name = name
        self.x = x
        self.y = y
        self.assignment = assignment

    def get_name(self):
        return self.name

    def get_assignment(self):
        return self.assignment
    
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