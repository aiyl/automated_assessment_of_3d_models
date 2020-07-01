import os
import trimesh
import numpy as np
import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv
import check_renders
import check_normals
dir = os.path.abspath(os.curdir)
reference = dir + '/Tests/check1.obj'
solve = dir + '/Tests/separate_face.obj'

def get_renders(file_path, obj_type):
    renders = []
    obj = trimesh.load(file_path, process = False)
    try:
        meshes_list = obj.dump()
        scene = trimesh.Scene(meshes_list)
    except:
        mesh = obj
        scene = mesh.scene()
    #scene.show()
    scene.centroid
    #scene.apply_transform(trimesh.transformations.random_rotation_matrix())
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
            renders.append(file_name)
            png = scene.save_image(resolution=[500, 500], visible=True)
            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()

        except BaseException as E:
            print("unable to save image", str(E))
    return renders
if __name__ == '__main__':
    #check renders
    solve_renders = get_renders(solve, 'solve')
    reference_renders = get_renders(reference, 'reference')
    check_renders = check_renders.Check_renders(reference_renders, solve_renders)
    print('check renders', check_renders.all_points)
    #check material
    mtl1 = parse_mtl.Mtl(reference)
    mtl2 = parse_mtl.Mtl(solve)
    checker = check_materials.Checker(mtl1, mtl2)
    print('material points', checker.pointer())

    #check obj
    obj = parse_obj.Obj(solve)
    check_obj = check_obj.Check(obj)
    print('separate face', check_obj.sep_face_count, 'separate_edge', check_obj.sep_edge_count,'multiply_connected_geometry',
          check_obj.multiply_connected_geometry, 'double vertices', len(obj.double_vertices), 'err_face', obj.err_face)

    #check_uv
    check_uv = check_uv.Check_UV(obj.polygons)
    print( 'percent_busy', check_uv.percent_busy, ' area', check_uv.polygon_areas)
    #check_normals
    check_normals = check_normals.Check_normals(obj.polygons)
    print('err_normal_face', check_normals.err_normals_count)
