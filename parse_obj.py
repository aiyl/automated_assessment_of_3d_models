import numpy as np
class Points:
    def __init__(self, point_number, verts_coords):
        self.point_number = point_number
        self.verts_coords = verts_coords


class Polygon:
    def __init__(self, pol_edges, points, normals, uv_verts, uv_edges, number):
        self.pol_edges = pol_edges
        self.points = points
        self.normals = normals
        self.uv_verts = uv_verts
        self.uv_edges = uv_edges
        self.number = number


class Obj:
    polygons = []
    err_face = 0
    verts_coords = []
    all_edges = []
    double_vertices = []
    logs = True
    normal_logs = ''
    texture_logs = ''

    def __init__(self, file):
        self.file = file
        self.parse()

    def check_repeat(self, list1, list2):
        list = [list1[1], list1[0]]
        if (list1 in list2) or (list in list2):
            return False
        return True

    def get_all_edges(self):
        all_edges = []
        for n in range(len(self.polygons)):
            for m in range(len(self.polygons[n].pol_edges)):
                # verts_numbers = []
                if len(all_edges) == 0:
                    all_edges.append(self.polygons[n].pol_edges[m])
                elif self.check_repeat(self.polygons[n].pol_edges[m], all_edges):
                    all_edges.append(self.polygons[n].pol_edges[m])
        return all_edges

    def get_edge(self, faces_verts):
        edges = []
        for m in range(len(faces_verts)):
            if m == len(faces_verts) - 1:
                edge = [faces_verts[m], faces_verts[0]]
            else:
                edge = [faces_verts[m], faces_verts[m + 1]]
            edges.append(edge)
        return edges

    def create_coords_list(self, words, vert_coords_len):
        if vert_coords_len == 3:
            x, y, z = float(words[1]), float(words[2]), float(words[3])
            coords = [x, y, z]
            return coords
        else:
            x, y = float(words[1]), float(words[2])
            coords = [x, y]
            return coords

    def parse(self):
        normals_coords = []
        uv_coords = []
        number = 0
        try:
            file = open(self.file, 'r')
            for line in file:
                words = line.split()
                if len(words) == 0 or words[0].startswith('#') or words[0].startswith('o') or words[0].startswith('newmtl'):
                    pass
                elif words[0] == 'v':
                    list = self.create_coords_list(words, 3)
                    for i in range(len(self.verts_coords)):
                        if [round(list[0], 3), round(list[1], 3), round(list[2], 3)] \
                                == [round(self.verts_coords[i][0], 3), round(self.verts_coords[i][1], 3),
                                    round(self.verts_coords[i][2], 3)]:
                            self.double_vertices.append(list)
                    self.verts_coords.append(list)
                elif words[0] == 'vt':
                    list = self.create_coords_list(words, 2)
                    uv_coords.append(list)
                elif words[0] == 'vn':
                    list = self.create_coords_list(words, 3)
                    normals_coords.append(list)
                elif words[0] == 'f':
                    number += 1
                    faceVertList = []
                    normal_list = []
                    uv_list = []
                    for faceIdx in words[1:]:
                        faceVertList.append(faceIdx)
                    if len(faceVertList) != 4 and len(faceVertList) != 3:
                        self.err_face += 1
                    faces_verts = []  # индексы вершин грани(ей)
                    vertices = []
                    normals = []
                    uvs = []
                    for i in range(len(faceVertList)):
                        faces_verts.append(faceVertList[i].split('/')[0])
                        uv_list.append(faceVertList[i].split('/')[1])
                        normal_list.append(faceVertList[i].split('/')[2])
                        vertices.append(self.verts_coords[int(faces_verts[i]) - 1])
                        try:
                            uvs.append(uv_coords[int(uv_list[i]) - 1])
                        except:
                            self.texture_logs = 'not all texture coordinates found'
                        try:
                            normals.append(normals_coords[int(normal_list[i]) - 1])
                        except:
                            self.normal_logs = 'not all normal coordinates found'
                    points = Points(faces_verts, vertices)
                    uv = Points(uv_list, uvs)
                    normal = Points(normal_list, normals)
                    polygon = Polygon(self.get_edge(faces_verts), points, normal, uv, self.get_edge(uv_list), number)
                    self.polygons.append(polygon)
            file.close()
            self.all_edges = self.get_all_edges()
        except:
            self.logs = False
