import skimage
from skimage import io, color
class Checker:
    points = 0
    need_material = ''
    def __init__(self, reference, solve):
        self.reference = reference
        self.solve = solve

    def check_names(self):
        need_names = []
        solve_materials = self.solve.materials
        reference_materials = self.reference.materials
        for i in range(len(reference_materials)):
            k = 0
            while k<len(solve_materials):
                if reference_materials[i].material_name == solve_materials[k].material_name:
                    self.points += Checker.check_diffuse_color(self, reference_materials[i], solve_materials[i])
                    break
                k += 1
            if k == len(solve_materials):
                need_names.append(reference_materials[i].material_name)
        return need_names

    def check_diffuse_color(self, reference_materials, solve_materials):
        diffuse_color1= []
        diffuse_color2 = []

        for i in range(len(reference_materials.diffuse_color)):
            reference_materials.diffuse_color[i] = float(reference_materials.diffuse_color[i])
            diffuse_color1.append(reference_materials.diffuse_color[i])
        for i in range(len(solve_materials.diffuse_color)):
            solve_materials.diffuse_color[i] = float(solve_materials.diffuse_color[i])
            diffuse_color2.append(solve_materials.diffuse_color[i])
        lab1 = color.rgb2lab([[diffuse_color1]],  illuminant='D65', observer='2')
        lab2 = color.rgb2lab([[diffuse_color2]], illuminant='D65', observer='2')
        deltaE2 = skimage.color.deltaE_ciede2000(lab1, lab2, 1, 1, 1)
        points = int((101-int(deltaE2))/10) #max point 10
        return points

    def pointer(self):
        check_names = self.check_names()
        if len(check_names) != 0:
            self.need_material =  check_names
        maxPoint = len(self.reference.materials)*10
        if maxPoint != 0:
            points = (self.points*10)/maxPoint
            return int(points)
        else:
            return 0
