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

    def onSegment(self, p, q, r):
        if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    def orientation(self, p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Colinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if (val > 0):

            # Clockwise orientation
            return 1
        elif (val < 0):

            # Counterclockwise orientation
            return 2
        else:

            # Colinear orientation
            return 0

    def doIntersect(self, p1, q1, p2, q2):

        # Find the 4 orientations required for
        # the general and special cases
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        if ((o1 != o2) and (o3 != o4)):
            return True

        return False

    def check_cross(self):
        integrity = []

        for i in range(len(self.uv_edges)):
            k = 0
            x1_1 = self.uv_coords[int(self.uv_edges[i][0]) - 1][0]
            y1_1 = self.uv_coords[int(self.uv_edges[i][0]) - 1][1]
            p1 = [x1_1, y1_1]
            x1_2 = self.uv_coords[int(self.uv_edges[i][1]) - 1][0]
            y1_2 = self.uv_coords[int(self.uv_edges[i][1]) - 1][1]
            q1 = [x1_2, y1_2]
            while k < len(self.uv_edges)-1:
                if k == i:
                    k += 1
                    pass
                x2_1 = self.uv_coords[int(self.uv_edges[k][0]) - 1][0]
                y2_1 = self.uv_coords[int(self.uv_edges[k][0]) - 1][1]
                x2_2 = self.uv_coords[int(self.uv_edges[k][1]) - 1][0]
                y2_2 = self.uv_coords[int(self.uv_edges[k][1]) - 1][1]
                p2 = [x2_1, y2_1]
                q2 = [x2_2, y2_2]
                if self.doIntersect(p1,q1,p2,q2):
                    A1 = y1_1 - y1_2
                    B1 = x1_2 - x1_1
                    C1 = x1_1 * y1_2 - x1_2 * y1_1
                    A2 = y2_1 - y2_2
                    B2 = x2_2 - x2_1
                    C2 = x2_1 * y2_2 - x2_2 * y2_1
                    if B1 * A2 - B2 * A1 != 0 and A1 != 0:
                        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
                        x = (-C1 - B1 * y) / A1
                        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2) and \
                                min(y1_1, y1_2) <= y <= max(y1_1, y1_2):
                            list = [round(x, 6), round(y, 6)]
                            if not list in self.uv_coords and not list in integrity:
                                integrity.append(list)
                                print('Точка пересечения отрезков есть, координаты: ({0:f}, {1:f}).'.
                                     format(x, y), '1 otrez', x1_1, y1_1, x1_2, y1_2, '2otrez', x2_1, y2_1, x2_2, y2_2 )
                                self.uv_intersection += 1
                k+=1


    def check_uv(self):
        self.check_cross()
       # if self.uv_intersection == 0:
        #    for i in range(len(self.polygons)):
         #       self.uv_areas(self.polygons[i])
          #  self.percent_busy = int(round(self.polygon_areas * 100 / self.uv_map_area))

