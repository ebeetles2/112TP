from cmu_graphics import *
import produce_trace
import json
import frame_stack
from PIL import Image
import label
from cmu_graphics import pygameEvent

def onAppStart(app):
    app.frame_width, app.frame_height = 1200, 800
    app.dark_purple = color=rgb(32,26,35)
    app.line_purple = color=rgb(77,64,77)
    app.onyx = color=rgb(57, 62, 65)
    app.grayish = color=rgb(219, 205, 198)
    app.light_purple = color=rgb(209,177,200)
    app.orange = color=rgb(255, 92, 0)

    app.bg_color = app.dark_purple
    app.text_color = 'white'

    app.prim_color = color=rgb(255, 203, 252)
    app.list_color = color=rgb(87, 98, 255)
    app.tuple_color = color=rgb(68, 198, 25)
    app.dict_color = color=rgb(255, 87, 247)

    app.topbar_width, app.topbar_height = app.frame_width, 85
    app.input_width, app.input_height = 480, app.frame_height - app.topbar_height
    app.visual_x, app.visual_y = app.input_width, app.topbar_height
    app.text_x, app.text_y = 0, app.topbar_height
    app.text_width, app.text_height = 2000, 10000
    app.visual_width, app.visual_height = 1000, 10000

    app.buttonbox_width, app.buttonbox_height = app.input_width, 100
    app.help_x, app.help_y, app.help_size = 130, 43, 20

    app.numberline_x = 35

    app.settings_x, app.settings_y, app.settings_size = 60, 43, 20
    app.setting_move = False
    app.settings_angle = 0

    app.edit_mode = False
    app.visual_mode = False
    app.text_cursor_x, app.text_cursor_y = app.text_x + 55, app.text_y + 15
    app.text_cursor_blink = True

    app.stepsPerSecond = 2
    
    app.code_x, app.code_y = app.text_x + 55, app.text_y + 17

    app.code = ''
    app.code_lines = ['']
    app.code_lines_index = 0

    app.trace = produce_trace.produce_trace(app.code)

    app.frames = frame_stack.frame_stack(app.trace)

    app.indent = 25
    app.line_to_highlight = 1
    app.line_number = 0
    app.line_index = 0
    app.lines = []
    app.current_line = None

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

    app.settings_mode = False
    app.color_mode = 'Dark Mode'

    app.file_button_x, app.file_button_y = app.help_x + 60, app.help_y - 23
    app.file_button_w, app.file_button_h = 180, 50
    app.help_mode = False

def redrawAll(app):
    drawRect(0, app.text_y, app.text_width, app.text_height, fill=app.bg_color)
    draw_text(app)

    draw_panels(app)
    draw_visuals(app)
    draw_topbar(app)

    if app.settings_mode:
        draw_settings(app)

    if app.help_mode:
        draw_help(app)

def draw_text(app):
    if app.visual_mode:
        draw_code(app)
    else:
        for i in range(len(app.code_lines)):
            drawLabel(app.code_lines[i], app.code_x, app.code_y + i * 20, fill=app.text_color, size=20, align = 'top-left', font='monospace')

def draw_visuals(app):
    if app.visual_mode:
        objects = draw_objects(app, app.frames, app.obj_x, app.obj_y)
        draw_frames(app, app.frames, objects, app.frames_x, app.frames_y)

