from cmu_graphics import *
import copy
import test
import json
import list_obj
import var_obj
import frame_stack
import frame_obj
from PIL import Image
import label
from cmu_graphics import pygameEvent

# TODO 
# y is off
# scrollable visuals
# primitive next to var
# margin around text and its box
# highlight lines of current function
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
    app.visual_x, app.visual_y = app.input_width, app.topbar_height
    app.text_x, app.text_y = 0, app.topbar_height
    app.text_width, app.text_height = 1000, 10000
    app.visual_width, app.visual_height = 1000, 10000

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

    app.code_x, app.code_y = app.text_x + 55, app.text_y + 17

#     app.code = '''
# def test(a):
#     if len(a) == 0:
#         return 0
#     else:
#         return a[0] + test(a[1:])
# a = [1, 2, 3, 4, 5]
# b = 'shasd'
# a = {1:3,4:4,3434234:35435435}
# test(a)'''

    app.code = '''def merge_sort(my_list):

    # Base Case
    if len(my_list) <= 1:
        return my_list

    list_1 = my_list[0:len(my_list) // 2]
    list_2 = my_list[len(my_list) // 2:]

       # Induction Step
    ans_1 = merge_sort(list_1)
    ans_2 = merge_sort(list_2)

    # Sorting and merging two sorted list
    sort_list = sort_two_list(ans_1, ans_2)
    return sort_list

# Separate Function to sort and merge 2 sorted lists
def sort_two_list(list_1, list_2):
    final_list = []
    i = 0
    j = 0
    while i < len(list_1) and j < len(list_2):
        if list_1[i] <= list_2[j]:
            final_list.append(list_1[i])
            i += 1
            continue
        final_list.append(list_2[j])
        j += 1

    while i < len(list_1):
        final_list.append(list_1[i])
        i = i + 1

    while j < len(list_2):
        final_list.append(list_2[j])
        j = j + 1

    return final_list


my_list = [3, 1, 4, 5]
ans = merge_sort(my_list)'''
    app.code_lines = ['']
    app.code_lines_index = 0

    app.trace = test.test_tracing(app.code)

    app.frames = frame_stack.frame_stack(app.trace)

    app.indent = 25
    app.line_to_highlight = 1
    app.line_number = 0
    app.line_index = 0
    app.lines = []
    app.current_line = None
    load_lines(app)

    # app.visual_dict = {
    #     "<class 'list'>" : drawList,
    #     "<class 'str'>" : drawVar,
    #     "<class 'int'>" : drawVar
    # }

    app.output_x, app.output_y = app.input_width + 50, app.topbar_height + 500
    app.globals_x, app.globals_y = app.input_width + 50, app.topbar_height + 70
    app.locals_x, app.locals_y = app.input_width + 50, app.topbar_height + 330

    app.letter_space = 12
    app.line_space = 20
    app.unique_vars = set()
    app.vars = []

    app.frames_x, app.frames_y = app.visual_x + 160, app.visual_y + 40
    app.obj_x, app.obj_y = app.visual_x + 350, app.visual_y + 50

    app.labels = []

    app.code_scroll = False
    app.visual_scroll = False

