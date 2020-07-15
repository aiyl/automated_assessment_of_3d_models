import re
import sys
import accrue_points
#from aao3m import accrue_points as check_all
reference = sys.argv[1] #Путь к эталону
solve = sys.argv[2] #путь к решению участника
txt_file = re.findall(r'\w+', solve)[-2] + '.txt'
result_path = sys.argv[3] + txt_file #sys.argv[3] - путь к папке в этой папке создастся файл txt
args = [   'normals']

if __name__ == '__main__':
    points = accrue_points.Calc_points(reference, solve, result_path,  args)
    #checker = check_all.Calc_points(reference, solve, result_path,  args)