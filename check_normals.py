from functools import reduce
import numpy as np
import math
import trimesh



class Check_normals:
    logs = ''
    err_normals_count = 0
    err_normals = True
    def __init__(self, obj, path_obj):
        self.obj = obj
        self.path_obj = path_obj
        self.main(path_obj, obj)

    def points_different(self, p1, p2):
        vector = []
        for i in range(len(p1)):
            vector.append(p2[i] - p1[i])
        return vector

    def scalar_multiplication(self, v1, v2):
        scalar = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
        if scalar < 0:
            return False
        else:
            return True

    def sum_vectors(self, v, w):
        return [vi + wi for vi, wi in zip(v, w)]

    def sum_of_all_vectors(self, vecs):
        return reduce(self.sum_vectors, vecs)

    def middle_point(self, vertices):
        x = 0
        y = 0
        z = 0
        for i in range(len(vertices)):
            x += vertices[i][0]
            y += vertices[i][1]
            z += vertices[i][2]
        return [x/len(vertices),y/len(vertices),z/len(vertices)]

    def check_normals(self, polygon, a):
        b = polygon.points.verts_coords[0]
        face_normal = self.sum_of_all_vectors(polygon.normals.verts_coords)
        len_face_normal = math.sqrt(float(face_normal[0] * face_normal[0] + face_normal[1] * face_normal[1] + face_normal[2] * face_normal[2]))
        for i in range(len(face_normal)):
            face_normal[i] = (face_normal[i]/len_face_normal)
        vec = self.points_different(a, b)
        if not self.scalar_multiplication(face_normal, vec):
            self.err_normals_count += 1

    def check_normals_2(self, mesh_trimesh):
        #print(l)
        startpoint = mesh_trimesh.center_mass
        directional_dist = startpoint - mesh_trimesh.triangles_center
        dots = np.einsum("ij,ij->i", directional_dist, mesh_trimesh.face_normals) / np.linalg.norm(directional_dist, axis=1)
        front_facing = dots < 0
        self.err_normals_count = len(front_facing) - np.sum(front_facing)
        print(self.err_normals_count)

    def check_normals_3(self):
        all_edges = []
        for i in range(len(self.obj.polygons)):
            for j in range(len(self.obj.polygons[i].pol_edges)):
                all_edges.append(self.obj.polygons[i].pol_edges[j])
        for k in range(len(all_edges)):
            for l in range(k+1, len(all_edges)):
                if all_edges[k] == all_edges[l]:
                    return False
        return True

    def main(self, obj_path, obj):
        obj_trimesh = trimesh.load(obj_path, process=False)
        try:
            meshes_list = obj_trimesh.dump()
            mesh = meshes_list.sum()
        except:
            mesh = obj_trimesh
        convex = False
        try:
            convex = trimesh.convex.is_convex(mesh)
        except Exception as e:
            self.logs += ' '
            print(e)
        if convex:
            a = self.middle_point(self.obj.verts_coords)
            for i in range(len(obj.polygons)):
                self.check_normals(obj.polygons[i], a)
        elif self.logs != '':
            if not self.check_normals_2(mesh):
                self.logs += '3d model has inverted normals. Counting in triangles: '
        elif not convex:
            self.logs = 'object is not a convex hull. Cannot count inverted normals'
            self.err_normals = self.check_normals_3()
