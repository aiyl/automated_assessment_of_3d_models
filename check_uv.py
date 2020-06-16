import numpy as np
class Check_UV:
    polygon_areas = 0
    uv_map_edge = 1
    uv_map_area = 1
    percent_busy = 0
    def __init__(self, polygons):
        self.polygons = polygons
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
            n = self.vector_multiplication(u, v) /2
            self.polygon_areas += n
        self.uv_map_area = self.uv_map_edge*self.uv_map_edge
    def check_uv(self):
        for i in range(len(self.polygons)):
            self.uv_areas(self.polygons[i])
        self.percent_busy = round(self.polygon_areas*100/self.uv_map_area)

