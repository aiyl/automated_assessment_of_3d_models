import re
import sys
import accrue_points

reference = sys.argv[1]
solve = sys.argv[2]
txt_file = re.findall(r'\w+', solve)[-2] + '.txt'
result_path = sys.argv[3] + txt_file
args = ['obj', 'material', 'uv', 'voxel']

if __name__ == '__main__':
    points = accrue_points.Calc_points(reference, solve, result_path,  args)
