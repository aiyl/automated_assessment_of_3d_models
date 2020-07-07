import os
import sys

import numpy as np
import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv
import check_renders
import check_normals
import trimesh_module

dir = os.path.abspath(os.curdir)
#reference = dir + '/Tests/check1.obj'
#solve = dir + '/Tests/isbaForBlend.obj'
reference = sys.argv[1]
solve = sys.argv[2]
#print(os.listdir(path=dir+'/Tests/isba') )


if __name__ == '__main__':
    """
    #check renders
    trimesh_module = trimesh_module.Trimesh(reference, solve)
    print('voxel compare', trimesh_module.voxel_points)
    """
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
    #check_normals = check_normals.Check_normals(obj.polygons)
    check_normals = check_normals.Check_normals(obj.polygons)
    print('err_normal_face', check_normals.err_normals_count)
