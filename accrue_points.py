import parse_mtl
import check_materials
import parse_obj
import check_obj
import check_uv
import check_normals
import renders_compare
import voxel_compare
import json


class Calc_points:
    total_point = 0
    obj_max_point = 0

    def __init__(self, reference, solve, res_path, settings_path):
        self.reference = reference
        self.solve = solve
        self.res_path = res_path
        self.settings_path = settings_path
        self.calc_points()

    def percentage_ratio(self, points):
        max_point = len(points) * 10  # config
        points_sum = sum(points)
        if max_point != 0:
            return round(points_sum * 10 / max_point, 2)
        else:
            return 0

    def obj_points(self, j, obj_pointer, errors):
        variable = {
            0: 'separate_face_point',
            1: 'separate_edge_point',
            2: "multyply_geometry_point",
            3: "double_vertices_point",
            4: "err_vertices_point",
            5: "polygons_count_point"

        }.get(j)
        maxpoint = obj_pointer[j].get(variable).get('max_point')
        err_weight1 = obj_pointer[j].get(variable).get('err_weight1')
        err_weight2 = obj_pointer[j].get(variable).get('err_weight2')
        err_weight3 = obj_pointer[j].get(variable).get('err_weight3')
        err_count1 = obj_pointer[j].get(variable).get('err_count1')
        err_count2 = obj_pointer[j].get(variable).get('err_count2')
        err_count3 = obj_pointer[j].get(variable).get('err_count3')
        self.obj_max_point += maxpoint
        if j == 5:
            return {
                errors <= err_count1: maxpoint,
                err_count1 < errors <= err_count2: maxpoint - err_weight1,
                err_count2 < errors <= err_count3: maxpoint - err_weight2,
                errors > err_count3: 0
            }[True]
        else:
            return {
            errors == 0: maxpoint,
            0 < errors < err_count1: maxpoint - err_weight1,
            err_count1 <= errors < err_count2: maxpoint - err_weight2,
            err_count2 <= errors < err_count3: maxpoint - err_weight3,
            errors > err_count3: 0
            }[True]

    def uv_points(self, uv_pointer, area):
        maxpoint = uv_pointer.get('max_point')
        err_weight1 = uv_pointer.get('err_weight1')
        err_weight2 = uv_pointer.get('err_weight2')
        err_weight3 = uv_pointer.get('err_weight3')
        err_count1 = uv_pointer.get('err_count1')
        err_count2 = uv_pointer.get('err_count2')
        err_count3 = uv_pointer.get('err_count3')

        return {
            area >= err_count3: maxpoint,
            err_count2 <= area < err_count3: maxpoint - err_weight1,
            err_count1 <= area < err_count2: maxpoint - err_weight2,
            area < err_count1: maxpoint - err_weight3
        }[True]

    def normals_points(self, normals_pointer, errors):
        maxpoint = normals_pointer.get('max_point')
        err_weight1 = normals_pointer.get('err_weight1')
        err_weight2 = normals_pointer.get('err_weight2')
        err_weight3 = normals_pointer.get('err_weight3')
        err_count1 = normals_pointer.get('err_count1')
        err_count2 = normals_pointer.get('err_count2')
        err_count3 = normals_pointer.get('err_count3')
        return {
            errors == 0: maxpoint,
            0 < errors < err_count1: maxpoint - err_weight1,
            err_count1 <= errors < err_count2: maxpoint - err_weight2,
            err_count2 <= errors < err_count3: maxpoint - err_weight3,
            errors > err_count3: 0
        }[True]
    def calc_points(self):

        try:
            with open(self.settings_path) as json_data:
                data = json.load(json_data)
        except Exception as e:
            print(e)

        args = data['config']
        points = []
        f = open(self.res_path, 'w')

        obj = parse_obj.Obj(self.solve)
        if obj.logs == False:
            f.write('error during opening ' + self.solve + '\n')

        for i in range(len(args)):
            # check renders
            if args[i] == 'renders':
                renders = renders_compare.Renders(self.reference, self.solve)
                points.append(renders.render_points)
                f.write('renders check point ' + str(renders.render_points) + '\n')
                # print('renders check', renders.render_points)

            # check_voxels
            if args[i] == 'voxels':
                voxels = voxel_compare.Voxels(self.reference, self.solve)
                if voxels.logs == '':
                    vox_point = round(voxels.voxel_points / 10, 2)
                else:
                    vox_point = 0
                    f.write(voxels.logs + '\n')
                points.append(vox_point)
                # print('voxel compare', voxels.voxel_points )
                f.write('voxels compare point ' + str(vox_point) + '\n')

            # check material
            if args[i] == 'materials':
                reference_mtl_path = data['reference_mtl_path']
                solve_mtl_path = data['solve_mtl_path']
                mtl1 = parse_mtl.Mtl(self.reference, reference_mtl_path)
                mtl2 = parse_mtl.Mtl(self.solve, solve_mtl_path)
                if mtl2.logs != '':
                    f.write('material check point ' + mtl2.logs + '\n')
                    mat_point = 0
                else:
                    checker = check_materials.Checker(mtl1, mtl2)
                    mat_point = checker.pointer()
                    if checker.need_material != '':
                        f.write('material check point ' + str(mat_point) + '\n' + 'can not find mestrials: ' + str(
                            checker.need_material) + '\n')
                    else:
                        f.write('material check point ' + str(mat_point) + '\n')
                points.append(mat_point)

            # check obj
            if args[i] == 'obj':
                if obj.logs == True:
                    check_geometry = check_obj.Check(obj)
                    obj_pointer = (data['OBJ_points'])
                    err_sep_face_point = self.obj_points(0, obj_pointer, check_geometry.sep_face_count)
                    err_edge_point = self.obj_points(1, obj_pointer, check_geometry.sep_edge_count)
                    err_multiply_geom_point = self.obj_points(2, obj_pointer,
                                                              check_geometry.multiply_connected_geometry)
                    err_double_verts_point = self.obj_points(3, obj_pointer, len(obj.double_vertices))
                    err_face_point = self.obj_points(4, obj_pointer, obj.err_face)
                    polygon_count = self.obj_points(5, obj_pointer, len(obj.polygons))
                    f.write(
                        'separate face ' + str(check_geometry.sep_face_count) + ' separate_edge ' + str(
                            check_geometry.sep_edge_count) +
                        ' multiply_connected_geometry ' +
                        str(check_geometry.multiply_connected_geometry) + ' double vertices ' + str(
                            len(obj.double_vertices)) +
                        ' count face with more than 4 vertices ' + str(obj.err_face) + '\n' )
                    obj_point = sum([err_sep_face_point, err_edge_point, err_multiply_geom_point, err_double_verts_point,
                                    err_face_point, polygon_count])/self.obj_max_point*10
                else:
                    obj_point = 0
                points.append(obj_point)
                f.write('obj point ' + str(obj_point) + '\n')

            if args[i] == 'uv':
                uv_pointer = (data['UV_points'])
                if obj.texture_logs == '':
                    check_uv_map = check_uv.Check_UV(obj.polygons)
                    if check_uv_map.logs == '':
                        uv_point = self.uv_points(uv_pointer, check_uv_map.polygon_areas)
                    else:
                        uv_point = 0
                        f.write(check_uv_map.logs + '\n')
                else:
                    uv_point = 0
                    f.write(obj.texture_logs + '\n')
                points.append(uv_point)
                f.write('UV point ' + str(uv_point) + '\n')

            # check normals
            if args[i] == 'normals':
                normals_pointer = (data['Normals_points'])
                checking_normals = check_normals.Check_normals(obj, self.solve)
                if checking_normals.logs == 'object is not a convex hull. Cannot count inverted normals':
                    if checking_normals.err_normals == False:
                        normals_point = 0
                    else:
                        normals_point = normals_pointer.get('max_point')
                    f.write(checking_normals.logs + '\n')
                elif checking_normals.logs =='':
                    normals_point = self.normals_points(normals_pointer, checking_normals.err_normals_count)
                    f.write('count of wrongly aligned normals '+str(checking_normals.err_normals_count) + '\n' + 'normals point '+ str(normals_point) +'\n')
                elif checking_normals.logs !='':
                    normals_point = self.normals_points(normals_pointer, int(checking_normals.err_normals_count/2))
                    f.write(checking_normals.logs + str(checking_normals.err_normals_count) + '\n')
                points.append(normals_point)
                f.write('normals check point '+str(normals_point) + '\n')
        self.total_point = self.percentage_ratio(points)
        f.write('total score ' + str(self.total_point))
        f.close()
