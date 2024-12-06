import var_obj
import json
import frame_obj
import list_obj
import dict_obj
import set_obj
import tuple_obj
import copy

class frame_stack:
    def __init__(self, trace):
        self.trace = trace
        self.stack = []
        self.pointers = {}

        self.unique_objects = set()
        self.objects = []
        self.vars = []

        self.line_index = 0
        self.lines = []
        self.load_lines()
        self.current_line = None

        self.data_dict = {
            'line' : None,
            'event' : self.handle_event,
            'func_name' : self.handle_func,
            'globals' : self.handle_global,
            'stack_locals' : self.handle_local,
            'stdout' : self.handle_stdout
        }

    def step_forward(self):
        self.stack = []
        self.vars = []
        self.unique_objects = set()
        self.objects = []
        self.line_update(1)
        self.update_stack_state()

    def step_backward(self):
        self.stack = []
        self.vars = []
        self.unique_objects = set()
        self.objects = []
        self.line_update(-1)
        self.update_stack_state()

    def line_update(self, dir):
        if self.line_index + dir >= 0 and self.line_index + dir < len(self.lines):
            self.line_index += dir
            self.current_line = self.lines[self.line_index]

    def load_lines(self):
        self.user_input_json = json.loads(self.trace)
        # print(self.user_input_json)
        for line in self.user_input_json:
            self.lines.append(line)
        self.current_line = self.lines[0]

    def get_stack(self):
        return self.stack

    def get_vars(self):
        return self.vars
    
    def get_objects(self):
        return self.objects
    
    def update_stack_state(self):
        if self.current_line == None: return
        for data in self.current_line:
            if data == 'line': continue
            data_value = self.current_line[data]
            self.data_dict[data](data_value)

    def handle_event(self, event):
        pass

    def handle_func(self, func):
        pass
        # if (func != '<module>'):
        #     drawLabel(str(func), 300, 20)

    def handle_global(self, globals):
        if (len(globals) == 0):
            return
        # print(globals)
        for var in globals:
            val = globals[var]
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

    def handle_local(self, locals):
        if (len(locals) == 0):
            return
        for func in locals:
            func_name = func[0]
            func_dict = func[1]
            # print(func_dict)
            new_frame = frame_obj.frame_obj(func_name, func_dict)
            new_frame.handle_frame()
            self.stack.append(new_frame)

    def handle_stdout(self, stdout):
        if len(stdout) == 0:
            return
        pass
