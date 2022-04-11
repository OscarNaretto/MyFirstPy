import configparser
import random


def main():
    config = configparser.ConfigParser()
    config.read_file(open(r'settings.txt'))

    rows_num = int(config.get('Settings', 'rows_num'))
    columns_num = int(config.get('Settings', 'columns_num'))
    pattern_path = config.get('Settings', 'pattern_path')

    with open(pattern_path, 'r') as f_pattern:
        pattern = [[int(num) for num in line.split(' ')] for line in f_pattern]

    matrix = ([random.choices(range(0, 2), k=columns_num) for _ in range(rows_num)])
    with open('matrix.txt', 'w') as out:
        for row in matrix:
            out.write(' '.join([str(a) for a in row]) + '\n')

    res = False
    res_list = list(find_pattern(matrix, pattern))
    for i in range(len(res_list)):
        if True in res_list[i]:
            res = True
            break
    print(res)


def find_pattern(matrix, pattern):
    sub_matrices_matrix = sliding_window_view(matrix, (len(pattern), len(pattern[0])))
    for sub_matrices_row in sub_matrices_matrix:
        yield [sub_matrix == pattern for sub_matrix in sub_matrices_row]


def sliding_window_view(matrix, window_shape):
    h, w = len(matrix), len(matrix[0])
    window_h, window_w = window_shape

    for y in range(h - window_h + 1):
        yield [
            [row[x:x + window_w] for row in matrix[y:y + window_h]]
            for x in range(w - window_w + 1)
        ]


main()
