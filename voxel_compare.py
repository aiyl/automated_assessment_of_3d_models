import trimesh
import numpy as np
class Voxels:
    voxel_points = 0
    logs = ''
    def __init__(self, reference_path, solve_path):
        self.reference_path = reference_path
        self.solve_path = solve_path
        self.voxel_compare()


    def voxelized_obj(self, obj, pitch):

        try:
            v = obj.voxelized(pitch=pitch)
        except:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
            scene = trimesh.Scene(meshes_list)
            v = mesh.voxelized(pitch=pitch)
        return v


    def load_obj(self, obj_path):
        obj = trimesh.load(obj_path, process=False)
        try:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
        except:
            mesh = obj
        return mesh


    def voxel_compare(self):
        obj = self.load_obj(self.reference_path)
        obj2 = self.load_obj(self.solve_path)
        vol1 = round(int(obj.bounding_box_oriented.volume)/1000, 1)
        vol2 = round(int(obj2.bounding_box_oriented.volume)/1000, 1)
        if  vol1 != vol2:
            self.logs = 'Objects have a large difference in volume. Maybe you should see the size of the object'
        else:
            vol = str(int(obj2.bounding_box_oriented.volume))
            if len(vol) <= 2:
                pitch = 0.05
            else:
                pitch = 0.05 * (len(vol)-1)
            v1 = self.voxelized_obj(obj, pitch)
            v2 = self.voxelized_obj(obj2, pitch)
            #v2.show()
            #v1.show()
            if v1.points.size >= v2.points.size:
                compare_array = np.in1d(v2.points, v1.points)
                same_voxels = np.count_nonzero(compare_array)
                self.voxel_points = (same_voxels * 100) / v1.points.size
            else:
                compare_array = np.in1d(v1.points, v2.points)
                same_voxels = np.count_nonzero(compare_array)
                self.voxel_points = (same_voxels * 100) / v2.points.size
