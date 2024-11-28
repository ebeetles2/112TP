
class list_obj():
    def  __init__(self, lst, x, y, idn):
        self.list = lst
        self.x = x
        self.y = y
        self.id = idn

    def get_list(self):
        return self.lst
    
    def get_id(self):
        return self.idn
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y