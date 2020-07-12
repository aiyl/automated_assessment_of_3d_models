import trimesh
import numpy as np
class Voxels:
    voxel_points = 0
    def __init__(self, reference_path, solve_path):
        self.reference_path = reference_path
        self.solve_path = solve_path
        self.voxel_compare()


    def voxelized_obj(self, obj):

        try:
            v = obj.voxelized(pitch=0.125)
        except:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
            scene = trimesh.Scene(meshes_list)
            v = mesh.voxelized(pitch=0.125)
        return v

    def voxel_compare(self):
        obj = trimesh.load(self.solve_path, process=False)
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