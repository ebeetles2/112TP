
class list_obj():
    def  __init__(self, lst, x, y, idn, scope):
        self.lst = lst
        self.x = x
        self.y = y
        self.idn = idn
        self.scope = scope

    def get_assignment(self):
        return self.lst
    
    def get_id(self):
        return self.idn
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_scope(self):
        return self.scope
    
    def __str__(self):
        return f"List: {self.lst}, ID: {self.idn}"