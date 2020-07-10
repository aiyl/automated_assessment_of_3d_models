class Obj_points:
    def __init__(self, checker, err_weight, max_point, errors, all_count):
        self.checker = checker
        self.err_weight = err_weight
        self.max_point = max_point
        self.errors = errors
        self.all_count = all_count
        if checker == 'obj':
            err_percent = (errors)/all_count
            if err_percent == 0:
                p = max_point
            else:
                p = max(int(round((1 - err_percent * err_weight) * max_point, 0)), 0)
            print(p)
        elif checker == 'uv':
            err_percent = errors * 0.01
            p = max(int(round((err_percent * err_weight) * max_point, 0)), 0)
            print(p)

