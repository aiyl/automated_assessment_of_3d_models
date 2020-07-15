import os

import check_renders
import trimesh

class Renders:
    render_points = 0
    def __init__(self, reference_path, solve_path):
        self.reference_path = reference_path
        self.solve_path = solve_path
        transformations = []
        for i in range(10):
            transformations.append(trimesh.transformations.random_rotation_matrix())

        check_file = os.path.exists('renders')
        if not check_file:
            os.makedirs('renders', exist_ok=True)
        solve_renders = self.get_renders(solve_path, 'solve', transformations)

        reference_renders = self.get_renders(reference_path, 'reference', transformations)

        renders = check_renders.Check_renders(reference_renders, solve_renders)
        self.render_points = renders.all_points



    def get_renders(self, file_path, obj_type, transformations):
        renders = []

        obj = trimesh.load(file_path, process = False)
        try:
            meshes_list = obj.dump()
            scene = trimesh.Scene(meshes_list)
        except:
            mesh = obj
            scene = mesh.scene()
        scene.centroid
        #scene.show()
        for i in range(10):
            scene.apply_transform(transformations[i])
            try:
                file_name = 'renders/render_' + obj_type + str(i) + '.png' #fix it add mkdir
                renders.append(file_name)
                png = scene.save_image(resolution=[500, 500] , visible=True)
                with open(file_name, 'wb') as f:
                    f.write(png)
                    f.close()

            except BaseException as E:
                print("unable to save image", str(E))
        return renders



