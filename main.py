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

    choice = input("Scegli le opzioni:\n1) Genera una nuova matrice casuale \n2) Leggi la matrice dal file "
                   "/matrix.txt \n ")

    if choice == '2':
        print("Leggo la matrice...")
        with open('matrix.txt', 'r') as f_matrix:
            matrix = [[int(num) for num in line.split(' ')] for line in f_matrix]
    else:
        print("Genero la matrice...")
        matrix = ([random.choices(range(0, 2), k=columns_num) for _ in range(rows_num)])
        with open('matrix.txt', 'w') as out:
            for row in matrix:
                out.write(' '.join([str(a) for a in row]) + '\n')

    rot90 = rotate_matrix(pattern)
    rot180 = rotate_matrix(rot90)
    rot270 = rotate_matrix(rot180)

    res = evaluate_matrix(list(find_pattern(matrix, pattern)))
    res_90 = evaluate_matrix(list(find_pattern(matrix, rot90)))
    res_180 = evaluate_matrix(list(find_pattern(matrix, rot180)))
    res_270 = evaluate_matrix(list(find_pattern(matrix, rot270)))

    if res or res_90 or res_180 or res_270:
        print("Pattern individuato,\n")
        if res:
            print("Rotazione: 0 gradi")
        if res_90:
            print("Rotazione: 90 gradi")
        if res_180:
            print("Rotazione: 180 gradi")
        if res_270:
            print("Rotazione: 270 gradi")
    else:
        print("Pattern non presente")


def rotate_matrix(matrix):
    list_of_tuples = zip(*matrix[::-1])
    return [list(elem) for elem in list_of_tuples]


def evaluate_matrix(matrix):
    res = False
    for i in range(len(matrix)):
        if True in matrix[i]:
            res = True
            break
    return res


def find_pattern(matrix, pattern):
    sub_matrices_matrix = sliding_window_view(matrix, (len(pattern), len(pattern[0])))
    for sub_matrices_row in sub_matrices_matrix:
        yield [sub_matrix == pattern for sub_matrix in sub_matrices_row]


def sliding_window_view(matrix, window_shape):
    height, width = len(matrix), len(matrix[0])
    window_h, window_w = window_shape

    for y in range(height - window_h + 1):
        yield [
            [row[x:x + window_w] for row in matrix[y:y + window_h]]
            for x in range(width - window_w + 1)
        ]


main()
