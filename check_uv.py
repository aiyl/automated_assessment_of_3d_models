import timeit

import numpy as np
import math
import shapely
from shapely.geometry import Polygon
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

    def polygon_area(self, x, y):
        correction = x[-1] * y[0] - y[-1] * x[0]
        main_area = np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])
        return 0.5 * np.abs(main_area + correction)

    def uv_areas(self, polygon):
        x = np.array([])
        y = np.array([])
        for i in range(len(polygon.uv_verts.verts_coords)):

            x = np.append(x, polygon.uv_verts.verts_coords[i][0])
            y = np.append(y, polygon.uv_verts.verts_coords[i][1])

        self.polygon_areas += self.polygon_area(x,y)
        return self.polygon_area(x,y)

    def check_polygon_cross(self):
        try:
            for i  in range(len(self.polygons)):
                pol1 = Polygon(self.polygons[i].uv_verts.verts_coords)
                for k in range(len(self.polygons)-1):
                    if k==i:
                        k += 1
                    pol2 = Polygon(self.polygons[k].uv_verts.verts_coords)
                    inter = pol1.intersection(pol2)
                    if inter.geom_type == 'Polygon' and inter.wkt != 'POLYGON EMPTY':
                        return False
        except:
            return False

        return True

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
        if self.check_polygon_cross():
            for i in range(len(self.polygons)):
                self.uv_areas(self.polygons[i])
            self.percent_busy = int(round(self.polygon_areas * 100 / self.uv_map_area))


