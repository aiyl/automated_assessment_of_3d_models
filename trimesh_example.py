import numpy as np
import trimesh
import pyglet
from pyglet.gl import *
from trimesh import Trimesh
from trimesh.viewer import windowed, SceneViewer


class Checker():
    def __init__(self, mesh):
        print(mesh)

if __name__ == '__main__':
    obj = trimesh.load('Tests/lego_character.obj', process=False)
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
        print('broken faces ', len(trimesh.repair.broken_faces(mesh))/3)
        #trimesh.repair.fill_holes(mesh)
        print('unnormal normals', trimesh.repair.fix_inversion( mesh , multibody = False ))
        print('winding consistent ',mesh.is_winding_consistent) #winding consistent - непрерывная сетка?
        print('watertight ',mesh.is_watertight)
        print('volume', mesh.is_volume)

        scene = mesh.scene()
        rotate = trimesh.transformations.rotation_matrix(
            angle=25,
            direction=[0, 0, 5],
            point=scene.centroid)

        for i in range(4):
            trimesh.constants.log.info('Saving image %d', i)

            # rotate the camera view transform
            camera_old, _geometry = scene.graph[scene.camera.name]
            camera_new = np.dot(camera_old, rotate)

            # apply the new transform
            scene.graph[scene.camera.name] = camera_new

            # saving an image requires an opengl context, so if -nw
            # is passed don't save the image
            try:
                # increment the file name
                file_name = 'renders/render_' + str(i) + '.png'
                # save a render of the object as a png
                png = scene.save_image(resolution=[500, 500], visible=True)
                with open(file_name, 'wb') as f:
                    f.write(png)
                    f.close()

            except BaseException as E:
                print("unable to save image", str(E))
        #print(mesh.edges_sorted)
#    meshes_list.apply_transform(trimesh.transformations.random_rotation_matrix())

    #meshes.show()
    #checker = Checker(mesh)
    #scene = trimesh.Scene(meshes_list)
    #scene.show()