def redrawAll(app):
    drawRect(0, app.text_y, app.text_width, app.text_height, fill=app.dark_purple)
    if app.visual_mode:
        drawCode(app)
    drawRect(0, app.topbar_height, app.numberline_x, app.frame_height - app.topbar_height - app.buttonbox_height, fill=app.dark_purple)
    drawRect(app.visual_x, app.visual_y, app.visual_width, app.visual_height, fill=app.dark_purple)
    drawRect(0, app.frame_height - app.buttonbox_height, app.buttonbox_width, app.buttonbox_height, fill = app.dark_purple)

    drawLine(0, app.topbar_height, app.topbar_width, app.topbar_height, fill=app.line_purple, lineWidth=5)
    drawLine(app.input_width, app.topbar_height, app.input_width, app.frame_height, fill=app.line_purple, lineWidth=5)
    drawLine(app.numberline_x, app.topbar_height, app.numberline_x, app.frame_height - app.buttonbox_height, fill=app.line_purple, lineWidth=5)
    drawLine(0, app.frame_height - app.buttonbox_height, app.buttonbox_width, app.frame_height - app.buttonbox_height, fill = app.line_purple, lineWidth = 5)

    drawImage('button.png', app.buttonbox_width // 2 - 110, app.frame_height - app.buttonbox_height + 50, align='center')
    drawLabel('RESET', app.buttonbox_width // 2 - 110, app.frame_height - app.buttonbox_height + 50, align='center', size=20, fill=app.dark_purple, bold=True)
    drawImage('button.png', app.buttonbox_width // 2 + 90, app.frame_height - app.buttonbox_height + 50, align='center')
    drawLabel('GENERATE', app.buttonbox_width // 2 + 90, app.frame_height - app.buttonbox_height + 50, align='center', size=20, fill=app.dark_purple, bold=True)

    drawLine(app.text_cursor_x, app.text_cursor_y, app.text_cursor_x, app.text_cursor_y + 20, visible=app.text_cursor_blink, fill='white')

    if app.visual_mode:
        objects = draw_objects(app, app.frames, app.obj_x, app.obj_y)
        draw_frames(app, app.frames, objects, app.frames_x, app.frames_y)
    else:
        for i in range(len(app.code_lines)):
            drawLabel(app.code_lines[i], app.code_x, app.code_y + i * 20, fill='white', size=20, align = 'top-left', font='monospace')
    # drawLabel(app.code, app.code_x, app.code_y, fill='white', size=20, align='top-left', font='monospace')

    drawRect(0, 0, app.topbar_width, app.topbar_height, fill=app.dark_purple)
    settings = Image.open('settings.png')
    drawImage(CMUImage(settings), app.settings_x, app.settings_y, width = app.settings_size, height=app.settings_size, rotateAngle=app.settings_angle, align='center')  
    # drawImage('settings.png', app.settings_x, app.settings_y, width = app.settings_size, height=app.settings_size, rotateAngle=app.settings_angle, align='center')
    drawImage('help.png', app.help_x, app.help_y)
    drawLabel('PyViz', app.topbar_width // 2, app.topbar_height - 43, fill=app.grayish, size=50, font='monospace', bold=True)

def drawCode(app):
    if app.code == '': return
    i = 1
    for line in app.code.splitlines():
        # print(repr(line))
        line_color = 'white'
        if i == app.line_to_highlight:
            line_color = 'green'
        drawLabel(line, app.code_x, app.code_y + (i-1) * 20, size=20, align='top-left', fill = line_color, font='monospace')
        i += 1

def draw_objects(app, frames, x, y):
    # print('drawing')
    objects = {}

    for obj in frames.get_objects():
        draw_object(app, obj, objects, x, y)
        y += 120

    for func in list(reversed(frames.get_stack())):
        for obj in func.get_objects():
            draw_object(app, obj, objects, x, y)
            y += 60
    y -= 60
    return objects

def draw_object(app, obj, objects, x, y):
    obj_type = str(type(obj))
    if is_primitive(obj_type):
        return
    obj_id = obj.get_id()
    if obj_id in objects:
        return
    obj_val = obj.get_assignment()
    
    if obj_type == "<class 'list_obj.list_obj'>":
        coords = draw_list(app, obj_val, x, y)
    elif obj_type == "<class 'dict_obj.dict_obj'>":
        coords = draw_dict(app, obj_val, x, y)
    elif obj_type == "<class 'tuple_obj.tuple_obj'>":
        coords = draw_tuple(app, obj_val, x, y)
    elif obj_type == "<class 'set_obj.set_obj'>":
        coords = draw_set(app, obj_val, x, y)
    
    objects[obj_id] = coords

def draw_frames(app, frames, objects, x, y):
    y = draw_frame(app, 'global', frames.get_vars(), objects, x, y)
    # y += 70
    for func in list(reversed(frames.get_stack())):
        y += 50
        y = draw_frame(app, func.get_name(), func.get_vars(), objects, x, y)

def is_primitive(t):
    if t == "<class 'int'>" or t == "<class 'str'>" or t == "<class 'float'>":
        return True
    else:
        return False
    
def draw_frame(app, func, vars, objects, x, y):
    drawRect(x, y, len(func) * 12, 25, fill = None, align = 'right', border = app.prim_color)
    l = label.label(func, x, y)
    draw_name(app, l)
    y += 20
    if len(vars) == 0: return
    # print(vars)
    for var in vars:
        y += 20
        var_type = str(type(var.get_assignment()))
        var_val = var.get_assignment()
        l = label.label(var.get_name(), x, y)
        draw_name(app, l)
        if is_primitive(var_type):
            l = label.label(var_val, x + 300, y)
            draw_value(app, l)
            draw_pointer(app, (x + 300, y), x, y)
        else:
            var_id = var.get_assignment().get_id()
            draw_pointer(app, objects[var_id], x, y)
    return y

def draw_name(app, name):
    drawLabel(str(name.get_label()), name.get_x(), name.get_y(), fill = 'white', font = 'monospace', size = 20, align = 'right')

def draw_value(app, val):
    drawLabel(str(val.get_label()), val.get_x(), val.get_y(), fill='white', font = 'monospace', size=20, align='left')

def draw_pointer(app, coords, x, y):
    drawLine(x + 10, y, coords[0] - 10, coords[1], fill='white', lineWidth = 1)

def draw_list(app, lst, x, y):
    if len(lst) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.list_color)
    else:
        drawRect(x, y, len(lst) * 20, 20, fill=None, align='left',border=app.list_color)
    for i in range(len(lst)):
        drawLabel(str(lst[i]), x + 10 + i * 20, y, fill='white', font='monospace', size=20)
        drawLabel(str(i), x + 10 + i * 20, y - 20, fill='white', font='monospace', size=12)
    return x, y

def draw_dict(app, d, x, y):
    if len(d) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.dict_color)
    else:
        width = get_max_length(d)
        drawRect(x, y, width * 17, len(d) * 25, fill=None, align='left-top',border=app.dict_color)
    i = 0
    for k, v in d.items():
        drawLabel(str(k) + ' : ' + str(v), x + 10, y + 20  * i + 10, fill='white', font='monospace', size=20, align = 'left-top')
        i += 1
    return x, y

def get_max_length(d):
    max_k = 0
    max_v = 0
    for k, v in d.items():
        if len(str(k)) > max_k:
            max_k = len(str(k))
        if len(str(v)) > max_v:
            max_v = len(str(v))
    return max_k + max_v

def draw_set(app, s):
    pass

def draw_tuple(app, t):
    pass

def line_update(app, dir):
    if app.line_index + dir >= 0 and app.line_index + dir < len(app.lines):
        app.line_index += dir
        app.current_line = app.lines[app.line_index]

def load_lines(app):
    t = json.loads(app.trace)
    for l in t:
        app.lines.append(l)
    app.current_line = app.lines[0]

def onMouseDrag(app, mouseX, mouseY):
    if mouseX > 380 and mouseX < app.frame_width - 50 and mouseX > app.input_width - 50 and mouseX < app.input_width + 50:
        app.input_width = mouseX
        app.visual_width, app.visual_height = app.frame_width - app.input_width, app.frame_height - app.topbar_height
        app.buttonbox_width, app.buttonbox_height = app.input_width, 100
        app.output_x, app.output_y = app.input_width + 50, app.topbar_height + 500
        app.globals_x, app.globals_y = app.input_width + 50, app.topbar_height + 70
        app.locals_x, app.locals_y = app.input_width + 50, app.topbar_height + 330
        app.frames_x, app.frames_y = app.input_width + 50, app.topbar_height + 70
        app.obj_x, app.obj_y = app.input_width + 300, app.topbar_height + 70

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
        app.frames = frame_stack.frame_stack(app.trace)
        app.edit_mode = False
        app.visual_mode = True
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
    if mouseX > app.numberline_x and mouseX < app.input_width and mouseY > app.topbar_height and mouseY < app.frame_height - app.buttonbox_height:
        app.code_scroll = True
    else:
        app.code_scroll = False

    if mouseX > app.input_width and mouseX < app.frame_width and mouseY > app.topbar_height and mouseY < app.frame_height:
        app.visual_scroll = True
    else:
        app.visual_scroll = False

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
            # if app.line_index < len(app.lines) - 1:
            app.frames.step_forward()
            line_update(app, 1)
            print(app.frames.get_vars())
        elif key == 'left':
            # if app.line_index > 0:
            app.frames.step_backward()
            line_update(app, -1)
            print(app.frames.get_stack())
        if len(app.lines) > 0:
            print('updated')
            app.line_to_highlight = app.lines[app.line_index]['line']

# scroll wheel code from Austin provided on Ed

def handlePygameEvent(event, callUserFn, app):
    # pygame.MOUSEWHEEL == 1027
    if event.type == 1027:
        callUserFn('onMouseWheel', (event.x, event.y))

pygameEvent.connect(handlePygameEvent)

def onMouseWheel(app, dx, dy):
    dx *= 20
    dy *= 20
    if app.text_y + dy < app.topbar_height and app.code_scroll:
        app.text_y += dy
    if app.text_x - dx < 20 and app.code_scroll:
        app.text_x -= dx

    if app.visual_y - dy < app.topbar_height and app.visual_scroll:
        app.visual_y -= dy
    # if app.visual_x - dx > app.input_width and app.visual_scroll:
    #     app.visual_x += dx
        
    app.frames_x, app.frames_y = app.visual_x + 160, app.visual_y + 40
    app.obj_x, app.obj_y = app.visual_x + 350, app.visual_y + 50
    app.code_x, app.code_y = app.text_x + 55, app.text_y + 30
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