def draw_help(app):
    drawRect(140, 285, 280, 90, fill=app.list_color)
    drawLabel('Write your code here,', 150, 295, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('or enter file above.', 150, 315, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('Press generate to', 150, 335, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('visualize', 150, 355, font='monospace', size=20, fill = app.text_color, align='left')
    drawRect(395, 533, 400, 30, fill=app.list_color)
    drawLabel('Drag this line to resize panels',405, 543, font='monospace', size=20, fill = app.text_color, align='left')
    drawRect(656, 202, 300, 100, fill=app.list_color)
    drawLabel('Your visualized code', 666, 212, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('will appear in here.', 666, 232, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('Press left and right', 666, 252, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('arrows to step through', 666, 272, font='monospace', size=20, fill = app.text_color, align='left')
    drawRect(394, 23, 280, 90, fill=app.list_color)
    drawLabel('Enter your file here,', 404, 33, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('or write code below.', 404, 53, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('Press generate to', 404, 73, font='monospace', size=20, fill = app.text_color, align='left')
    drawLabel('visualize', 404, 93, font='monospace', size=20, fill = app.text_color, align='left')

def draw_topbar(app):
    drawRect(0, 0, app.topbar_width, app.topbar_height, fill=app.bg_color)
    settings = Image.open('settings.png')
    drawImage(CMUImage(settings), app.settings_x, app.settings_y, width = 45, height=45, rotateAngle=app.settings_angle, align='center')
    hlp = Image.open('help.png')  
    drawImage(CMUImage(hlp), app.help_x, app.help_y, width = 50, height=50, align='center')
    drawLabel('ENTER CODE FILE', app.file_button_x + 7, app.file_button_y + app.file_button_h // 2, fill=app.light_purple, size=18, font='monospace', align='left', bold = True)
    drawRect(app.file_button_x, app.file_button_y, app.file_button_w, app.file_button_h, fill=None, border=app.light_purple)
    drawLabel('PyViz', app.topbar_width // 2, app.topbar_height - 43, fill=app.grayish, size=50, font='monospace', bold=True)

def draw_panels(app):
    drawRect(0, app.topbar_height, app.numberline_x, app.frame_height - app.topbar_height - app.buttonbox_height, fill=app.bg_color)
    
    drawRect(app.visual_x, app.visual_y, app.visual_width, app.visual_height, fill=app.bg_color)
    draw_line_numbers(app)
    drawLine(app.text_cursor_x, app.text_cursor_y, app.text_cursor_x, app.text_cursor_y + 20, visible=app.text_cursor_blink, fill=app.text_color)
    drawRect(0, app.frame_height - app.buttonbox_height, app.buttonbox_width, app.buttonbox_height, fill = app.bg_color)

    drawLine(0, app.topbar_height, app.topbar_width, app.topbar_height, fill=app.line_purple, lineWidth=5)
    drawLine(app.input_width, app.topbar_height, app.input_width, app.frame_height, fill=app.line_purple, lineWidth=5)
    drawLine(app.numberline_x, app.topbar_height, app.numberline_x, app.frame_height - app.buttonbox_height, fill=app.line_purple, lineWidth=5)
    drawLine(0, app.frame_height - app.buttonbox_height, app.buttonbox_width, app.frame_height - app.buttonbox_height, fill = app.line_purple, lineWidth = 5)

    drawImage('button.png', app.buttonbox_width // 2 - 110, app.frame_height - app.buttonbox_height + 50, align='center')
    drawLabel('RESET', app.buttonbox_width // 2 - 110, app.frame_height - app.buttonbox_height + 50, align='center', size=20, fill=app.bg_color, bold=True)
    drawImage('button.png', app.buttonbox_width // 2 + 90, app.frame_height - app.buttonbox_height + 50, align='center')
    drawLabel('GENERATE', app.buttonbox_width // 2 + 90, app.frame_height - app.buttonbox_height + 50, align='center', size=20, fill=app.bg_color, bold=True)


def draw_settings(app):
    color_button = None
    if app.color_mode == "Dark Mode":
        color_button = "Light Mode"
    else:
        color_button = "Dark Mode"
    drawRect(0,0,app.frame_width,app.frame_height,fill=app.bg_color)
    drawLabel('PyViz', app.topbar_width // 2, app.topbar_height - 43, fill=app.grayish, size=50, font='monospace', bold=True)
    drawLine(0, app.topbar_height, app.topbar_width, app.topbar_height, fill=app.line_purple, lineWidth=5)
    settings = Image.open('settings.png')
    drawImage(CMUImage(settings), app.settings_x, app.settings_y, width = 45, height=45, rotateAngle=app.settings_angle, align='center')
    drawImage('button.png', app.frame_width // 2, app.frame_height // 2, align='center')
    drawLabel(color_button, app.frame_width // 2, app.frame_height // 2, align='center', fill=app.onyx, font='monospace', size=20, bold = True)

def draw_code(app):
    i = 1
    for line in app.code_lines:
        line_color = app.text_color
        if i == app.line_to_highlight:
            line_color = 'green'
        drawLabel(line, app.code_x, app.code_y + (i-1) * 20, size=20, align='top-left', fill = line_color, font='monospace')
        i += 1

def draw_line_numbers(app):
    for i in range(1, len(app.code_lines) + 1):
        line_color = app.text_color
        if i == app.line_to_highlight:
            line_color = 'green'
        drawLabel(str(i), 25, app.code_y + (i-1) * 20, size=20, align='top-right', fill = line_color, font='monospace')

def draw_objects(app, frames, x, y):
    objects = {}

    i = 0
    for obj in frames.get_objects():
        
        if i > 0:
            y += 120
        draw_object(app, obj, objects, x, y)
        i += 1
    for func in list(reversed(frames.get_stack())):
        i = 0
        for obj in func.get_objects():
            
            if i > 0:
                y += 60
            draw_object(app, obj, objects, x, y)
            i += 1
            
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
    y = draw_frame(app, 'global', frames.get_vars(), objects, x, y, False)
    for func in list(reversed(frames.get_stack())):
        current = False
        if func == frames.get_stack()[0]:
            current = True
        y += 50
        y = draw_frame(app, func.get_name(), func.get_vars(), objects, x, y, current)

def is_primitive(t):
    if t == "<class 'int'>" or t == "<class 'str'>" or t == "<class 'float'>":
        return True
    else:
        return False
    
def draw_frame(app, func, vars, objects, x, y, current):
    drawRect(x, y, len(func) * 12, 25, fill = None, align = 'right', border = app.prim_color)
    l = label.label(func, x, y)
    draw_name(app, l)
    y += 20
    if len(vars) == 0: return
    for var in vars:
        y += 20
        var_type = str(type(var.get_assignment()))
        var_val = var.get_assignment()

        pointer_color = app.text_color
        pointer_thickness = 1
        if current:
            pointer_color = app.dict_color
            pointer_thickness = 2
        if is_primitive(var_type):
            draw_value(app, var.get_name(), var_val, x, y)
        else:
            l = label.label(var.get_name(), x, y)
            draw_name(app, l)
            var_id = var.get_assignment().get_id()
            draw_pointer(app, objects[var_id], x, y, pointer_color, pointer_thickness)
    return y

def draw_name(app, name):
    drawLabel(str(name.get_label()), name.get_x(), name.get_y(), fill = app.text_color, font = 'monospace', size = 20, align = 'right')

def draw_value(app, name, val, x, y):
    drawLabel(str(name) + ' : ' + str(val), x, y, fill=app.orange, font = 'monospace', size=20, align='right')

def draw_pointer(app, coords, x, y, pointer_color, pointer_thickness):
    drawLine(x + 10, y, coords[0] - 10, coords[1], fill = pointer_color, lineWidth = pointer_thickness)

def draw_list(app, lst, x, y):
    if len(lst) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.list_color)
    else:
        drawRect(x, y, len(lst) * 20, 20, fill=None, align='left',border=app.list_color)
    for i in range(len(lst)):
        drawLabel(str(lst[i]), x + 10 + i * 20, y, fill=app.text_color, font='monospace', size=20)
        drawLabel(str(i), x + 10 + i * 20, y - 20, fill=app.text_color, font='monospace', size=12)
    return x, y

def draw_dict(app, d, x, y):
    if len(d) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.dict_color)
    else:
        width = get_max_length(d)
        drawRect(x, y, (width + 3) * 13 + 10, len(d) * 25 + 5, fill=None, align='left-top',border=app.dict_color)
    i = 0
    for k, v in d.items():
        drawLabel(str(k) + ' : ' + str(v), x + 10, y + 20  * i + 10, fill=app.text_color, font='monospace', size=20, align = 'left-top')
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

def draw_set(app, s, x, y):
    if len(s) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.list_color)
    else:
        drawRect(x, y, len(s) * 20, 20, fill=None, align='left',border=app.list_color)
    i = 0
    for e in s:
        drawLabel(str(e), x + 10 + i * 20, y, fill=app.text_color, font='monospace', size=20)
        i += 1
    return x, y

def draw_tuple(app, t, x, y):
    if len(t) == 0:
        drawRect(x, y, 20, 20, fill=None, align='left',border=app.tuple_color)
    else:
        drawRect(x, y, len(t) * 20, 20, fill=None, align='left',border=app.tuple_color)
    for i in range(len(t)):
        drawLabel(str(t[i]), x + 10 + i * 20, y, fill=app.text_color, font='monospace', size=20)
        drawLabel(str(i), x + 10 + i * 20, y - 20, fill=app.text_color, font='monospace', size=12)
    return x, y

def line_update(app, dir):
    if app.line_index + dir >= 0 and app.line_index + dir < len(app.lines):
        app.line_index += dir
        app.current_line = app.lines[app.line_index]

def load_lines(app):
    t = json.loads(app.trace)
    for l in t:
        app.lines.append(l)
    app.current_line = app.lines[0]

def mouse_on_line(app, mouseX):
    if mouseX > 380 and mouseX < app.frame_width - 50 and mouseX > app.input_width - 50 and mouseX < app.input_width + 50:
        return True
    return False
def update_bounds(app, mouseX):
    app.input_width = mouseX
    app.visual_x, app.visual_y = app.input_width, app.topbar_height
    app.text_x, app.text_y = 0, app.topbar_height
    app.text_width, app.text_height = 2000, 10000
    app.visual_width, app.visual_height = 1000, 10000
    app.buttonbox_width, app.buttonbox_height = app.input_width, 100

    app.output_x, app.output_y = app.input_width + 50, app.topbar_height + 500
    app.globals_x, app.globals_y = app.input_width + 50, app.topbar_height + 70
    app.locals_x, app.locals_y = app.input_width + 50, app.topbar_height + 330

    app.frames_x, app.frames_y = app.visual_x + 160, app.visual_y + 40
    app.obj_x, app.obj_y = app.visual_x + 350, app.visual_y + 50
    
def onMouseDrag(app, mouseX, mouseY):
    if mouse_on_line(app, mouseX):
        update_bounds(app, mouseX)

def generate_pressed(app, mouseX, mouseY):
    if mouseX > app.buttonbox_width // 2 + 10 and mouseX < app.buttonbox_width // 2 + 170 and mouseY > app.frame_height - app.buttonbox_height + 25 and mouseY < app.frame_height - app.buttonbox_height + 70:
        return True
    return False

def generate(app):
    app.trace = produce_trace.produce_trace(app.code)
    app.frames = frame_stack.frame_stack(app.trace)
    app.edit_mode = False
    app.visual_mode = True
    load_lines(app)

def reset_pressed(app, mouseX, mouseY):
    if mouseX > app.buttonbox_width // 2 - 195 and mouseX < app.buttonbox_width // 2 - 30 and mouseY > app.frame_height - app.buttonbox_height + 25 and mouseY < app.frame_height - app.buttonbox_height + 70:
        return True
    return False

def reset(app):
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
    app.line_to_highlight = 1
    app.line_index = 0

def editor_pressed(app, mouseX, mouseY):
    if mouseX > app.numberline_x and mouseX < app.input_width and mouseY > app.topbar_height and mouseY < app.frame_height - app.buttonbox_height:
        return True
    return False

def swap_colors(app):
    if app.color_mode == "Dark Mode":
        app.color_mode = "Light Mode"
        app.text_color = 'black'
        app.bg_color = 'white'
    else:
        app.color_mode = "Dark Mode"
        app.text_color = 'white'
        app.bg_color = app.dark_purple

def mouse_on_color(app, mouseX, mouseY):
    if mouseX > app.frame_width // 2 - 80 and mouseX < app.frame_width // 2 + 80 and mouseY > app.frame_height // 2 - 23 and mouseY < app.frame_height // 2 + 23:
        return True
    return False

def get_user_input(app):
    raw_input = app.getTextInput('Code File')
    with open(raw_input, 'r') as file:
        app.raw_input_string = file.read()
    app.code = app.raw_input_string

def convert_user_input(app):
    app.code_lines = []
    for line in app.code.splitlines():
        app.code_lines.append(line)

def mouse_on_input_file_button(app, mouseX, mouseY):
    if mouseX > app.file_button_x and mouseX < app.file_button_x + app.file_button_w and mouseY > app.file_button_y and mouseY < app.file_button_y + app.file_button_h:
        return True
    return False

def mouse_on_help(app, mouseX, mouseY):
    if mouseX > app.help_x - app.help_size and mouseX < app.help_x + app.help_size and mouseY > app.help_y - app.help_size and mouseY < app.help_y + app.help_size:
        return True
    return False

def onMousePress(app, mouseX, mouseY):
    if editor_pressed(app, mouseX, mouseY):
        app.edit_mode = True
    else:
        app.edit_mode = False

    if generate_pressed(app, mouseX, mouseY):
        generate(app)
    elif reset_pressed(app, mouseX, mouseY):
        reset(app)
    
    if mouse_on_settings(app, mouseX, mouseY) and not app.settings_mode:
        app.settings_mode = True
    elif mouse_on_settings(app, mouseX, mouseY):
        app.settings_mode = False

    if mouse_on_help(app, mouseX, mouseY) and not app.help_mode:
        app.help_mode = True
    else:
        app.help_mode = False
    
    if mouse_on_color(app, mouseX, mouseY) and app.settings_mode:
        swap_colors(app)

    if mouse_on_input_file_button(app, mouseX, mouseY):
        get_user_input(app)
        convert_user_input(app)

def mouse_on_settings(app, mouseX, mouseY):
    if mouseX > app.settings_x - app.settings_size and mouseX < app.settings_x + app.settings_size and mouseY > app.settings_y - app.settings_size and mouseY < app.settings_y + app.settings_size:
        return True
    return False

def mouse_on_code_panel(app, mouseX, mouseY):
    if mouseX > app.numberline_x and mouseX < app.input_width and mouseY > app.topbar_height and mouseY < app.frame_height - app.buttonbox_height:
        return True
    return False

def mouse_on_visual_panel(app, mouseX, mouseY):
    if mouseX > app.input_width and mouseX < app.frame_width and mouseY > app.topbar_height and mouseY < app.frame_height:
        return True
    return False

def onMouseMove(app, mouseX, mouseY):
    if mouse_on_settings(app, mouseX, mouseY):
        app.setting_move = True
    else:
        app.setting_move = False
    if mouse_on_code_panel(app, mouseX, mouseY):
        app.code_scroll = True
    else:
        app.code_scroll = False

    if mouse_on_visual_panel(app, mouseX, mouseY):
        app.visual_scroll = True
    else:
        app.visual_scroll = False

def onKeyPress(app, key):
    if app.edit_mode:
        if key == 'backspace':
            app.code = app.code[:-1]
            if app.code_lines[0] != '':
                if app.code_lines[app.code_lines_index] != '':
                    app.code_lines[app.code_lines_index] = app.code_lines[app.code_lines_index][:-1]
                    app.text_cursor_x -= app.letter_space
                else:
                    app.code_lines.pop()
                    app.code_lines_index -= 1
                    app.text_cursor_y -= app.line_space
                    app.text_cursor_x = len(app.code_lines[app.code_lines_index]) * app.letter_space + 55
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
        if key == 'right':
            app.frames.step_forward()
            line_update(app, 1)
        elif key == 'left':
            app.frames.step_backward()
            line_update(app, -1)
        if len(app.lines) > 0:
            app.line_to_highlight = app.lines[app.line_index]['line']

# scroll wheel code from Austin provided on Ed
def handlePygameEvent(event, callUserFn, app):
    if event.type == 1027:
        callUserFn('onMouseWheel', (event.x, event.y))

pygameEvent.connect(handlePygameEvent)

def onMouseWheel(app, dx, dy):
    dx *= 20
    dy *= 20
    if app.text_y + dy < app.topbar_height and app.code_scroll:
        app.text_y += dy
        app.text_cursor_y += dy
    if app.text_x - dx < 20 and app.code_scroll:
        app.text_x -= dx
        app.text_cursor_x -= dx

    if app.visual_y - dy < app.topbar_height + 20 and app.visual_scroll:
        app.visual_y -= dy
    
    app.frames_x, app.frames_y = app.visual_x + 160, app.visual_y + 40
    app.obj_x, app.obj_y = app.visual_x + 350, app.visual_y + 50
    app.code_x, app.code_y = app.text_x + 55, app.text_y + 35

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