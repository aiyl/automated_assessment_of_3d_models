import traceback

#path1 - эталон path2 - решение участника
class Material_properties:
    def __init__(self, material_name, diffuse_color):
        self.material_name = material_name
        self.diffuse_color = diffuse_color


class Mtl:
    materials = []
    material_name = ''
    logs = ''
    def __init__(self, path):
        self.file = path
        self.parseMtl()
    def parseMtl(self):
        materials = []
        file = self.file
        mtl = file.split('.')[0] + '.mtl'
        try:
            file = open(mtl, 'r')
            for line in file:
                words = line.split()
                if len(words) == 0 or words[0].startswith('#'):
                    pass
                elif words[0] == 'newmtl':
                    self.material_name = words[1]
                elif words[0] == 'Kd':
                    list = []
                    list.append(words[1])
                    list.append(words[2])
                    list.append(words[3])
                    material = Material_properties(self.material_name, list)
                    materials.append(material)
                    self.materials = materials
            #self.materials.clear()
            file.close()

        except Exception as e:
            self.logs = 'File mtl and file obj must match! file must be named:' + str(mtl)
            print('File mtl and file obj must match! file must be named:\n'+ mtl, traceback.format_exc())
