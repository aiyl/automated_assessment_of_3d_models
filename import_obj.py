# parse the file
import os
dir = os.path.abspath(os.curdir)
obj_filename = dir + '\check1.obj'
file = open(obj_filename, 'r')
polygons = []
err_face = 0
all_edges = []
all_verts = []
verts_coords = []

class Points:
    def __init__(self, point_number, verts_coords):
        self.point_number = point_number
        self.verts_coords = verts_coords

class Polygon:
    def __init__(self, pol_edges, points):
        self.pol_edges = pol_edges
        self.points = points

def check(edges1, edges2):
    boolean = False
    for n in range(len(edges1)):
        for m in range(len(edges2)):
            for k in range(len(edges2[m]) - 1):
                if (edges2[m][k] == edges1[n][k] and edges2[m][k + 1] == edges1[n][k + 1]) or (
                        edges2[m][k] == edges1[n][k + 1] and edges2[m][k + 1] == edges1[n][k]):
                    #return edges2[m]
                    boolean = True
                    return boolean
    return boolean

def check_adjacency(polygons):
    adjancy_list = []
    i=0
    while i < (len(polygons)):
        m = 1
        while m <(len(polygons)):
            if m!=i :
                #if Adjacency.check(self, polygons[i].pol_edges, polygons[m].pol_edges) is not None:
                if check(polygons[i].pol_edges, polygons[m].pol_edges):
                    list = []
                    list.append(i)
                    list.append(m)
                    #list.append(Adjacency.check(self, polygons[i].pol_edges, polygons[m].pol_edges))
                    adjancy_list.append(list)
            m+=1

        i=i+1
    return adjancy_list

def get_edge(faces_verts):
    edges = []
    for m in range(len(faces_verts)):
        list3=[]
        if m == len(faces_verts) - 1:
            list3.append(faces_verts[m])
            list3.append(faces_verts[0])
        else:
            list3.append(faces_verts[m])
            list3.append(faces_verts[m+1])
        edges.append(list3)
    return edges

def check_repeat(list):
    boolean = True
    for n in range(len(all_edges)):
        for m in range(len(all_edges[n]) - 1):
            if (all_edges[n][m] == list[0] and all_edges[n][m+1] == list[1]) or (all_edges[n][m] == list[1] and all_edges[n][m+1] == list[0]):
                boolean = False
    return boolean

def get_all_verts():
    for i in range(len(polygons)):
        all_verts.append(polygons[i].points.point_number)

def get_all_edges(all_verts):
    for n in range(len(all_verts)):
        for m in range(len(all_verts[n])):
            list3=[]
            if m == len(all_verts[n]) - 1:
                list3.append(all_verts[n][m])
                list3.append(all_verts[n][0])
            else:
                list3.append(all_verts[n][m])
                list3.append(all_verts[n][m+1])
                #edge = Edge(faces_verts[n][m], faces_verts[n][m+1])
            if check_repeat(list3) or len(all_edges) == 0:
                all_edges.append(list3)

def check_adjacency_edge():
    print('lol')
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
        verts_coords.append(list)

    elif words[0] == 'f':
        faceVertList = []
        for faceIdx in words[1:]:
            faceVertList.append(faceIdx)
        if not (len(faceVertList) == 4 or len(faceVertList) == 3):
            err_face+=1
        faces_verts = []  # индексы вершин грани(ей)
        vertices = []
        for i in range(len(faceVertList)):
            faces_verts.append(faceVertList[i].split('/')[0])
            vertices.append(verts_coords[int(faces_verts[i]) - 1])
        points = Points(faces_verts, vertices)
        polygon = Polygon(get_edge(faces_verts), points)
        polygons.append(polygon)
get_all_verts()
get_all_edges(all_verts)

for i in range(len(polygons)):
    print(i, polygons[i].points.point_number, polygons[i].points.verts_coords, polygons[i].pol_edges )
print('count err face ', err_face)
print('adj',check_adjacency(polygons))
print('all_edges ', len(all_edges), all_edges)

