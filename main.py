import os
import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv

dir = os.path.abspath(os.curdir)
reference = dir + '/Tests/check1.obj'
solve = dir + '/Tests/check_uv.obj'

if __name__ == '__main__':
    #check material
    mtl1 = parse_mtl.Mtl(reference)
    mtl2 = parse_mtl.Mtl(solve)
    checker = check_materials.Checker(mtl1, mtl2)

    print('material points', checker.pointer())
    #check obj
    obj = parse_obj.Obj(solve)
    check_obj = check_obj.Check(obj)

    check_uv = check_uv.Check_UV(obj.polygons, obj.uv_coords, obj.all_uv_edge)
    print('percent_busy', check_uv.percent_busy, ' area', check_uv.polygon_areas)
    print('separate face', check_obj.sep_face_count, 'separate_edge', check_obj.sep_edge_count,'multiply_connected_geometry', check_obj.multiply_connected_geometry)

"""    for i in range(len(mtl1.materials)):
        print('mat1', mtl1.materials[i].material_name, mtl1.materials[i].diffuse_color )
    for i in range(len(mtl2.materials)):
        print('mat2', mtl2.materials[i].material_name, mtl2.materials[i].diffuse_color) """
