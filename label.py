class label():
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y

    def get_label(self):
        return self.label
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def __hash__(self):
        return hash(self.label)
    
    def __eq__(self, other):
        return self.label == other.label