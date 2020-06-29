class Adjacency:
    def __init__(self, polygon, edge):
        self.polygon = polygon
        self.edge = edge

class Check:
    sep_edges_list = []
    sep_face_count = 0
    sep_edge_count = 0
    multiply_connected_geometry = 0

    def __init__(self, obj):
        self.obj = obj
        self.check_adjacency_edge()

    def check_adjacency_edge(self):
        global adj
        all_edges = self.obj.all_edges
        polygons = self.obj.polygons
        count_adjacency = []
        for i in range(len(all_edges)):
            count = 0
            for k in range(len(polygons)):
                for l in range(len(polygons[k].pol_edges)):
                    if (polygons[k].pol_edges[l][0] == all_edges[i][0] and polygons[k].pol_edges[l][1] == all_edges[i][
                        1]) or \
                            (polygons[k].pol_edges[l][1] == all_edges[i][0] and polygons[k].pol_edges[l][0] ==
                             all_edges[i][1]):
                        count += 1
            if count == 1:
                self.sep_edge_count +=1
                adj = Adjacency(polygons[k], polygons[k].pol_edges[l])
                self.sep_edges_list.append(adj)
                self.check_separate_face(self.sep_edges_list)
            #count_adjacency.append(count)

            if count > 2:
                self.multiply_connected_geometry += 1

    def check_separate_face(self, adjacency_edges):
       count = 0
       for i in range(len(adjacency_edges)):
           k = 1
           count = 0
           while k < len(adjacency_edges)-1:
               if adjacency_edges[k].polygon.number == adjacency_edges[i].polygon.number:
                    count += 1
               k +=1
       if count == 4:
           self.sep_face_count += 1

