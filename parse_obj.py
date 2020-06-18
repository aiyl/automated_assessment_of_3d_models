import traceback
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
    all_uv_edge = []
    all_edges = []
    all_verts = []
    all_uv_verts = []
    verts_coords = []
    normals_coords = []
    uv_coords = []
    def __init__(self, file):
        self.file = file
        self.parse()

    def get_all_verts(self, args):
        all_verts = []
        for i in range(len(self.polygons)):
            if args == 'pol':
                all_verts.append(self.polygons[i].points.point_number)
            else:
                all_verts.append(self.polygons[i].uv_verts.point_number)
        return all_verts

    def check_repeat(self, list, list2):
        boolean = True
        for n in range(len(list2)):
            for m in range(len(list2[n]) - 1):
                if (list2[n][m] == list[0] and list2[n][m + 1] == list[1]) or (
                        list2[n][m] == list[1] and list2[n][m + 1] == list[0]):
                    boolean = False
        return boolean

    def get_all_edges(self, all_verts):
        all_edges = []
        for n in range(len(all_verts)):
            for m in range(len(all_verts[n])):
                list3 = []
                if m == len(all_verts[n]) - 1:
                    list3.append(all_verts[n][m])
                    list3.append(all_verts[n][0])
                else:
                    list3.append(all_verts[n][m])
                    list3.append(all_verts[n][m + 1])
                    # edge = Edge(faces_verts[n][m], faces_verts[n][m+1])
                if self.check_repeat(list3, all_edges) or len(all_edges) == 0:
                    all_edges.append(list3)
        return all_edges

    def get_edge(self, faces_verts):
        edges = []
        for m in range(len(faces_verts)):
            list3 = []
            if m == len(faces_verts) - 1:
                list3.append(faces_verts[m])
                list3.append(faces_verts[0])
            else:
                list3.append(faces_verts[m])
                list3.append(faces_verts[m + 1])
            edges.append(list3)

        return edges

    def create_coords_list(self, words, vert_coords_len):
        list = []
        if vert_coords_len == 3:
            x, y, z = float(words[1]), float(words[2]), float(words[3])
            list.append(x)
            list.append(y)
            list.append(z)
            return list
        else:
            x,y = float(words[1]), float(words[2])
            list.append(x)
            list.append(y)
            return list

    def parse(self):
        number = 0
        try:
            file = open(self.file, 'r')
            for line in file:
                words = line.split()
                if len(words) == 0 or words[0].startswith('#'):
                    pass
                elif words[0] == 'v':
                    list = self.create_coords_list(words, 3)
                    self.verts_coords.append(list)
                elif words[0] == 'vt':
                    list = self.create_coords_list(words, 2)
                    self.uv_coords.append(list)
                elif words[0] == 'vn':
                    list = self.create_coords_list(words, 3)
                    self.normals_coords.append(list)
                elif words[0] == 'f':
                    number += 1
                    faceVertList = []
                    normal_list = []
                    uv_list = []
                    for faceIdx in words[1:]:
                        faceVertList.append(faceIdx)
                    if not (len(faceVertList) == 4 or len(faceVertList) == 3):
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
                        uvs.append(self.uv_coords[int(uv_list[i]) - 1])
                        normals.append(self.normals_coords[int(normal_list[i]) - 1])
                    points = Points(faces_verts, vertices)
                    uv = Points(uv_list, uvs)
                    normal = Points(normal_list, normals)
                    polygon = Polygon(self.get_edge(faces_verts), points, normal, uv, self.get_edge(uv_list), number)
                    self.polygons.append(polygon)
            file.close()
            self.all_verts = self.get_all_verts('pol')
            self.all_uv_verts = self.get_all_verts('uv')
            self.all_edges = self.get_all_edges(self.all_verts)
            self.all_uv_edge = self.get_all_edges(self.all_uv_verts)
        except Exception as e:
            print('Error format! File has to be obj:\n', traceback.format_exc())
