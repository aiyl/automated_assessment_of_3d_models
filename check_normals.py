from functools import reduce

import math

class Check_normals2:
    err_normals_count = 0
    def __init__(self, polygons):
        self.polygons = polygons
        for i in range(len(polygons)):
            self.check(polygons[i])

    def scalar_multiplication(self, vector1, vector2):
        result = 0
        for i in range(len(vector1)):
            result += vector1[i]*vector2[i]
        return result

    def points_different(self, p1, p2):
        vector = []
        for i in range(len(p1)):
            vector.append(p2[i] - p1[i])
        return vector


    def check(self, polygon):
        p1 = polygon.points.verts_coords[0]
        p2 = polygon.points.verts_coords[1]
        p3 = polygon.points.verts_coords[2]
        v1 = self.points_different(p2, p1)
        v2 = self.points_different(p3, p1)
        vec_mult = self.scalar_multiplication(v1, v2)
        print(vec_mult)

class Check_normals:
    err_normals_count = 0
    def __init__(self, polygons):
        self.polygons = polygons
        self.main(polygons)

    def points_different(self, p1, p2):
        vector = []
        for i in range(len(p1)):
            vector.append(p2[i] - p1[i])
        return vector

    def vector_multiplication(self, v1, v2):
        scalar = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
        if scalar<0:
            return False
        else:
            return True

    def sum_vectors(self, v, w):
        return [vi - wi for vi, wi in zip(v, w)]

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
        a2 = self.middle_point(polygon.points.verts_coords)
        b = polygon.points.verts_coords[0]
        sum_normals = self.sum_of_all_vectors(polygon.normals.verts_coords)
        delitel = math.sqrt(float(sum_normals[0] * sum_normals[0] + sum_normals[1] * sum_normals[1] + sum_normals[2] * sum_normals[2]))
        for i in range(len(sum_normals)):
            sum_normals[i] = (sum_normals[i]/delitel) - delitel
        a = sum_normals

        #check is it point inside mesh
        vec = self.points_different(a, b)
        for i in range(len(polygon.normals.verts_coords)):
            if not self.vector_multiplication(polygon.normals.verts_coords[i], vec):
                return False
        return True
    def main(self, polygons):
        for i in range(len(polygons)):
            if not self.check_normals(polygons[i]):
                self.err_normals_count+=1