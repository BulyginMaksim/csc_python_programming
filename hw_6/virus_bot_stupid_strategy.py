import numpy as np
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action='store_const', const='WeakestBot', help='Name of the bot')
    return parser


n = 10

def get_input():  # получаем на вход состояние игры
    matrix = []
    for _ in range(n):
        matrix.append(list(map(int, list(input()))))
    player_status = int(input())
    return player_status, np.array(matrix)


def replace_position(matrix):  # если предлагают ходить за 2, то свапаем матрицу на pi рад. и свапаем значения
    matrix = matrix[::-1, ::-1]
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 1:
                matrix[i, j] = 2
            elif matrix[i, j] == 2:
                matrix[i, j] = 1
            elif matrix[i, j] == 3:
                matrix[i, j] = 4
            elif matrix[i, j] == 4:
                matrix[i, j] = 3
    return matrix


def swap_corners(matrix):  # для удобства индексации отзеркаливаем матрицу относительно оси абсцисс
    return matrix[::-1]


def get_square(matrix, status_matrix, i, j):  # находим все доступные места в квадрате длины 3 с центром в (i, j)
    for k in range(i - 1, i + 2):
        for l in range(j - 1, j + 2):
            if 0 <= k <= n - 1 and 0 <= l <= n - 1 and matrix[k, l] == 0:
                status_matrix[k, l] = 1
            elif 0 <= k <= n - 1 and 0 <= l <= n - 1 and matrix[k, l] == 2:
                status_matrix[k, l] = 2

    return status_matrix

def check_begin(matrix):
    if np.sum(matrix[:3, :3]) == 0:
        return True
    else:
        return False

def get_available_positions(matrix):  # находим все доступные места для хода в текущем состоянии игры
    status_matrix = np.zeros((n, n), dtype=int)
    flag = False
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 1:
                if status_matrix[i, j] == 0:
                    flag = True
                status_matrix = get_square(matrix, status_matrix, i, j)
                if flag:
                    status_matrix[i, j] = 0
                    flag = False
    kill = []
    go = []
    for i in range(n):
        for j in range(n):
            if status_matrix[i, j] == 1:
                go.append((i, j))
            elif status_matrix[i, j] == 2:
                kill.append((i, j))
    return go, kill


def return_out(matrix):  # возвращаем поле после того как сходили
    for row in matrix:
        print(*row, sep="")


def main():
    parser = create_parser()
    if parser.parse_args().name:  # если хотят чтобы бот представился
        print(parser.parse_args().name)
    else:  # если бот должен сделать ходы
        player_status, matrix = get_input()  # принимаем текущее поле

        status_replaced = False  # статус того, свапались ли местами крестики и нолики

        if player_status == 2:  # если предлагается сделать ход за нолики, то свапаем матрицу и ходим за крестики
            matrix = replace_position(matrix)
            status_replaced = True

        matrix = swap_corners(matrix)  # инвертируем матрицу относительно оси абсцисс для удобства индексации
        if check_begin(matrix):
            matrix[:3, :3] = np.array([[1, 1, 0],[1, 0, 0],[0, 0, 0]])
        else:
            go, kill = get_available_positions(matrix)  # находим доступные для хода позиции

            k = len(go)
            m = len(kill)
            if m >= 3:
                pos = kill[:3]
            else:
                pos = kill
                pos = pos + go
            s = 0
            while s < 3:
                if s - 1 < m - 1:
                    i, j = pos[s]
                    matrix[i, j] = 4
                elif s - 1 < len(pos) - 1:
                    i, j = pos[s]
                    matrix[i, j] = 1
                s += 1
        matrix = swap_corners(matrix)  # инвертируем обратно матрицу относительно оси абсцисс
        if status_replaced:  # если матрица свапалась, то свапаем ее обратно
            matrix = replace_position(matrix)
        return_out(matrix)  # принтуем поле после того как сходили


main()
