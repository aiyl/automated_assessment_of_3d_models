import numpy as np
import math
class Check_UV:
    polygon_areas = 0
    uv_map_edge = 1
    uv_map_area = 1
    percent_busy = 0
    uv_intersection = 0
    def __init__(self, polygons, uv_coords, all_uv_edges):
        self.polygons = polygons
        self.uv_coords = uv_coords
        self.uv_edges = all_uv_edges
        self.check_uv()

    def points_different(self, p1, p2):
        vector = []
        for i in range(len(p1)):
            vector.append(p2[i] - p1[i])
        return vector

    def vector_multiplication(self, v1, v2):
        vector = v1[0] * v2[1] - v1[1] * v2[0]
        return vector

    def uv_areas(self, polygon):
        max_edge = 1
        for i in range(len(polygon.uv_verts.verts_coords) - 2):
            p0 = np.array([polygon.uv_verts.verts_coords[i][0], polygon.uv_verts.verts_coords[i][1]])
            p1 = np.array([polygon.uv_verts.verts_coords[i+1][0], polygon.uv_verts.verts_coords[i+1][1]])
            p2 = np.array([polygon.uv_verts.verts_coords[i+2][0], polygon.uv_verts.verts_coords[i+2][1]])
            max_edge = max(p0.max(), p1.max(), p2.max())
            if self.uv_map_edge < max_edge:
                self.uv_map_edge = int(str(max_edge).split('.')[0]) + 1
            u = self.points_different(p1, p0)
            v = self.points_different(p2, p0)
            n = abs(self.vector_multiplication(u, v) /2)
            self.polygon_areas += n
        self.uv_map_area = self.uv_map_edge*self.uv_map_edge

    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between(self, v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def distance(self,x1,y1,x2,y2):
        return math.hypot(x2-x1, y2-y1)


    def check_cross(self):
        integrity = []

        for i in range(len(self.uv_edges)):
            k = 0
            x1_1 = self.uv_coords[int(self.uv_edges[i][0]) - 1][0]
            y1_1 = self.uv_coords[int(self.uv_edges[i][0]) - 1][1]
            A = [x1_1, y1_1]
            x1_2 = self.uv_coords[int(self.uv_edges[i][1]) - 1][0]
            y1_2 = self.uv_coords[int(self.uv_edges[i][1]) - 1][1]
            B = [x1_2, y1_2]
            while k < len(self.uv_edges)-1:
                if k == i:
                    k += 1
                    pass
                x2_1 = self.uv_coords[int(self.uv_edges[k][0]) - 1][0]
                y2_1 = self.uv_coords[int(self.uv_edges[k][0]) - 1][1]
                x2_2 = self.uv_coords[int(self.uv_edges[k][1]) - 1][0]
                y2_2 = self.uv_coords[int(self.uv_edges[k][1]) - 1][1]
                C = [x2_1, y2_1]
                D = [x2_2, y2_2]
                AB = self.points_different(A,B)
                AC = self.points_different(A,C)
                angleA = self.angle_between(AB, AC)
                CD = self.points_different(C,D)
                angle = self.angle_between(AB, CD)
                print(angle)
                AD = self.points_different(A, D)
                angleB = self.angle_between(AB, AD)
                distanceAB = self.distance(A[0], A[1], B[0], B[1])
                distanceAC = self.distance(A[0], A[1], C[0], C[1])
                distanceAD = self.distance(A[0], A[1], D[0], D[1])
                z1 = round(distanceAB*distanceAC*math.sin(angleA), 6)
                z2 = round(distanceAB*distanceAD*math.sin(angleB), 6)
                divider = abs(z2-z1)
                if divider!=0 and not math.isnan(divider) and z1*z2>0 and round(angle,4) != 1.5708:
                    Px = C[0]+(D[0]-C[0])*abs(z1)/divider
                    Py = C[1] + (D[1] - C[1]) * abs(z1) /divider
                    list = [round(Px, 6), round(Py, 6)]
                    if not list in self.uv_coords and not list in integrity:
                        integrity.append(list)

                k+=1
        print('integrity', len(integrity))
        """
                A1 = y1_1 - y1_2
                B1 = x1_2 - x1_1
                C1 = x1_1 * y1_2 - x1_2 * y1_1
                A2 = y2_1 - y2_2
                B2 = x2_2 - x2_1
                C2 = x2_1 * y2_2 - x2_2 * y2_1
                if B1 * A2 - B2 * A1 != 0 and A1!=0:
                    y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
                    x = (-C1 - B1 * y) / A1
                    if min(x1_1, x1_2) <= x <= max(x1_1, x1_2) and \
                            min(y1_1, y1_2) <= y <= max(y1_1, y1_2):
                        list = [round(x, 6), round(y, 6)]
                        if not list in self.uv_coords and not list in integrity :
                            integrity.append(list)
                            #print('Точка пересечения отрезков есть, координаты: ({0:f}, {1:f}).'.
                            #      format(x, y), '1 otrez', x1_1, y1_1, x1_2, y1_2, '2otrez', x2_1, y2_1, x2_2, y2_2 )
                            self.uv_intersection += 1
                k += 1
"""

    def check_uv(self):
        self.check_cross()
       # if self.uv_intersection == 0:
        #    for i in range(len(self.polygons)):
         #       self.uv_areas(self.polygons[i])
          #  self.percent_busy = int(round(self.polygon_areas * 100 / self.uv_map_area))

