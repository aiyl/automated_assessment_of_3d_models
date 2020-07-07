import trimesh_module
import numpy as np
import check_renders
import trimesh
class Trimesh:
    render_points = 0
    voxel_points = []
    def __init__(self, reference_path, solve_path):
        self.reference_path = reference_path
        self.solve_path = solve_path
        solve_renders = self.get_renders(solve_path, 'solve')

        reference_renders = self.get_renders(reference_path, 'reference')

        #renders = check_renders.Check_renders(reference_renders, solve_renders)
        #self.render_points = renders.all_points
        i = 0
        print(len(solve_path))
        while i <1:
            self.voxel_compare(solve_path[i] )
            i += 1


    def get_renders(self, file_path, obj_type):
        renders = []
        obj = trimesh.load(file_path, process = False)
        try:
            meshes_list = obj.dump()
            scene = trimesh.Scene(meshes_list)
        except:
            mesh = obj
            scene = mesh.scene()
        scene.centroid
        #scene.apply_transform(trimesh.transformations.random_rotation_matrix())
        rotate = trimesh.transformations.rotation_matrix(
            angle=25,
            direction=[0, 0, 5],
            point=scene.centroid)
        for i in range(4):
            trimesh.constants.log.info('Saving image %d', i)
            camera_old, _geometry = scene.graph[scene.camera.name]
            camera_new = np.dot(camera_old, rotate)
            scene.graph[scene.camera.name] = camera_new
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

    def voxel_compare(self,solve):

        obj = trimesh.load(solve, process=False)
        obj2 = trimesh.load(self.reference_path, process=False)
        obj2.show()
        try:
            v1 = obj.voxelized(pitch=0.25)
        except:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
            scene = trimesh.Scene(meshes_list)
            v1 = mesh.voxelized(pitch=0.25)

        try:
            v2 = obj2.voxelized(pitch=0.25)
        except:
            meshes_list = obj2.dump()
            mesh = meshes_list.sum()
            v2 = mesh.voxelized(pitch=0.25)

        #    result = list(set(v1) & set(v2))
        c = 0
        nope = 0
        print('v1 volume', v1.volume)
        print('v2 volume', v2.volume)
        scale = round(v2.volume/v1.volume, 3)
        scale_list = [scale, scale, scale]
        #print(v1.apply_transform(trimesh.transformations.scale_and_translate(scale=scale_list)))

        print('v1 volume after scale', v1.volume)
        if v1.points.size >= v2.points.size:
            c = np.in1d(v2.points, v1.points)
            for i in range(len(c)):
                if c[i] == True:
                    nope += 1
            percent = (nope * 100) / v1.points.size
        else:
            c = np.in1d(v1.points, v2.points)
            for i in range(len(c)):
                if c[i] == True:
                    nope += 1
            percent = (nope * 100) / v2.points.size

        print(solve, percent)
        self.voxel_points.append(percent)

