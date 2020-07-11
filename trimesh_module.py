import numpy as np
import check_renders
import trimesh

class Trimesh:
    render_points = 0
    voxel_points = 0
    def __init__(self, reference_path, solve_path):
        self.reference_path = reference_path
        self.solve_path = solve_path
        transformations = []
        for i in range(10):
            transformations.append(trimesh.transformations.random_rotation_matrix())

        solve_renders = self.get_renders(solve_path, 'solve', transformations)

        reference_renders = self.get_renders(reference_path, 'reference', transformations)

        renders = check_renders.Check_renders(reference_renders, solve_renders)
        self.render_points = renders.all_points
        i = 0
        while i <1:
            self.voxel_compare(solve_path)
            i += 1


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
        rotate = trimesh.transformations.rotation_matrix(
            angle=25,
            direction=[0, 0, 5],
            point=scene.centroid)
        for i in range(10):
            scene.apply_transform(transformations[i])
            #trimesh.constants.log.info('Saving image %d', i)
            #camera_old, _geometry = scene.graph[scene.camera.name]
            #camera_new = np.dot(camera_old, rotate)
            #scene.graph[scene.camera.name] = camera_new
            try:
                file_name = 'renders/render_' + obj_type + str(i) + '.png'
                renders.append(file_name)
                png = scene.save_image(resolution=[500, 500], visible=True)
                with open(file_name, 'wb') as f:
                    f.write(png)
                    f.close()

            except BaseException as E:
                print("unable to save image", str(E))
        return renders

    def voxelized_obj(self, obj):
        try:
            v = obj.voxelized(pitch=0.25)
        except:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
            scene = trimesh.Scene(meshes_list)
            v = mesh.voxelized(pitch=0.25)
        return v
    def voxel_compare(self,solve):
        obj = trimesh.load(solve, process=False)
        obj2 = trimesh.load(self.reference_path, process=False)
        v1 = self.voxelized_obj(obj)
        v2 = self.voxelized_obj(obj2)
        same_voxels = 0
        if v1.points.size >= v2.points.size:
            compare_array = np.in1d(v2.points, v1.points)
            for i in range(len(compare_array)):
                if compare_array[i] == True:
                    same_voxels += 1
            self.voxel_points = (same_voxels * 100) / v1.points.size
        else:
            compare_array = np.in1d(v1.points, v2.points)
            for i in range(len(compare_array)):
                if compare_array[i] == True:
                    same_voxels += 1
            self.voxel_points = (same_voxels * 100) / v2.points.size


