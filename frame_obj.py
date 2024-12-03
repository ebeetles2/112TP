import list_obj
import dict_obj
import var_obj

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
        # print(globals)
        for var in self.trace:
            val = self.trace[var]
            type_val = val[0]
            # print(type_val)
            if (type_val == "<class 'str'>" or type_val == "<class 'int'>"):
                v = var_obj.var_obj(var, val[1])
                self.vars.append(v)
                if val[1] not in self.unique_objects:
                    self.objects.append(val[1])
                    self.unique_objects.add(val[1])
            elif (type_val == "<class 'list'>"):
                self.handle_list(var, val[1], val[2])
            elif (type_val == "<class 'dict'>"):
                self.handle_dict(var, val[1], val[2])
    
    def handle_list(self, var, lst, idn):
        new_list = list_obj.list_obj(lst, idn)
        v = var_obj.var_obj(var, new_list)
        self.vars.append(v)
        if new_list not in self.unique_objects:
            self.objects.append(new_list)
            self.unique_objects.add(new_list)

    def handle_dict(self, var, dct, idn):
        new_dict = dict_obj.dict_obj(dct, idn)
        v = var_obj.var_obj(var, new_dict)
        self.vars.append(v)
        if new_dict not in self.unique_objects:
            self.objects.append(new_dict)
            self.unique_objects.add(new_dict)

    def handleSet(self, app, var, lst, x, y, idn, scope):
        new_list = list_obj.list_obj(lst, x + 300, y, idn, scope)
        v = var_obj.var_obj(var, x, y, new_list, scope)
        if v not in app.unique_vars:
            app.vars.append(v)
            app.unique_vars.add(v)
        if idn not in app.existing_objects:
            app.existing_objects[idn] = new_list

    def handleDict(self, app, var, lst, x, y, idn, scope):
        new_list = list_obj.list_obj(lst, x + 300, y, idn, scope)
        v = var_obj.var_obj(var, x, y, new_list, scope)
        if v not in app.unique_vars:
            app.vars.append(v)
            app.unique_vars.add(v)
        if idn not in app.existing_objects:
            app.existing_objects[idn] = new_list

    def __str__(self):
        return f'{self.name} : {self.objects}'