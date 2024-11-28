# code from original PythonTutor backend github, modified to work for Python 3 and for the needs of this project

import sys
import json
import bdb  # Import the debugger module for stepping through code
import io  # Use io.StringIO instead of cStringIO in Python 3
import inspect

MAX_EXECUTED_LINES = 200
IGNORE_VARS = set(('__stdout__', '__builtins__', '__name__', '__exception__'))

def get_user_stdout(frame):
    return frame.f_globals['__stdout__'].getvalue()

def get_user_globals(frame):
    return filter_var_dict(frame.f_globals)

def get_user_locals(frame):
    return filter_var_dict(frame.f_locals)

def filter_var_dict(d):
    ret = {}
    for (k, v) in d.items():  # Replace iteritems() with items()
        if k not in IGNORE_VARS:
            try:
                json.dumps(v)  # Try serializing the variable
                ret[k] = v

                # sys.stdout = sys.__stdout__
                # if isinstance(v, list):
                #     print(id(v))
                # sys.stdout = tos[0].f_globals['__stdout__']
            except TypeError:
                # ret[k] = f"<non-serializable: {type(v).__name__}>"
                name = v.__name__
                parameters = str(inspect.signature(v))
                ret[k] = name + parameters
                
    return ret

class PGLogger(bdb.Bdb):

    def __init__(self, finalizer_func, ignore_id=False):
        bdb.Bdb.__init__(self)
        self.mainpyfile = ''
        self._wait_for_mainpyfile = 0
        self.finalizer_func = finalizer_func
        self.trace = []
        self.ignore_id = ignore_id

    def reset(self):
        bdb.Bdb.reset(self)
        self.forget()

    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

    def setup(self, f, t):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, t)
        self.curframe = self.stack[self.curindex][0]

    # Override Bdb methods
    def user_call(self, frame, argument_list):
        if self._wait_for_mainpyfile:
            return
        if self.stop_here(frame):
            self.interaction(frame, None, 'call')

    def user_line(self, frame):
        if self._wait_for_mainpyfile:
            if (self.canonic(frame.f_code.co_filename) != "<string>" or 
                frame.f_lineno <= 0):
                return
            self._wait_for_mainpyfile = 0
        self.interaction(frame, None, 'step_line')

    def user_return(self, frame, return_value):
        frame.f_locals['__return__'] = return_value
        self.interaction(frame, None, 'return')

    def user_exception(self, frame, exc_info):
        exc_type, exc_value, exc_traceback = exc_info
        frame.f_locals['__exception__'] = exc_type, exc_value
        if type(exc_type) == type(''):
            exc_type_name = exc_type
        else:
            exc_type_name = exc_type.__name__
        self.interaction(frame, exc_traceback, 'exception')

    # General interaction function
    def interaction(self, frame, traceback, event_type):
        self.setup(frame, traceback)
        tos = self.stack[self.curindex]
        lineno = tos[1]

        encoded_stack_locals = []

        i = self.curindex
        while True:
            cur_frame = self.stack[i][0]
            cur_name = cur_frame.f_code.co_name
            if cur_name == '<module>':
                break

            if cur_name == '<lambda>':
                cur_name = 'lambda on line ' + str(cur_frame.f_code.co_firstlineno)
            elif cur_name == '':
                cur_name = 'unnamed function'

            encoded_locals = {}
            for (k, v) in get_user_locals(cur_frame).items():  # Replace iteritems() with items()
                if k != '__module__':
                    encoded_locals[k] = str(type(v)), v, id(v)

            encoded_stack_locals.append((cur_name, encoded_locals))
            i -= 1

        encoded_globals = {}
        
        for (k, v) in get_user_globals(tos[0]).items():  # Replace iteritems() with items()
            encoded_globals[k] = str(type(v)), v, id(v)

        trace_entry = dict(line=lineno,
                           event=event_type,
                           func_name=tos[0].f_code.co_name,
                           globals=encoded_globals,
                           stack_locals=encoded_stack_locals,
                           stdout=get_user_stdout(tos[0]))

        if event_type == 'exception':
            exc = frame.f_locals['__exception__']
            trace_entry['exception_msg'] = exc[0].__name__ + ': ' + str(exc[1])

        self.trace.append(trace_entry)

        if len(self.trace) >= MAX_EXECUTED_LINES:
            self.trace.append(dict(event='instruction_limit_reached', exception_msg='(stopped after ' + str(MAX_EXECUTED_LINES) + ' steps to prevent possible infinite loop)'))
            self.force_terminate()


        self.forget()

    def _runscript(self, script_str):
        self._wait_for_mainpyfile = 1
        user_builtins = {}
        # for (k, v) in __builtins__.__dict__.items():  # .__dict__ only needed to test this function itself somehow
        for (k, v) in __builtins__.items(): # remove .__dict__ makes object work 
            if k in ('reload', 'input', 'apply', 'open', 'compile', 
                     '__import__', 'file', 'eval', 'execfile',
                     'exit', 'quit', 'raw_input', 'dir', 'globals', 'locals', 'vars', 'compile'):
                continue
            user_builtins[k] = v

        user_stdout = io.StringIO()  # Use io.StringIO instead of cStringIO in Python 3
        sys.stdout = user_stdout

        user_globals = {"__name__": "__main__",
                        "__builtins__": user_builtins,
                        "__stdout__": user_stdout}

        try:
            self.run(script_str, user_globals, user_globals)
        except SystemExit:
            sys.exit(0)
        except:
            trace_entry = dict(event='uncaught_exception')
            exc = sys.exc_info()[1]
            if hasattr(exc, 'lineno'):
                trace_entry['line'] = exc.lineno
            if hasattr(exc, 'offset'):
                trace_entry['offset'] = exc.offset
            if hasattr(exc, 'msg'):
                trace_entry['exception_msg'] = "Error: " + exc.msg
            else:
                trace_entry['exception_msg'] = "Unknown error"
            self.trace.append(trace_entry)
            self.finalize()
            sys.exit(0)

    def force_terminate(self):
        self.finalize()
        sys.exit(0)

    def finalize(self):
        sys.stdout = sys.__stdout__
        assert len(self.trace) <= (MAX_EXECUTED_LINES + 1)
        res = []
        for e in self.trace:
            res.append(e)
            if e['event'] == 'return' and e['func_name'] == '<module>':
                break
        if len(res) >= 2 and res[-2]['event'] == 'exception' and res[-1]['event'] == 'return' and res[-1]['func_name'] == '<module>':
            res.pop()
        self.trace = res
        self.finalizer_func(self.trace)

# Finalizer function to print the trace as human-readable JSON
def finalizer_func(trace):
    global final_trace
    final_trace = json.dumps(trace, indent=4)

# Main testing function to trace the execution of test_code
def test_tracing(script_str):
    logger = PGLogger(finalizer_func)
    logger._runscript(script_str)
    logger.finalize()
    return final_trace

if __name__ == "__main__":
    print(test_tracing('''
def test_function(a, n):
    a = [1, 2, 3, 4, 5]
    for i in range(len(a)):
        if a[i] == n:
            return i

a = [1, 2, 3, 4, 5]
n = 3
z = test_function(a, n)'''))
