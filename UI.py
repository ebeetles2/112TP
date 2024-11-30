from cmu_graphics import *
import copy
import test
import json
import list_obj
import var_obj
from PIL import Image

def onAppStart(app):
    app.frame_width, app.frame_height = 1200, 800
    app.dark_purple = color=rgb(32,26,35)
    app.line_purple = color=rgb(77,64,77)
    app.onyx = color=rgb(57, 62, 65)
    app.grayish = color=rgb(219, 205, 198)
    app.light_purple = color=rgb(209,177,200)

    app.prim_color = color=rgb(255, 203, 252)
    app.list_color = color=rgb(87, 98, 255)
    app.dict_color = color=rgb(255, 87, 247)

    app.topbar_width, app.topbar_height = app.frame_width, 85
    app.input_width, app.input_height = 480, app.frame_height - app.topbar_height
    app.visual_width, app.visual_height = app.frame_width - app.input_width, app.frame_height - app.topbar_height

    app.buttonbox_width, app.buttonbox_height = app.input_width, 100
    app.help_x, app.help_y = 110, 20

    app.numberline_x = 35

    app.settings_x, app.settings_y, app.settings_size = 60, 43, 45
    app.setting_move = False
    app.settings_angle = 0

    app.edit_mode = False
    app.visual_mode = False
    app.text_cursor_x, app.text_cursor_y = 55, 100
    app.text_cursor_blink = True

    app.stepsPerSecond = 2

    app.code_x, app.code_y = 55,102
    app.code = '''
def listSum(numbers):
    if not numbers:
        return 0
    else:
	    (f, rest) = numbers
	    return f + listSum(rest)
	
myList = (1, (2, (3, None)))
total = listSum(myList)'''
    app.code_lines = ['']
    app.code_lines_index = 0

    app.trace = ''

    app.indent = 25
    app.line_to_highlight = 1
    app.user_input_json = None
    app.line_number = 0
    app.line_index = 0
    app.lines = []
    app.current_line = None

    app.existing_objects = {}
    app.existing_objects_stack = []
    app.vars_stack = []

    app.data_dict = {
        'line' : None,
        'event' : handleEvent,
        'func_name' : handleFunc,
        'globals' : handleGlobal,
        'stack_locals' : handleLocal,
        'stdout' : handleStdout
    }

    app.visual_dict = {
        "<class 'list'>" : drawList,
        "<class 'str'>" : drawVar,
        "<class 'int'>" : drawVar
    }

    app.output_x, app.output_y = app.input_width + 50, app.topbar_height + 500
    app.globals_x, app.globals_y = app.input_width + 50, app.topbar_height + 70
    app.locals_x, app.locals_y = app.input_width + 50, app.topbar_height + 330

    app.letter_space = 12
    app.line_space = 20
    app.unique_vars = set()
    app.vars = []

