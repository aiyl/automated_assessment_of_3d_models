import os
import parse_mtl
import check_materials
import parse_obj

dir = os.path.abspath(os.curdir)
reference = dir + '/Tests/check2.obj'
solve = dir + '/Tests/unnormal_box.obj'

if __name__ == '__main__':
    #check material
    mtl1 = parse_mtl.Mtl(reference)
    mtl1.parseMtl()
    mtl2 = parse_mtl.Mtl(solve)
    mtl2.parseMtl()
    checker = check_materials.Checker(mtl1, mtl2)
    print('points', checker.pointer(), 'max point', checker.maxPoint)

    #check obj
    obj = parse_obj.obj(solve)
    obj.parse()
    print('err face count', obj.err_face)
    

"""    for i in range(len(mtl1.materials)):
        print('mat1', mtl1.materials[i].material_name, mtl1.materials[i].diffuse_color )
    for i in range(len(mtl2.materials)):
        print('mat2', mtl2.materials[i].material_name, mtl2.materials[i].diffuse_color) """
