import traceback
class Points:
    def __init__(self, point_number, verts_coords):
        self.point_number = point_number
        self.verts_coords = verts_coords


class Polygon:
    def __init__(self, pol_edges, points, normals, number):
        self.pol_edges = pol_edges
        self.points = points
        self.normals = normals
        self.number = number

class Obj:
    polygons = []
    err_face = 0
    all_edges = []
    all_verts = []
    verts_coords = []
    normals_coords = []
    def __init__(self, file):
        self.file = file
        self.parse()

    def get_all_verts(self):
        for i in range(len(self.polygons)):
            self.all_verts.append(self.polygons[i].points.point_number)

    def check_repeat(self, list, list2):
        boolean = True
        for n in range(len(list2)):
            for m in range(len(list2[n]) - 1):
                if (list2[n][m] == list[0] and list2[n][m + 1] == list[1]) or (
                        list2[n][m] == list[1] and list2[n][m + 1] == list[0]):
                    boolean = False
        return boolean

    def get_all_edges(self, all_verts):
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
                if self.check_repeat(list3, self.all_edges) or len(self.all_edges) == 0:
                    self.all_edges.append(list3)

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

    def parse(self):
        number = 0
        try:
            file = open(self.file, 'r')
            for line in file:
                words = line.split()
                if len(words) == 0 or words[0].startswith('#'):
                    pass
                elif words[0] == 'v':
                    x, y, z = float(words[1]), float(words[2]), float(words[3])
                    list = []
                    list.append(x)
                    list.append(y)
                    list.append(z)
                    self.verts_coords.append(list)
                elif words[0] == 'vn':
                    x, y, z = float(words[1]), float(words[2]), float(words[3])
                    list2 = []
                    list2.append(x)
                    list2.append(y)
                    list2.append(z)
                    self.normals_coords.append(list2)
                elif words[0] == 'f':
                    number += 1
                    faceVertList = []
                    normal_list = []
                    for faceIdx in words[1:]:
                        faceVertList.append(faceIdx)
                    if not (len(faceVertList) == 4 or len(faceVertList) == 3):
                        self.err_face += 1
                    faces_verts = []  # индексы вершин грани(ей)
                    vertices = []
                    normals = []
                    for i in range(len(faceVertList)):
                        faces_verts.append(faceVertList[i].split('/')[0])
                        normal_list.append(faceVertList[i].split('/')[2])
                        vertices.append(self.verts_coords[int(faces_verts[i]) - 1])
                        normals.append(self.normals_coords[int(normal_list[i]) - 1])
                    points = Points(faces_verts, vertices)
                    normal = Points(normal_list, normals)
                    polygon = Polygon(self.get_edge(faces_verts), points, normal, number)
                    self.polygons.append(polygon)
            file.close()
            self.get_all_verts()
            self.get_all_edges(self.all_verts)
        except Exception as e:
            print('Error format! File has to be obj:\n', traceback.format_exc())
