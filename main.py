import re
import sys
import accrue_points
from aao3m import accrue_points as check_all
reference = sys.argv[1]
solve = sys.argv[2]
txt_file = re.findall(r'\w+', solve)[-2] + '.txt'
result_path = sys.argv[3] + txt_file #sys.argv[3] - путь к папке
args = ['obj',  'voxel', 'material']

if __name__ == '__main__':
    #points = accrue_points.Calc_points(reference, solve, result_path,  args)
    checker = check_all.Calc_points(reference, solve, result_path,  args)