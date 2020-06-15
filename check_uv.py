class Check_UV:
    areas = 0
    normal_err = 0
    def __init__(self, polygons):
        self.polygons = polygons
        self.check_uv()

    def uv_area(self, polygon):
        listX = []
        listY = []
        sum1 = 0
        sum2 = 0
        for k in range(len(polygon.uv_verts.verts_coords)):
            if polygon.uv_verts.verts_coords[k][0]==0 or polygon.uv_verts.verts_coords[k][1] ==0:
                new_coords = [polygon.uv_verts.verts_coords[k][0] +1, polygon.uv_verts.verts_coords[k][1] +1 ]
                listX.append(new_coords[0])
                listY.append(1)


        for i in range(len(listX) -1):
            sum1 += listX[i] * listY[i+1]
        for i in range(len(listY) -1):
            sum2 += listY[i] * listX[i+1]
        area = 0.5 * abs(sum1 - sum2)
        print(area)
        return area

    def points_different(self,p1, p2):
        vector = []
        for i in range(len(p1)):
            vector.append(p2[i] - p1[i])
        return vector

    def vector_multiplication(self, v1, v2):
        vector = v1[0] * v2[1] - v1[1] * v2[0]
        return vector

    def check_normals(self, polygon):
        p0 = [polygon.uv_verts.verts_coords[0][0], polygon.uv_verts.verts_coords[0][1]]
        p1 = [polygon.uv_verts.verts_coords[1][0], polygon.uv_verts.verts_coords[1][1]]
        p2 = [polygon.uv_verts.verts_coords[2][0], polygon.uv_verts.verts_coords[2][1]]

        u = self.points_different(p1, p0)
        v = self.points_different(p2, p0)
        n = self.vector_multiplication(u,v)
        if n < 0:
            self.normal_err += 1

    def check_uv(self):
        for i in range(len(self.polygons)):
            self.areas += self.uv_area(self.polygons[i])
            self.check_normals(self.polygons[i])