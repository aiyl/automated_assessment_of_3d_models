# parse the file
import os

class Polygon:
    def __init__(self, edge, points):
        self.edge = edge
        self.points = points

dir = os.path.abspath(os.curdir)
obj_filename = dir + '\check1.obj'
file = open(obj_filename, 'r')
verts = []
faces_verts = [] #индексы вершин грани(ей)
edges = []
i = 0
err_face = 0
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
        verts.append(list)

    elif words[0] == 'f':
        faceVertList = []
        for faceIdx in words[1:]:
            faceVertList.append(faceIdx)
        if not (len(faceVertList) == 4 or len(faceVertList) == 3):
            err_face+=1
        list2 = []
        for i in range(len(faceVertList)):
            list2.append(faceVertList[i].split('/')[0])
        faces_verts.append(list2)
        print('faceVertList', faceVertList)

def check(list):
    boolean = True
    for n in range(len(edges)):
        for m in range(len(edges[n]) - 1):
            if (edges[n][m] == list[0] and edges[n][m+1] == list[1]) or (edges[n][m] == list[1] and edges[n][m+1] == list[0]):
                boolean = False
    return boolean

for n in range(len(faces_verts)):
    for m in range(len(faces_verts[n])):
        list3=[]
        if m == len(faces_verts[n]) - 1:
            list3.append(faces_verts[n][m])
            list3.append(faces_verts[n][0])
        else:
            list3.append(faces_verts[n][m])
            list3.append(faces_verts[n][m+1])
            #edge = Edge(faces_verts[n][m], faces_verts[n][m+1])
        if check(list3) or len(edges) == 0:
            edges.append(list3)
print('edges ', edges)
print('count err face ', err_face)
print(verts)
print('faces verts ', faces_verts)
