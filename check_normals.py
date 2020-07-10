from functools import reduce

import math

class Check_normals:
    err_normals_count = 0

    def __init__(self, obj):
        self.obj = obj
        self.main(obj)

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

        a = self.middle_point(self.obj.verts_coords)
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

    def check_normals2(self, polygon):
        xyz = self.middle_point(polygon.points.verts_coords)
        a = polygon.normals.verts_coords[0]
        b = polygon.normals.verts_coords[1]
        c = polygon.normals.verts_coords[2]
        normal = self.sum_of_all_vectors([a,b,c])

        d = -1*(normal[0]*xyz[0]+normal[1]*xyz[1]+normal[2]*xyz[0])
        if normal[0]*xyz[0]+normal[1]*xyz[1]+normal[2]*xyz[2] + d>=0:
            return True
        else:
            return False

    def vector_len(self, vector):
        len = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
        return len
    def check_normals3(self, polygon):

        v0 = polygon.points.verts_coords[0]
        v1 = polygon.points.verts_coords[1]
        v2 = polygon.points.verts_coords[2]
        middle_point = self.middle_point([v0, v1, v2])
        vec_len = self.vector_len(middle_point)
        ray1 = []
        ray1.append([middle_point[0], middle_point[1], middle_point[2] + vec_len])
        ray1.append([middle_point[0], middle_point[1], middle_point[2] - vec_len]) #point inside?
        print(ray1)
        u = self.points_different(v0, v1)
        v = self.points_different(v0, v2)
        n = self.vector_multiplication(u, v)
        if n[0] == 0 and n[1] == 0 and n[2] == 0:
            print('triangle is degenerate')

    def check_normals4 (self):
        polygons = self.obj.polygons
        all_edges = []
        for i in range(len(polygons)):
            for k in range(len(polygons[i].pol_edges)):
                all_edges.append(polygons[i].pol_edges[k])
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
        self.check_normals4()
        '''for i in range(len(obj.polygons)):
            self.check_normals(obj.polygons[i])
        print(self.err_normals_count)'''
