class Checker:
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
                    break
                k += 1
            if k == len(solve_materials):
                need_names.append(reference_materials[i].material_name)

        return need_names
   # def check_diffuse_color(self):


