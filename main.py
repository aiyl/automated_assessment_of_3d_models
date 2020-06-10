import os
import parse_mtl
import check_materials

dir = os.path.abspath(os.curdir)
reference = dir + '/Tests/unnormal_box2.obj'
solve = dir + '/Tests/isbaForBlend.obj'

if __name__ == '__main__':
    mtl1 = parse_mtl.Mtl(reference)
    mtl1.parseMtl()
    mtl2 = parse_mtl.Mtl(solve)
    mtl2.parseMtl()
    checker = check_materials.Checker(mtl1, mtl2)
    print(checker.check_names())
"""    for i in range(len(mtl1.materials)):
        print('mat1', mtl1.materials[i].material_name, mtl1.materials[i].diffuse_color )
    for i in range(len(mtl2.materials)):
        print('mat2', mtl2.materials[i].material_name, mtl2.materials[i].diffuse_color) """
