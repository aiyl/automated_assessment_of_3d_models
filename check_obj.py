class Adjacency:
    def __init__(self, polygon_number, edge):
        self.polygon_number = polygon_number
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
        list = [] #DEL
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
                        pol_number = polygons[k].number
                        count += 1
            list.append(count)
            if count == 1:
                self.sep_edge_count += 1
                adj = Adjacency(pol_number, polygons[k].pol_edges[l])
                #print('debug', pol_number)
                self.sep_edges_list.append(adj)
            #count_adjacency.append(count)

            if count > 2:
                self.multiply_connected_geometry += 1
        print(list)
        self.check_separate_face(self.sep_edges_list)

    def check_separate_face(self, adjacency_edges):

       for i in range(len(adjacency_edges)):
           k = 0
           count = 1
           while i < len(adjacency_edges)-1:
               if adjacency_edges[k].polygon_number == adjacency_edges[i].polygon_number:
                    count += 1
               k +=1
           if count == len(self.obj.polygons[adjacency_edges[i].polygon_number-1].points.point_number):
               self.sep_face_count += 1