def redrawAll(app):
    drawRect(0, 0, app.topbar_width, app.topbar_height, fill=app.dark_purple)
    drawRect(0, app.topbar_height, app.input_width, app.input_height - app.buttonbox_height, fill=app.dark_purple)
    drawRect(app.input_width, app.topbar_height, app.visual_width, app.visual_height, fill=app.dark_purple)
    drawRect(0, app.frame_height - app.buttonbox_height, app.buttonbox_width, app.buttonbox_height, fill = app.dark_purple)

    drawLine(0, app.topbar_height, app.topbar_width, app.topbar_height, fill=app.line_purple, lineWidth=5)
    drawLine(app.input_width, app.topbar_height, app.input_width, app.frame_height, fill=app.line_purple, lineWidth=5)
    drawLine(app.numberline_x, app.topbar_height, app.numberline_x, app.frame_height - app.buttonbox_height, fill=app.line_purple, lineWidth=5)
    drawLine(0, app.frame_height - app.buttonbox_height, app.buttonbox_width, app.frame_height - app.buttonbox_height, fill = app.line_purple, lineWidth = 5)

    settings = Image.open('settings.png')
    drawImage(CMUImage(settings), app.settings_x, app.settings_y, width = app.settings_size, height=app.settings_size, rotateAngle=app.settings_angle, align='center')  
    # drawImage('settings.png', app.settings_x, app.settings_y, width = app.settings_size, height=app.settings_size, rotateAngle=app.settings_angle, align='center')
    drawImage('help.png', app.help_x, app.help_y)
    drawImage('button.png', app.buttonbox_width // 2 - 110, app.frame_height - app.buttonbox_height + 50, align='center')
    drawLabel('RESET', app.buttonbox_width // 2 - 110, app.frame_height - app.buttonbox_height + 50, align='center', size=20, fill=app.dark_purple, bold=True)
    drawImage('button.png', app.buttonbox_width // 2 + 90, app.frame_height - app.buttonbox_height + 50, align='center')
    drawLabel('GENERATE', app.buttonbox_width // 2 + 90, app.frame_height - app.buttonbox_height + 50, align='center', size=20, fill=app.dark_purple, bold=True)

    drawLabel('PyViz', app.topbar_width // 2, app.topbar_height - 43, fill=app.grayish, size=50, font='monospace', bold=True)
    drawCode(app)

    drawLine(app.text_cursor_x, app.text_cursor_y, app.text_cursor_x, app.text_cursor_y + 20, visible=app.text_cursor_blink, fill='white')

    for i in range(len(app.code_lines)):
        drawLabel(app.code_lines[i], app.code_x, app.code_y + i * 20, fill='white', size=20, align = 'top-left', font='monospace')
    # drawLabel(app.code, app.code_x, app.code_y, fill='white', size=20, align='top-left', font='monospace')

    if app.visual_mode:
        drawLabel('Globals:', app.input_width + 50, app.topbar_height + 30, align='left', fill='white', size=16)
        drawLabel('Output:', app.input_width + 50, app.topbar_height + 500, align='left', fill='green', size=16)
        # drawCode(app)
        drawVisual(app)
    
def drawCode(app):
    if app.code == '': return
    i = 1
    for line in app.code.splitlines():
        # print(repr(line))
        line_color = 'white'
        if i == app.line_to_highlight:
            line_color = 'green'
        drawLabel(line, 55, 100 + (i-1) * app.indent, size=20, align='left', fill = line_color)
        i += 1

def drawVisual(app):
    if app.existing_objects_stack == []: return
    # print(app.existing_objects_stack)
    print(app.vars_stack[-1])
    for v in app.vars_stack[-1]:
        type_val = v.get_type()
        val_scope = v.get_scope()
        x = v.get_x()
        y = v.get_y()
        if (str(type_val) == "<class 'str'>" or str(type_val) == "<class 'int'>"):
            drawVar(app, v.get_name(), v.get_assignment(), x, y)
        else:
            drawVar(app, v.get_name(), None, x, y)
        drawPointer(app, v)

    current_existing_objects = app.existing_objects_stack[-1]
    for idn in current_existing_objects:
        obj = current_existing_objects[idn]
        obj_scope = obj.get_scope()
        x = obj.get_x()
        y = obj.get_y()
        app.visual_dict[str(type(obj.get_assignment()))](app, obj, x, y)
        # for idn in obj:
        #     app.visual_dict[obj[][0]](app, obj[idn].get_name(), obj[idn].get_list(), app.globals_x, app.globals_y)
    # if app.current_line == None: return
    # for data in app.current_line:
    #     data_value = app.current_line[data]
    #     if data == 'globals':
    #         for var in data_value:
    #             app.visual_dict[data_value[var][0]](app, var, data_value[var][1], app.globals_x, app.globals_y)
    #     elif data == 'locals':
    #         for var in data_value:
    #             app.visual_dict[data_value[var][0]](app, var, data_value[var][1], app.locals_x, app.locals_y)

def updateStackState(app):
    if app.current_line == None: return
    for data in app.current_line:
        data_value = app.current_line[data]
        if data == 'line': continue
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
            v = var_obj.var_obj(var, app.globals_x, app.globals_y + (i-1) * 40, val[1], 'global')
            if v not in app.unique_vars:
                app.vars.append(v)
                app.unique_vars.add(v)
            else:
                app.vars.remove(v)
                app.vars.append(v)
        elif (type_val == "<class 'list'>"):
            handleList(app, var, val[1], app.globals_x, app.globals_y +  + (i-1) * 40, val[2], 'global')
            # drawList(app, var, val[1], app.globals_x, app.globals_y, val[2])

        i += 1

def handleLocal(app, locals):
    if (len(locals) == 0):
        return
    i = 1
    for var in locals[0][1]:
        # print(var)
        val = locals[0][1][var]
        type_val = val[0]
        if (type_val == "<class 'str'>" or type_val == "<class 'int'>"):
            v = var_obj.var_obj(var, app.locals_x, app.locals_y, val[1], 'local')
            if v not in app.unique_vars:
                app.vars.append(v)
                app.unique_vars.add(v)
        elif (type_val == "<class 'list'>"):
            handleList(app, var, val[1], app.locals_x, app.locals_y, val[2], 'local')
            # drawList(app, var, val[1], app.locals_x, app.locals_y, val[2])
        i += 1

def handleStdout(app, stdout):
    if len(stdout) == 0:
        return
    drawLabel(stdout, app.output_x + 40, app.output_y, fill = 'white')

def handleList(app, var, lst, x, y, idn, scope):
    new_list = list_obj.list_obj(lst, x + 300, y, idn, scope)
    v = var_obj.var_obj(var, x, y, new_list, scope)
    if v not in app.unique_vars:
        app.vars.append(v)
        app.unique_vars.add(v)
    if idn not in app.existing_objects:
        app.existing_objects[idn] = new_list

def handleSet(app, var, lst, x, y, idn, scope):
    new_list = list_obj.list_obj(lst, x + 300, y, idn, scope)
    v = var_obj.var_obj(var, x, y, new_list, scope)
    if v not in app.unique_vars:
        app.vars.append(v)
        app.unique_vars.add(v)
    if idn not in app.existing_objects:
        app.existing_objects[idn] = new_list

def handleDict(app, var, lst, x, y, idn, scope):
    new_list = list_obj.list_obj(lst, x + 300, y, idn, scope)
    v = var_obj.var_obj(var, x, y, new_list, scope)
    if v not in app.unique_vars:
        app.vars.append(v)
        app.unique_vars.add(v)
    if idn not in app.existing_objects:
        app.existing_objects[idn] = new_list

def drawPointer(app, var_obj):
    drawLine(var_obj.get_x() + len(var_obj.get_name()) * app.letter_space + 10, var_obj.get_y(), var_obj.get_x() + len(var_obj.get_name()) * app.letter_space + 90, var_obj.get_y(), fill='white')

def drawList(app, v, x, y):
    # new_list = list_obj.list_obj(list, x, y, id)
    # v = var_obj.var_obj(var, x, y, new_list)
    # print(id(list))
    new_list = v.get_assignment()
    # drawRect(x - 5, y, app.letter_space  * len(var) + 10, app.line_space + 10, align='left', fill=None, border=app.prim_color)
    # drawLabel(var, x, y, size=20, align = 'left', fill='white', font = 'monospace')
    
    if len(new_list) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.list_color)
    else:
        drawRect(x, y, len(new_list) * 20, 20, fill=None, align='left',border=app.list_color)
    for i in range(len(new_list)):
        drawLabel(str(new_list[i]), x + 10 + i * 20, y, fill='white', font='monospace', size=20)
        drawLabel(str(i), x + 10 + i * 20, y - 20, fill='white', font='monospace', size=12)
    
def drawVar(app, var, val, x, y):
    drawRect(x - 5, y, app.letter_space  * len(var) + 10, app.line_space + 10, align='left', fill=None, border=app.prim_color)
    drawLabel(var, x, y, size=20, align = 'left', fill='white', font = 'monospace')
    # print(val)
    if val != None:
        drawLabel(val, x + app.letter_space * len(var) + 100, y, size=20, fill='white', font='monospace')
    # v_string = str(var) + ' =' +  str(val).split('>",')[1][:-1]
    # if str(var) == '__return__':
    #     drawRect(x, y + n * 20, len(v_string) * 5 + 30, 15, fill=None, border='white')
    # else:
    #     drawRect(x, y + n * 20, len(v_string) * 5 + 10, 15, fill=None, border='white')
    # drawLabel(v_string, x + 5, y + n * 20 + 7, align='left', fill = 'white')

def lineUpdate(app, dir):
    if app.line_index + dir >= 0 and app.line_index + dir < len(app.lines):
        app.line_index += dir
        app.current_line = app.lines[app.line_index]

def loadLines(app):
    app.user_input_json = json.loads(app.trace)
    # print(app.user_input_json)
    for line in app.user_input_json:
        app.lines.append(line)
    app.current_line = app.lines[0]

def onMouseDrag(app, mouseX, mouseY):
    if mouseX > 380 and mouseX < app.frame_width - 50 and mouseX > app.input_width - 50 and mouseX < app.input_width + 50:
        app.input_width = mouseX
        app.visual_width, app.visual_height = app.frame_width - app.input_width, app.frame_height - app.topbar_height
        app.buttonbox_width, app.buttonbox_height = app.input_width, 100
        app.output_x, app.output_y = app.input_width + 50, app.topbar_height + 500
        app.globals_x, app.globals_y = app.input_width + 50, app.topbar_height + 70
        app.locals_x, app.locals_y = app.input_width + 50, app.topbar_height + 330

def onMousePress(app, mouseX, mouseY):
    print(str(mouseX) + ', ' + str(mouseY))
    if mouseX > app.numberline_x and mouseX < app.input_width and mouseY > app.topbar_height and mouseY < app.frame_height - app.buttonbox_height:
        app.edit_mode = True
    else:
        app.edit_mode = False

    # Generate and Reset buttons
    if mouseX > app.buttonbox_width // 2 + 10 and mouseX < app.buttonbox_width // 2 + 170 and mouseY > app.frame_height - app.buttonbox_height + 25 and mouseY < app.frame_height - app.buttonbox_height + 70:
        app.trace = test.test_tracing(app.code)
        print(app.trace)
        app.edit_mode = False
        app.visual_mode = True
        loadLines(app)
        # print('clicked')
    elif mouseX > app.buttonbox_width // 2 - 195 and mouseX < app.buttonbox_width // 2 - 30 and mouseY > app.frame_height - app.buttonbox_height + 25 and mouseY < app.frame_height - app.buttonbox_height + 70:
        app.code = ''
        app.code_lines = ['']
        app.code_lines_index = 0
        app.text_cursor_x, app.text_cursor_y = 55, 100
        app.edit_mode = True
        app.visual_mode = False
        app.existing_objects = {}
        app.vars = []
        app.unique_vars = set()
        app.lines = []
        # print('click')
    if app.edit_mode:
        pass

def onMouseMove(app, mouseX, mouseY):
    if mouseX > app.settings_x and mouseX < app.settings_x + app.settings_size and mouseY > app.settings_y and mouseY < app.settings_y + app.settings_size:
        app.setting_move = True
    else:
        app.setting_move = False

def onKeyPress(app, key):
    if app.edit_mode:
        if key == 'backspace':
            if app.code_lines[0] != '':
                app.code = app.code[:-1]
                if app.code_lines[app.code_lines_index] != '':
                    app.code_lines[app.code_lines_index] = app.code_lines[app.code_lines_index][:-1]
                    app.text_cursor_x -= app.letter_space
                else:
                    app.code_lines.pop()
                    app.code_lines_index -= 1
                    app.text_cursor_y -= app.line_space
                    app.text_cursor_x = len(app.code_lines[app.code_lines_index]) * app.letter_space + 60
        elif key == 'space':
            app.code += ' '
            app.code_lines[app.code_lines_index] += ' '
            app.text_cursor_x += app.letter_space
        elif key == 'enter':
            app.code += '\n'
            app.code_lines_index += 1
            app.code_lines.append('')
            app.text_cursor_y += app.line_space
            app.text_cursor_x = 55
        elif key == 'tab':
            app.code += '\t'
            app.code_lines[app.code_lines_index] += '  '
            app.text_cursor_x += app.letter_space * 2
        else:
            app.code += key
            app.code_lines[app.code_lines_index] += key
            app.text_cursor_x += app.letter_space
    else:
        # for ob in app.existing_objects:
        #     print(app.existing_objects[ob])
        # for v in app.vars:
        #     print(str(v))
        # print(len(app.vars))
        if key == 'right':
            if app.line_index < len(app.lines) - 1:
                lineUpdate(app, 1)
                updateStackState(app)
                existing_objects_copy = copy.copy(app.existing_objects)
                app.existing_objects_stack.append(existing_objects_copy)
                vars_copy = copy.copy(app.vars)
                app.vars_stack.append(vars_copy)
        elif key == 'left':
            if app.line_index > 0:
                lineUpdate(app, -1)
                app.vars = []
                app.unique_vars = set()
                app.existing_objects = {}
                updateStackState(app)
                if len(app.existing_objects_stack) > 0:
                    app.existing_objects_stack.pop()
                if len(app.vars_stack) > 0:
                    app.vars_stack.pop()
        if len(app.lines) > 0:
            app.line_to_highlight = app.lines[app.line_index]['line']

def onStep(app):
    app.drawn = True
    if app.setting_move:
        app.settings_angle += 4
    
    if app.edit_mode:
        app.text_cursor_blink = not app.text_cursor_blink
    else:
        app.text_cursor_blink = False

def main():
    runApp(height=800,width=1200)

main()