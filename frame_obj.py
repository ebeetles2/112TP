import list_obj
import dict_obj
import var_obj
import tuple_obj
import set_obj

class frame_obj:
    def __init__(self, name, trace):
        self.name = name
        self.trace = trace
        self.objects = []
        self.vars = []
        self.unique_objects = set()

    def get_name(self):
        return self.name
    
    def get_vars(self):
        return self.vars
    
    def get_objects(self):
        return self.objects

    def handle_frame(self):
        if (len(self.trace) == 0):
            return
        for var in self.trace:
            val = self.trace[var]
            type_val = val[0]
            if (type_val == "<class 'str'>" or type_val == "<class 'int'>"):
                v = var_obj.var_obj(var, val[1])
                self.vars.append(v)
                if val[1] not in self.unique_objects:
                    self.objects.append(val[1])
                    self.unique_objects.add(val[1])
            elif (type_val == "<class 'list'>"):
                self.handle_list(var, val[1], val[2])
            elif (type_val == "<class 'tuple'>"):
                self.handle_tuple(var, val[1], val[2])
            elif (type_val == "<class 'dict'>"):
                self.handle_dict(var, val[1], val[2])
            elif (type_val == "<class 'set'>"):
                self.handle_set(var, val[1], val[2])
    
    def handle_list(self, var, lst, idn):
        new_list = list_obj.list_obj(lst, idn)
        v = var_obj.var_obj(var, new_list)
        self.vars.append(v)
        if new_list not in self.unique_objects:
            self.objects.append(new_list)
            self.unique_objects.add(new_list)

    def handle_tuple(self, var, t, idn):
        new_tuple = tuple_obj.tuple_obj(t, idn)
        v = var_obj.var_obj(var, new_tuple)
        self.vars.append(v)
        if new_tuple not in self.unique_objects:
            self.objects.append(new_tuple)
            self.unique_objects.add(new_tuple)

    def handle_dict(self, var, dct, idn):
        new_dict = dict_obj.dict_obj(dct, idn)
        v = var_obj.var_obj(var, new_dict)
        self.vars.append(v)
        if new_dict not in self.unique_objects:
            self.objects.append(new_dict)
            self.unique_objects.add(new_dict)

    def handle_set(self, var, st, idn):
        new_set = set_obj.set_obj(st, idn)
        v = var_obj.var_obj(var, new_set)
        self.vars.append(v)
        if new_set not in self.unique_objects:
            self.objects.append(new_set)
            self.unique_objects.add(new_set)
    def __str__(self):
        return f'{self.name} : {self.objects}'