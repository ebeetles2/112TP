class set_obj():
    def  __init__(self, set, idn):
        self.set = set
        self.idn = idn

    def get_assignment(self):
        return self.set
    
    def get_id(self):
        return self.idn
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_scope(self):
        return self.scope
    
    def __hash__(self):
        return self.idn
    
    def __str__(self):
        return f"List: {self.set}, ID: {self.idn}"
    
    def __eq__(self, other):
        return self.idn == other.idn