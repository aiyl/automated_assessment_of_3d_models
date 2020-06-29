# parse the file
import os
from functools import reduce

import math
import numpy as np

dir = os.path.abspath(os.curdir)
obj_filename = dir + '/Tests/check1.obj'
file = open(obj_filename, 'r')
polygons = []
err_face = 0
all_edges = []
all_verts2 = []
all_verts = []
verts_coords = []
normals_coords= []
count = 0

class Points:
    def __init__(self, point_number, verts_coords):
        self.point_number = point_number
        self.verts_coords = verts_coords


class Polygon:
    def __init__(self, pol_edges, points, normals):
        self.pol_edges = pol_edges
        self.points = points
        self.normals = normals


def check(edges1, edges2):
    boolean = False
    for n in range(len(edges1)):
        for m in range(len(edges2)):
            for k in range(len(edges2[m]) - 1):
                if (edges2[m][k] == edges1[n][k] and edges2[m][k + 1] == edges1[n][k + 1]) or (
                        edges2[m][k] == edges1[n][k + 1] and edges2[m][k + 1] == edges1[n][k]):
                    # return edges2[m]
                    boolean = True
                    return boolean
    return boolean


def check_adjacency(polygons):
    adjancy_list = []
    i = 0
    while i < (len(polygons)):
        m = 1
        while m < (len(polygons)):
            if m != i:
                # if Adjacency.check(self, polygons[i].pol_edges, polygons[m].pol_edges) is not None:
                if check(polygons[i].pol_edges, polygons[m].pol_edges):
                    list = []
                    list.append(i)
                    list.append(m)
                    # list.append(Adjacency.check(self, polygons[i].pol_edges, polygons[m].pol_edges))
                    adjancy_list.append(list)
            m += 1

        i = i + 1
    return adjancy_list


def get_edge(faces_verts):
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


def check_repeat(list,list2):
    boolean = True
    for n in range(len(list2)):
        for m in range(len(list2[n]) - 1):
            if (list2[n][m] == list[0] and list2[n][m + 1] == list[1]) or (
                    list2[n][m] == list[1] and list2[n][m + 1] == list[0]):
                boolean = False
    return boolean


def get_all_verts():
    for i in range(len(polygons)):
        all_verts.append(polygons[i].points.point_number)


def get_all_edges(all_verts):
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
            if check_repeat(list3, all_edges) or len(all_edges) == 0:
                all_edges.append(list3)

def check_adjacency_edge():
    count_adjacency = []
    err_edge_adjacency = 0
    for i in range(len(all_edges)):
        #print(all_edges[i])
        count = 0
        for k in range (len(polygons)):
            for l in range(len(polygons[k].pol_edges)):
                if (polygons[k].pol_edges[l][0] == all_edges[i][0] and polygons[k].pol_edges[l][1] == all_edges[i][1]) or \
                        (polygons[k].pol_edges[l][1] == all_edges[i][0] and polygons[k].pol_edges[l][0] == all_edges[i][1]):
                    count+=1
        count_adjacency.append(count)
                #print(polygons[k].pol_edges)
    #print(count)
    for i in range(len(count_adjacency)):
        if count_adjacency[i] != 2:
            err_edge_adjacency += 1

            print('error! this edge has more or less than 2 adjacency face ', i)
    return err_edge_adjacency

def points_different(p1, p2):
    vector = []
    for i in range(len(p1)):
        vector.append(p2[i] - p1[i])
    return vector

def vector_multiplication(v1, v2):
    vector = []
    vector.append(v1[1] * v2[2] - v1[2] * v2[1])
    vector.append(v1[2] * v2[0] - v1[0] * v2[2])
    vector.append(v1[0] * v2[1] - v1[1] * v2[0])
    return vector
def add_vectors(v, w):
    return [vi - wi for vi, wi in zip(v, w)]
def sum_vectors(v, w):
    return [vi - wi for vi, wi in zip(v, w)]

def sum_of_all_vectors(vecs):
    return reduce(sum_vectors, vecs)

def check_normals(polygon, number):
    p = []
    #print('pol number', number)
    for i in range(len(polygon.points.verts_coords)):
        p.append(polygon.points.verts_coords[i])
    b = np.array(points_different([0, 0, 0], p[0]))
    a = np.array(points_different([0, 0, 0], p[1]))
    c = np.array(points_different([0, 0, 0], p[2]))
    x = add_vectors(b, a)
    y = add_vectors(c, a)
    N = vector_multiplication(x, y)
    lol = float(N[0]*N[0] + N[1]*N[1]+ N[2]*N[2])
    delitel = math.sqrt(lol)
    sum = sum_of_all_vectors(polygon.normals.verts_coords)
    #print('sum', sum)
    string = str(polygon.normals.verts_coords[0][0]).split('.')[1]
    round = len(string)
    for i in range(len(N)):
        N[i] = N[i]/delitel
        N[i] = np.round(N[i], round)
    for k in range(len(polygon.normals.verts_coords)):
        if N!=polygon.normals.verts_coords[k]:
            print('bad')
            print('has to be', N, 'real', polygon.normals.verts_coords[k])
        else:
            print('good')

   # p1 = np.linspace(polygon.normals.verts_coords[1])
   # p2 = np.linspace(polygon.normals.verts_coords[2])

if __name__ == '__main__':
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
            all_verts2.append(list)
        elif words[0] == 'vn':
            x, y, z = float(words[1]), float(words[2]), float(words[3])
            list2 = []
            list2.append(x)
            list2.append(y)
            list2.append(z)
            normals_coords.append(list2)
        elif words[0] == 'f':
            faceVertList = []
            normal_list = []
            for faceIdx in words[1:]:
                faceVertList.append(faceIdx)
            if not (len(faceVertList) == 4 or len(faceVertList) == 3):
                err_face += 1
            faces_verts = []  # индексы вершин грани(ей)
            vertices = []
            normals = []
            for i in range(len(faceVertList)):
                faces_verts.append(faceVertList[i].split('/')[0])
                normal_list.append(faceVertList[i].split('/')[2])
                vertices.append(verts_coords[int(faces_verts[i]) - 1])
                normals.append(normals_coords[int(normal_list[i])-1])
            points = Points(faces_verts, vertices)
            normal = Points(normal_list, normals)
            polygon = Polygon(get_edge(faces_verts), points, normal)
            polygons.append(polygon)
    get_all_verts()
    get_all_edges(all_verts)
    for i in range(len(polygons)):
        print(i, 'points', polygons[i].points.point_number, 'points coord', polygons[i].points.verts_coords, 'edges', polygons[i].pol_edges, 'normals number', polygons[i].normals.point_number, 'normal coords', polygons[i].normals.verts_coords )
    print('count err face ', err_face)
    for i in range(len(polygons)):
        check_normals(polygons[i], i)
    print('adj', check_adjacency(polygons))
    print('adj err_edge count', check_adjacency_edge())
    print('all_edges ', len(all_edges), 'all verts', len(all_verts2), 'polygons', len(polygons))
