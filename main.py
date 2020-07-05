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
reference = dir + '/Tests/isbaForBlend.obj'
solve = dir + '/Tests/isba/2965575_IS_.obj'

def get_renders(file_path, obj_type):
    renders = []
    obj = trimesh.load(file_path, process = False)
    try:
        meshes_list = obj.dump()
        mesh = meshes_list.sum()
        scene = mesh.scene()
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
    obj = trimesh.load(solve, process=False)
    obj2 = trimesh.load(reference, process=False)
    try:
        v1 = obj.voxelized(pitch=0.25)
    except:
        meshes_list = obj.dump()
        mesh = meshes_list.sum()
        v1 = mesh.voxelized(pitch=0.25)

    try:
        v2 = obj2.voxelized(pitch=0.25)
    except:
        meshes_list = obj2.dump()
        mesh = meshes_list.sum()
        v2 = mesh.voxelized(pitch=0.25)

#    result = list(set(v1) & set(v2))
    c= 0
    nope = 0
    v1.show()
    if v1.points.size >= v2.points.size:
        c = np.in1d(v2.points, v1.points)
        for i in range(len(c)):
            if c[i] == True:
                nope += 1
        percent = (nope*100)/v1.points.size
    else:
        c = np.in1d(v1.points, v2.points)
        for i in range(len(c)):
            if c[i] == True:
                nope += 1
        percent = (nope * 100) / v2.points.size
    print(percent)

    print('check renders', check_renders.all_points)
    #check material
    """
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
    #check_normals = check_normals.Check_normals(obj.polygons)
    check_normals = check_normals.Check_normals(obj.polygons)
    print('err_normal_face', check_normals.err_normals_count)"""
