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
    def __init__(self, polygons):
        self.polygons = polygons
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

        max_edge = max(x.max(), y.max())

        if self.uv_map_edge < max_edge:
            self.uv_map_edge = int(str(max_edge).split('.')[0]) + 1
        self.uv_map_area = self.uv_map_edge * self.uv_map_edge

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

    def check_uv(self):
        if self.check_polygon_cross():
            for i in range(len(self.polygons)):
                self.uv_areas(self.polygons[i])
            self.percent_busy = int(round(self.polygon_areas * 100 / self.uv_map_area))


