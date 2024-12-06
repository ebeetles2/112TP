class tuple_obj():
    def  __init__(self, t, idn):
        self.t = t
        self.idn = idn
        # self.x = x
        # self.y = y
        # self.idn = idn
        # self.scope = scope

    def get_assignment(self):
        return self.t
    
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
        return f"List: {self.t}, ID: {self.idn}"
    
    def __eq__(self, other):
        return self.idn == other.idn