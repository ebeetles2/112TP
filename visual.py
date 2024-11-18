from cmu_graphics import *
import test
import json
import list_obj

# TODO : add RUNTIME and/or MEMORY
# test if lists in the dictionary is aliased
# QUESTIONS: 
# 1. how to text input directly into the app
# 2. Differentiating between a separate object vs the same object in the json file

def onAppStart(app):
    app.user_input = ''
    app.file_button_x, app.file_button_y = 5, 5
    app.file_button_w, app.file_button_h = 150, 50
    app.output_x, app.output_y = 250, 350
    app.raw_input_string = ''
    app.code_x, app.code_y = 10, 80
    app.globals_x, app.globals_y = 160, 30
    app.locals_x, app.locals_y = 160, 200
    app.indent = 15
    app.line_to_highlight = 1
    app.user_input_json = None
    app.line_number = 0
    app.line_index = 0
    app.lines = []
    app.current_line = None
    app.existing_objects = set()
    app.data_dict = {
        'line' : None,
        'event' : handleEvent,
        'func_name' : handleFunc,
        'globals' : handleGlobal,
        'stack_locals' : handleLocal,
        'stdout' : handleStdout
    }

    app.obj_ids = {}
    app.pointers = {}

    app.visual_dict = {
        "<class 'list'>" : drawList,
        "<class 'str'>" : drawVar,
        "<class 'int'>" : drawVar
    }

def redrawAll(app):
    drawLabel('Enter Code File', app.file_button_w // 2, app.file_button_h // 2, fill='black', size=18)
    drawRect(app.file_button_x, app.file_button_y, app.file_button_w, app.file_button_h, fill=None, border='black')
    drawLabel('Globals:', app.globals_x, app.globals_y, align='left')
    drawLabel('Output:', app.output_x, app.output_y, fill='green', size=16)
    drawCode(app)
    drawVisual(app)

def drawVisual(app):
    if app.current_line == None: return
    for data in app.current_line:
        data_value = app.current_line[data]
        if data == 'line': continue
        print(str(data))
        app.data_dict[data](app, data_value)

def handleEvent(app, event):
    pass

def handleFunc(app, func):
    pass
    # if (func != '<module>'):
    #     drawLabel(str(func), 300, 20)

def handleGlobal(app, globals):
    if (len(globals) == 0):
        return
    i = 1
    # print(globals)
    for var in globals:
        val = globals[var]
        type_val = val[0]
        # print(type_val)
        if (type_val == "<class 'str'>" or type_val == "<class 'int'>"):
            drawVar(app, var, val, app.globals_x, app.globals_y, i)
        elif (type_val == "<class 'list'>"):
            handleList(app, val)

        i += 1

def handleLocal(app, locals):
    if (len(locals) == 0):
        return
    drawLabel(locals[0][0], app.locals_x, app.locals_y, align='left')
    i = 1
    for var in locals[0][1]:
        # print()
        val = locals[0][1][var]
        type_val = val[0]
        print(type_val)
        if (type_val == "<class 'str'>" or type_val == "<class 'int'>"):
            drawVar(app, var, locals[0][1][var], app.locals_x, app.locals_y, i)
        elif (type_val == "<class 'list'>"):
            drawList(app, val[1])
 
        i += 1
    # print(locals)

def handleStdout(app, stdout):
    if len(stdout) == 0:
        return
    drawLabel(stdout, app.output_x + 40, app.output_y)

def handleList(app, val):
    if val[2] not in app.obj_ids:
        app.objs[val[2]] = list_obj.list_obj(list, 300, 300, val[2])
        drawList(app, val[1])
    else:
        app.pointers[val] = app.obj_ids[val[2]]
        drawPointer(app)
        

def drawPointer(app, obj):
    pass

def drawList(app, list, id):
    new_list = list_obj.list_obj(list, 300, 100)
    # print(id(list))
    app.existing_objects.add(new_list)
    i = 0
    for element in list:
        drawLabel(element, new_list.get_x() + 10 * i, new_list.get_y())
        i += 1

def drawVar(app, var, val, x, y, n):
    v_string = str(var) + ' =' +  str(val).split('>",')[1][:-1]
    if str(var) == '__return__':
        drawRect(x, y + n * 20, len(v_string) * 5 + 30, 15, fill=None, border='black')
    else:
        drawRect(x, y + n * 20, len(v_string) * 5 + 10, 15, fill=None, border='black')
    drawLabel(v_string, x + 5, y + n * 20 + 7, align='left')

def drawCode(app):
    if app.raw_input_string == '': return
    i = 1
    for line in app.raw_input_string.splitlines():
        # print(repr(line))
        line_color = 'black'
        if i == app.line_to_highlight:
            line_color = 'green'
        drawLabel(line, app.code_x, app.code_y + (i-1) * app.indent, align='left', fill = line_color)
        i += 1

def onKeyPress(app, key):
    if key == 'right':
        lineUpdate(app, 1)
    elif key == 'left':
        lineUpdate(app, -1)
    if len(app.lines) > 0:
        app.line_to_highlight = app.lines[app.line_index]['line']

def lineUpdate(app, dir):
    if app.line_index + dir >= 0 and app.line_index + dir < len(app.lines):
        app.line_index += dir
        app.current_line = app.lines[app.line_index]

def onMousePress(app, mouseX, mouseY):
    if mouseX <= app.file_button_x + app.file_button_w and mouseX >= app.file_button_x and mouseY <= app.file_button_y + app.file_button_h and mouseY >= app.file_button_y:
        getUserInput(app)
        loadLines(app)

def getUserInput(app):
    raw_input = app.getTextInput('Code File')
    with open(raw_input, 'r') as file:
        app.raw_input_string = file.read()
    # print(app.raw_input_string)
    app.user_input = test.test_tracing(app.raw_input_string)
    print(app.user_input)

def loadLines(app):
    app.user_input_json = json.loads(app.user_input)
    # print(app.user_input_json)
    for line in app.user_input_json:
        app.lines.append(line)
    app.current_line = app.lines[0]

def main():
    runApp(height=500,width=1000)

main()