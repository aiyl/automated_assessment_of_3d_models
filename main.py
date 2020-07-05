import os
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
reference = dir + '/Tests/isbaForBlend.obj'
solve = dir + '/Tests/isba/2976376_OK_.obj'
#print(os.listdir(path=dir+'/Tests/isba') )


if __name__ == '__main__':
    #check renders
    trimesh_module = trimesh_module.Trimesh(reference, os.listdir(path=dir+'/Tests/isba'),  dir+'/Tests/isba/')
    print('voxel compare', trimesh_module.voxel_points)
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
