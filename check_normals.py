from functools import reduce
import numpy as np
import math
import trimesh



class Check_normals:
    err_normals_count = 0

    def __init__(self, polygons, path_obj):
        self.path_obj = path_obj
        self.polygons = polygons
        self.main(path_obj)

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

        #a = [0, 0, 0] #dot inside mesh

        a = self.middle_point(self.polygons.verts_coords)
        print('moddle point', a)
        b = polygon.points.verts_coords[0]
        face_normal = self.sum_of_all_vectors(polygon.normals.verts_coords)
        len_face_normal = math.sqrt(float(face_normal[0] * face_normal[0] + face_normal[1] * face_normal[1] + face_normal[2] * face_normal[2]))
        for i in range(len(face_normal)):
            face_normal[i] = (face_normal[i]/len_face_normal) - len_face_normal

        #check is it point inside mesh
        vec = self.points_different(a, b)
        if not self.scalar_multiplication(face_normal, vec):
            self.err_normals_count += 1
        for i in range(len(polygon.normals.verts_coords)):
            if not self.scalar_multiplication(polygon.normals.verts_coords[i], vec):
                return False
        return True


    def vector_len(self, vector):
        len = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
        return len


    def check_normals_5(self, obj_path):
        #error_edge = []
        obj = trimesh.load(obj_path, process=False)
        try:
            meshes_list = obj.dump()
            mesh = meshes_list.sum()
        except:
            mesh = obj
        mesh_edges = mesh.edges
        error_edge = mesh_edges[0]
        for i in range(len(mesh_edges)):
            copy  = mesh_edges[i +1 : len(mesh_edges)]
            check_in_copy = np.in1d(mesh_edges[i], copy)
            if  np.all(check_in_copy):
                error_edge = np.stack((error_edge, mesh_edges[i]), axis=0)
                #error_edge.append(mesh_edges[i])
                print(mesh_edges[i])

        triangles = mesh.edges[mesh.faces]
        #print(mesh.edges[mesh.faces])
        error_face_normals = 0
        for i in range(len(triangles)):
            for k in range(len(triangles[i])):
                compare_array = np.all(triangles[i][k],   error_edge)
                ame_voxels = np.count_nonzero(compare_array)
                #if triangles[i][k] in error_edge :
                #    error_face_normals += 1
        print(ame_voxels)
        print(error_face_normals)

        return error_edge


    def check_normals4 (self):
        polygons = self.polygons
        all_edges = []
        for i in range(len(polygons)):
            all_edges.append(sum(polygons[i].pol_edges, []))
        all_edges = sum(all_edges, [])
        for i in range(len(polygons)):
            list = []
            for k in range(len(polygons[i].pol_edges)):
                count = all_edges.count(polygons[i].pol_edges[k])
                if count >= 2:
                    list.append(False)
                else:
                    list.append(True)
            print(list)
            #if list.count(False) == len(polygons[i].pol_edges):
            if list.count(False) == len(polygons[i].pol_edges):
                self.err_normals_count += 1

    def main(self, obj):
        self.check_normals_5(obj)
        '''for i in range(len(obj.polygons)):
            self.check_normals(obj.polygons[i])
        print(self.err_normals_count)'''
