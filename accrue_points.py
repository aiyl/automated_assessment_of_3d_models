import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv
# import check_normals
import renders_compare
import voxel_compare


class Obj_points:
    point = 0

    def __init__(self, err_weight, max_point, errors, all_count):
        self.err_weight = err_weight
        self.max_point = max_point
        self.errors = errors
        self.all_count = all_count
        try:
            err_percent = (errors) / all_count
            if err_percent == 0:
                self.point = max_point
            else:
                self.point = max(int(round((1 - err_percent * err_weight) * max_point, 0)), 0)
        except Exception as e:

            raise SystemExit

class UV_points:
    point = 0

    def __init__(self, err_weight, max_point, errors, all_count):
        self.err_weight = err_weight
        self.max_point = max_point
        self.errors = errors
        self.all_count = all_count
        if errors < 80:
            err_weight = err_weight * 2
        err_percent = errors * 0.01
        self.point = max(int(round((err_percent / err_weight) * max_point, 0)), 0)


class Calc_points:
    point = 0

    def __init__(self, reference, solve, res_path, args):
        self.reference = reference
        self.solve = solve
        self.args = args
        self.res_path = res_path
        self.calc_points(args)

    def percentage_ratio(self,  points):
        max_point = len(points) * 10
        points_sum = sum(points)
        if max_point != 0:
            return round(points_sum * 10 / max_point, 2)
        else:
            return 0

    def calc_points(self, args):
        points = []
        f = open(self.res_path, 'w')
        obj = parse_obj.Obj(self.solve)
        if obj.logs == False:
            f.write('error during opening ' + self.solve + '\n')

        # check renders
        for i in range(len(args)):
            if args[i] == 'render':
                renders = renders_compare.Renders(self.reference, self.solve)
                points.append(renders.render_points)
                f.write('renders check point ' + str(renders.render_points) + '\n')
                # print('renders check', renders.render_points)

            # check_voxels
            if args[i] == 'voxel':
                voxels = voxel_compare.Voxels(self.reference, self.solve)
                vox_point = round(voxels.voxel_points/10, 2)
                points.append(vox_point)
                # print('voxel compare', voxels.voxel_points )
                f.write('voxels compare point ' + str(vox_point) + '\n')

            # check material
            if args[i] == 'material':
                mtl1 = parse_mtl.Mtl(self.reference)
                mtl2 = parse_mtl.Mtl(self.solve)
                if mtl2.logs =='':
                    checker = check_materials.Checker(mtl1, mtl2)
                    mat_point = checker.pointer()
                    if checker.need_material != '':
                        f.write('material check point ' + str(mat_point) + '\n' + 'can not find mestrials: ' + str(checker.need_material) + '\n')
                    else:
                        f.write('material check point ' + str(mat_point) + '\n')
                    points.append(mat_point)
                else:
                    f.write('material check point ' + mtl2.logs + '\n')
                # print('material points', checker.pointer())

            # check obj
            if args[i] == 'obj':
                if obj.logs == True:
                    check_geometry = check_obj.Check(obj)

                    f.write(
                        'separate face ' + str(check_geometry.sep_face_count) + ' separate_edge ' + str(
                            check_geometry.sep_edge_count) +
                        ' multiply_connected_geometry ' +
                        str(check_geometry.multiply_connected_geometry) + ' double vertices ' + str(
                            len(obj.double_vertices)) +
                        ' count face with more than 4 vertices ' + str(obj.err_face) + '\n')
                    point1 = Obj_points(30, 10, check_geometry.sep_face_count, len(obj.all_edges)).point
                    point2 = Obj_points(20, 10, check_geometry.sep_edge_count, len(obj.all_edges)).point
                    point3 = Obj_points(30, 10, check_geometry.multiply_connected_geometry, len(obj.all_edges)).point
                    point4 = Obj_points(10, 10, len(obj.double_vertices), len(obj.verts_coords)).point
                    point5 = Obj_points(10, 10, obj.err_face, len(obj.polygons)).point
                    obj_point = self.percentage_ratio([point1, point2, point3, point4, point5])
                else:
                    obj_point = 0
                points.append(obj_point)
                f.write('obj point ' + str(obj_point) + '\n')


            # check_uv
            if args[i] == 'uv':
                check_uv_map = check_uv.Check_UV(obj.polygons)
                if check_uv_map.logs != '':
                    f.write(check_uv_map.logs + '\n')
                f.write('UV point ' + str(check_uv_map.percent_busy / 10) + '\n')
                points.append(UV_points(1, 10, check_uv_map.percent_busy, 10).point)


        self.point = self.percentage_ratio(points)
        f.write('final score ' + str(self.point))
        # check_normals
        # check_normals = check_normals.Check_normals(obj.polygons)
        # check_normals = check_normals.Check_normals(obj)
        # print('err_normal_face', check_normals.err_normals_count)
        f.close()
