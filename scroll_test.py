from cmu_graphics import *
from cmu_graphics import pygameEvent

################################################################################
# Set up scroll wheel
################################################################################

def handlePygameEvent(event, callUserFn, app):
    # pygame.MOUSEWHEEL == 1027
    if event.type == 1027:
        callUserFn('onMouseWheel', (event.x, event.y))

pygameEvent.connect(handlePygameEvent)

################################################################################
# App
################################################################################

def onAppStart(app):
    app.cx = app.width // 2
    app.cy = app.width // 2
    app.r = 20

def redrawAll(app):
    drawCircle(app.cx, app.cy, app.r, fill='cyan')

def onMouseWheel(app, dx, dy):
    print(dx, dy)
    app.cx += dx
    app.cy += dy

runApp()