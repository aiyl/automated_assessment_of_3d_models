# parse the file
import os

dir = os.path.abspath(os.curdir)
# obj_filename = dir + '\Tests\check_mtl_blend.obj'
obj_filename = dir + '\e_vertex_quan_error.obj'
file = open(obj_filename, 'r')
verts = []
i = 0
for line in file:
    words = line.split()
    if len(words) == 0 or words[0].startswith('#'):
        pass
    elif words[0] == 'v':
        x, y, z = float(words[1]), float(words[2]), float(words[3])
        list = []
        list.append(x)
        list.append(y)
        list.append(z)
        verts.append(list)

    elif words[0] == 'f':
        faceVertList = []
        for faceIdx in words[1:]:
            faceVertList.append(faceIdx)
        if len(faceVertList) == 4 or len(faceVertList) == 3:
            print('ok')
        else:
            print('not')
        print(faceVertList)

print(verts)
