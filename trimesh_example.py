import numpy as np
import trimesh
import pyglet
from csg.core import CSG
from pyglet.gl import *
import glooey
from trimesh import Trimesh
from trimesh.viewer import windowed, SceneViewer


class Checker():
    def __init__(self, mesh):
        print(mesh)

if __name__ == '__main__':
    obj = trimesh.load('Tests/unnormal.obj', process=False)
    try:
        meshes_list = obj.dump()
        meshes = meshes_list.sum()
        print(meshes.vertex_faces)
        print('winding consistent for list ', meshes.is_winding_consistent)
        print('watertight ', meshes.is_watertight)
        print('volume', meshes.is_volume)
    except:
        mesh = obj
     #  print('face_adjacency_edges', mesh.face_adjacency_edges)
     #  print('face_adjacency', mesh.face_adjacency)
     #   print('mesh.edges_face', mesh.edges_face)
        print('adjacency_projections', trimesh.convex.adjacency_projections)
        print('is convex', trimesh.convex.is_convex(mesh))
        print('broken faces ', trimesh.repair.broken_faces(mesh))
        #trimesh.repair.fill_holes(mesh)
        print('unnormal normals', trimesh.repair.fix_inversion( mesh , multibody = False ))
        print('winding consistent ',mesh.is_winding_consistent) #winding consistent - непрерывная сетка?
        print('watertight ',mesh.is_watertight)
        print('volume', mesh.is_volume)
        #mesh.show()
        #print(mesh.edges_sorted)
#    meshes_list.apply_transform(trimesh.transformations.random_rotation_matrix())

    #meshes.show()
    #checker = Checker(mesh)
    #scene = trimesh.Scene(meshes_list)
    #scene.show()


