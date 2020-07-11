import os
import sys
import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv
#import check_normals
import check_renders
import  accrue_points
import voxel_compare

reference = sys.argv[1]
solve = sys.argv[2]


if __name__ == '__main__':
    #check renders
    renders = check_renders.Trimesh(reference, solve)
    print('renders points', renders.render_points)
    voxels = voxel_compare.Voxel(reference, solve)
    point0 = trimesh_module.voxel_points
    point1 = trimesh_module.render_points

    #check material
#    mtl1 = parse_mtl.Mtl(reference)
    mtl1 = parse_mtl.Mtl(reference)
    mtl2 = parse_mtl.Mtl(solve)
    checker = check_materials.Checker(mtl1, mtl2)
    print('material points', checker.pointer())

    #check obj
    obj = parse_obj.Obj(solve)
    check_obj = check_obj.Check(obj)
    print('separate face', check_obj.sep_face_count, 'separate_edge', check_obj.sep_edge_count,'multiply_connected_geometry',
          check_obj.multiply_connected_geometry, 'double vertices', len(obj.double_vertices), 'err_face', obj.err_face)
    point2 = accrue_points.Obj_points('obj', 3, 10, check_obj.sep_face_count, len(obj.all_edges))
    point3 = accrue_points.Obj_points('obj', 2, 10, check_obj.sep_edge_count, len(obj.all_edges))
    point4 = accrue_points.Obj_points('obj', 3, 10, check_obj.multiply_connected_geometry, len(obj.all_edges))
    point5 = accrue_points.Obj_points('obj', 1, 10, len(obj.double_vertices), len(obj.verts_coords))
    point6 = accrue_points.Obj_points('obj', 1, 10, obj.err_face, len(obj.polygons))

    #check_uv
    check_uv = check_uv.Check_UV(obj.polygons)
    print('percent_busy', check_uv.percent_busy)
    point7 = accrue_points.Obj_points('uv', 1, 10, check_uv.percent_busy , 80)

    #check_normals
    #check_normals = check_normals.Check_normals(obj.polygons)
    #check_normals = check_normals.Check_normals(obj)
    #print('err_normal_face', check_normals.err_normals_count)
