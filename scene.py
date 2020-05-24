"""This script shows another example of using the PyWavefront module."""
# This example was created by intrepid94
import ctypes
import os
import sys
from pyglet.window import key
from pyglet.window import mouse
sys.path.append('..')
import pyglet
from pyglet.gl import *
from pywavefront import visualization
from pywavefront import Wavefront

# Create absolute path from this module
file_abspath = os.path.join(os.path.dirname(__file__)+ '\Tests\check_mtl_blend.obj')
plane_path = os.path.join(os.path.dirname(__file__), 'Tests/check4.obj')
rotation = 0.0
pos =[0, 0, -20]
mesh = Wavefront(file_abspath)
plane = Wavefront(plane_path)
meshes = []
meshes.append(mesh)
material = mesh.materials
print(mesh.materials)

window = pyglet.window.Window(1024, 720, caption='Demo', resizable=True)
pyglet.gl.glClearColor(0,0,0,1)
keys = key.KeyStateHandler()
window.push_handlers(keys)
window.push_handlers(pyglet.window.event.WindowEventLogger())
lightfv = ctypes.c_float * 4

@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width) / height, 1.0, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40.0, 200.0, 100.0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)

    # glTranslated(0, 4, -8)
    # glRotatef(90, 0, 1, 0)
    # glRotatef(-60, 0, 0, 1)

    # Rotations for sphere on axis - useful
    glTranslatef(*pos)
    glRotatef(-66.5, 0, 0, 1)
    glRotatef(rotation, 1, 1, 0)
    #glRotatef(90, 0, 0, 1)
    #glRotatef(0, 0, 1, 0)
    visualization.draw(meshes[0])

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y == 1:
        pos[2] -=1
    else:
        pos[2] +=1
    pass

@window.event
def on_key_press(s,m):
    global rotation
    if s == pyglet.window.key.LEFT:
        pos[0] -=1
    if s == pyglet.window.key.RIGHT:
        pos[0] +=1
    if s == pyglet.window.key.DOWN:
        pos[1] -=1
    if s == pyglet.window.key.UP:
        pos[1] +=1
    if s == pyglet.window.key.A:
        rotation +=5
    if rotation > 720.0:
        rotation = 0.0
    if s == pyglet.window.key.D:
        rotation -= 5

@window.event
def on_mouse_press (x,y, button, modifier):
    if button == mouse.RIGHT:
        print('Right mouse was pressed')
    elif button == mouse.LEFT:
        print('Left mouse was pressed')

"""def update(dt):
    global rotation
    global move2
    rotation += 30 * dt

    if rotation > 720.0:
        rotation = 0.0
    if key.LEFT:
        move2 = -5
    if key.RIGHT:
        move2 = 5 """

#pyglet.clock.schedule(update)
pyglet.app.run()