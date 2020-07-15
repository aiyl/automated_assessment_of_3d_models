from functools import reduce
import numpy as np
import math
import trimesh



class Check_normals:
    logs = ''
    err_normals_count = 0

    def __init__(self, polygons, path_obj):
        self.polygons = polygons
        self.path_obj = path_obj
        self.main(path_obj, polygons)

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

    def vector_multiplication(self, v1, v2):
        vector = []
        vector.append(v1[1] * v2[2] - v1[2] * v2[1])
        vector.append(v1[2] * v2[0] - v1[0] * v2[2])
        vector.append(v1[0] * v2[1] - v1[1] * v2[0])
        return vector

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

    def check_normals(self, polygon):
        #a = self.middle_point(polygon.normals.verts_coords)
        a= [0,0,0]
        #print('middle point', a)
        b = polygon.points.verts_coords[0]
        face_normal = self.sum_of_all_vectors(polygon.normals.verts_coords)
        len_face_normal = math.sqrt(float(face_normal[0] * face_normal[0] + face_normal[1] * face_normal[1] + face_normal[2] * face_normal[2]))
        for i in range(len(face_normal)):
            face_normal[i] = (face_normal[i]/len_face_normal)

        #check is it point inside mesh
        vec = self.points_different(a, b)
        if not self.scalar_multiplication(face_normal, vec):
            self.err_normals_count += 1
        """for i in range(len(polygon.normals.verts_coords)):
            if not self.scalar_multiplication(polygon.normals.verts_coords[i], vec):
                return False
        return True """


    def vector_len(self, vector):
        len = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
        return len


    def check_normals_5(self, obj):
        #print(l)
        startpoint = obj.center_mass
        #startpoint = np.array([0, 0, 0])  # starting point of ray
        directional_dist = startpoint - obj.triangles_center
        dots = np.einsum("ij,ij->i", directional_dist, obj.face_normals) / np.linalg.norm(directional_dist, axis=1)
        front_facing = dots < 0
        self.err_normals_count = len(front_facing) - np.sum(front_facing)
        print(self.err_normals_count)


    def main(self, obj_path, polygons):
        obj = trimesh.load(obj_path, process=False)
        try:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
        except:
            mesh = obj

        #print(mesh.is_watertight)

        convex = False
        try:
            convex = trimesh.convex.is_convex(mesh)
        except Exception as e:
            self.logs += ' '
            print(e)
        if convex:
            for i in range(len(polygons)):
                self.check_normals(polygons[i])
            print(self.err_normals_count)
        elif self.logs != '':
            if not self.check_normals_5(mesh):
                self.logs += '3d model has inverted normals. Counting in triangles: ' + str(self.err_normals_count)
        else:
            pass
        print(self.logs)