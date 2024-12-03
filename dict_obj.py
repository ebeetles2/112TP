
class dict_obj():
    def  __init__(self, dct, idn):
        self.dct = dct
        self.idn = idn
        # self.x = x
        # self.y = y
        # self.idn = idn
        # self.scope = scope

    def get_assignment(self):
        return self.dct
    
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
        return f"Dict: {self.dct}, ID: {self.idn}"
    
    def __eq__(self, other):
        return self.idn == other.idn