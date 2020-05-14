import os
import pyglet
import ratcave as rc
from pyglet.window import key

# Create Window
window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)


# Insert filename into WavefrontReader.
dir = os.path.abspath(os.curdir)
obj_filename = dir + '/check_mtl_blend.obj'
obj_reader = rc.WavefrontReader(obj_filename)
print(obj_reader.bodies.keys())

# Create Mesh
monkey = obj_reader.get_mesh('Cube',position=(0, 0, -1.5), scale=.4)

# Create Scene
scene = rc.Scene(meshes=[monkey])
scene.bgColor = 1, 1, 1

# Functions to Run in Event Loop
def rotate_meshes(dt):
    monkey.rotation.y += 15 * dt  # dt is the time between frames
pyglet.clock.schedule(rotate_meshes)

def move_camera(dt):
    camera_speed = 3
    if keys[key.LEFT]:
        scene.camera.position.x -= camera_speed * dt
    if keys[key.RIGHT]:
        scene.camera.position.x += camera_speed * dt
pyglet.clock.schedule(move_camera)

@window.event
def on_draw():
    with rc.default_shader:
        scene.draw()

pyglet.app.run()