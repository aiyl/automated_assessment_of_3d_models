import os
import trimesh
import numpy as np
import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv

dir = os.path.abspath(os.curdir)
reference = dir + '/Tests/unnormal_box.obj'
solve = dir + '/Tests/check_uv2.obj'

def get_renders(file_path, obj_type):
    obj = trimesh.load(file_path, process=False)
    try:
        meshes_list = obj.dump()
        scene = trimesh.Scene(meshes_list)
    except:
        mesh = obj
        scene = mesh.scene()
    # scene.show()
    rotate = trimesh.transformations.rotation_matrix(
        angle=25,
        direction=[0, 0, 5],
        point=scene.centroid)

    for i in range(4):
        trimesh.constants.log.info('Saving image %d', i)
        camera_old, _geometry = scene.graph[scene.camera.name]
        camera_new = np.dot(camera_old, rotate)
        scene.graph[scene.camera.name] = camera_new
        try:
            file_name = 'renders/render_' + obj_type + str(i) + '.png'
            png = scene.save_image(resolution=[500, 500], visible=True)

            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()

        except BaseException as E:
            print("unable to save image", str(E))

if __name__ == '__main__':
    #check renders
    get_renders(solve, 'solve')
    get_renders(reference, 'reference')

    #check material
    mtl1 = parse_mtl.Mtl(reference)
    mtl2 = parse_mtl.Mtl(solve)
    checker = check_materials.Checker(mtl1, mtl2)

    print('material points', checker.pointer())
    #check obj
    obj = parse_obj.Obj(solve)
    check_obj = check_obj.Check(obj)

    check_uv = check_uv.Check_UV(obj.polygons, obj.uv_coords, obj.all_uv_edge)
    print('uv_intersection', check_uv.uv_intersection, 'percent_busy', check_uv.percent_busy, ' area', check_uv.polygon_areas)
    print('separate face', check_obj.sep_face_count, 'separate_edge', check_obj.sep_edge_count,'multiply_connected_geometry', check_obj.multiply_connected_geometry)

"""    for i in range(len(mtl1.materials)):
        print('mat1', mtl1.materials[i].material_name, mtl1.materials[i].diffuse_color )
    for i in range(len(mtl2.materials)):
        print('mat2', mtl2.materials[i].material_name, mtl2.materials[i].diffuse_color) """
