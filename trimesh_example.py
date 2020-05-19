import numpy as np
import trimesh
import pyglet
from pyglet.gl import *
import glooey
from trimesh.viewer import windowed

mesh = trimesh.load('check1.obj')
mesh2 = trimesh.load('check2.obj')
meshes =[]
meshes.append(mesh)
meshes.append(mesh2)
mesh.apply_transform(trimesh.transformations.random_rotation_matrix())
scene = trimesh.Scene(meshes)


#scene.show()

print(mesh.process(validate = False))
print('meshes duplicate faces ',mesh.remove_duplicate_faces())
print('mesh is sealed ', mesh.is_watertight)
#print(mesh.vertex_faces)
#mesh.show()

# transform method can be passed a (4, 4) matrix and will cleanly apply the transform
