import numpy as np
from PIL import Image
from skimage.measure import profile_line
from turtle import *
from math import sin, cos, radians

def get_pixels_array(image_name):
    """
    функция считывает картинку и возвращает массив значений яркости
    """
    # считываем картинку и получаем массив значений яркости
    with Image.open(image_name) as image:
        image.load()
        return np.array(image)

def get_circle_points():
    """
    функция выводит координаты (x, y) двухсот точек круга в пиксельной плоскости
    """
    # координаты по x двухсот точек круга
    x = np.arange(R, 2 * R + 1, int(R / (N / 4)))
    x = np.concatenate((x, x[::-1][1:], x[::-1][1:] - R, x[1:-1] - R)).astype(int)
    # если попадаем в условие, то точка находится на нижней полукоружности, поэтому
    # к радиуса прибавляем значение \sqrt(R^2 - (x - R)^2))
    # если нет, то точка находится на верхней полукоружности, поэтому
    # из радиуса вычитаем значение \sqrt(R^2 - (x - R)^2)
    i = 0
    coef = (-1 if 1 <= i + 1 <= int(N / 4) or int(N / 4) * 3 + 1 <= i + 1 <= N else 1)
    y = np.zeros(N)
    for i in range(N):
        y[i] = R + coef * (R ** 2 - (x[i] - R) ** 2) ** 0.5
    return np.transpose(np.array([x, y]))

def get_means_lens():
    """
    функция рассчитывает среднее значение пикселей на линии между каждой парой точек, а также
    <<расстояние>> (длину) между ними, которую мы используем как предподсчет средних значений
    для каждой линии чтобы впоследствии быстро делать перебор
    """
    # заводим двумерные массивы, в которые на позиции i,j и j,i будем записывать среднее значение
    # пикселей и расстояние от i-ой точки по кругу до j-ой точки по кругу
    means = np.zeros((N, N))
    lens = np.zeros((N, N))
    # рассчитываем C_N^2 значений и заносим их в массивы means и lens
    for i in range(N):
        for j in range(i, N):
            # считаем массив значений яркости на линии между i-ой и j-ой точками круга
            cur_line = profile_line(pixels, points[i], points[j], mode='reflect')
            # заносим в массивы среднее значение яркости и длину линии для i-ой и j-ой точек круга
            means[i, j] = means[j, i] = np.mean(cur_line)
            lens[i, j] = lens[j, i] = len(cur_line)
    return means, lens

def draw_picture():
    """
    Функция (из условия домашней работы), рисующая картинку по заданным ребрам
    """
    with open("edges.txt") as file:
        edges = file.read().strip().split("\n")
    tracer(False)
    vertices = []
    φ = 90
    for i in range(N):
        x = cos(radians(φ)) * R
        y = sin(radians(φ)) * R
        vertices.append((x, y))
        pu()
        goto(x, y)
        pd
        dot(10, "red")
        φ -= 360 / N
    for e in edges:
        v1, v2 = e.split()
        pu()
        goto(*vertices[int(v1) - 1])
        pd()
        goto(*vertices[int(v2) - 1])
    update()
    done()

def get_k_best_points(i, k):
    """
    функция, возвращающая k точек, проводя линию от i-ой точки круга до которых, будут получаться самые темные ребра
    """
    # если линия удовлетворяет условию (ребро не явлется петлей) и длина между точками i и j больше определенного
    # значения (чтобы избежать коротких ребер, которые, по сути соединяли бы очень близкие точки окружности)
    # таким значеинем минимальной длины эмпирически для данной картинки было подобрано значение 500
    best_points = np.array([(means[i, j], j) for j in range(N) if j != i and lens[i, j] > 500]).astype(int)
    # сортируем по возрастанию средней яркости и выбираем k точек с минимальной яркостью
    return list(best_points[best_points[:, 0].argsort()][:k][:, 1])

def gen_edges(k):
    """
    функция, генерирующая 200 * k ребер для рисования
    """
    # двумерный массив, в котором на i-ой позиции стоит массив точек, до которых будет проводиться ребро из точки i
    return [get_k_best_points(i, k) for i in range(N)]

def edges_ordering(edges, k):
    """
    функция, которая упорядочивает ребра графа в соответствии с просьбой в условии задачи
    <<Будет лучше, если ребра для построения будут укладываться по максимуму в цепочки>>
    """
    ordered_edges = []
    i = 0
    # проходим все N * k ребер
    for n in range(N * k):
        # если существует следующая вершина в пути, то берем ребро из текущей вершины в нее и заносим в список ребер
        if edges[i]:
            j = edges[i][0]
            edges[i] = edges[i][1:]
            ordered_edges.append([i, j])
            i = j
        # если не существует следующей вершины, то мы, скорее всего, обошли какую-то большею часть
        # компоненту связности, поэтому перейдем к следующей и  будем строим путь в ней O(N^2)
        else:
            for m in range(N):
                if edges[m]:
                    j = edges[m][0]
                    edges[m] = edges[m][1:]
                    ordered_edges.append([m, j])
                    i = j
                    break
    return ordered_edges

def edges_write(edges, file_name):
    """
    функция, которая записывает в txt-файл ребра
    """
    with open(file_name, 'w') as file:
        for v1, v2 in edges:
            file.write(f"{v1} {v2}\n")


N = 200  # Вершин
R = 500  # Радиус окружности визуализации

# вводим наименование jpg-файла
image_name = 'Поль Сезанн. Натюрморт с яблоками.jpg'

# получаем массив координат точек окружности, по которым будем проводить ребра
points = get_circle_points()

# получаем массив значений яркости для заданного jpg-файла, а также его высоту и ширину в количестве пикселей
pixels = get_pixels_array(image_name)
# делаем предподсчет (один раз) средних значений и длины для каждой линии в окружности
#means, lens = get_means_lens()

# записываем средние значения и длины линий в txt-файлы, чтобы быстро впоследствии его
# считывать и не перерасчитывать средние значения и длины линий
# np.savetxt("means.txt", means, delimiter=' ', newline='\n')
# np.savetxt("lengths.txt", lens, delimiter=' ', newline='\n')

# считаываем из txt-файлов средние значения и длины линий
means = np.loadtxt("means.txt")
lens = np.loadtxt("lengths.txt")

# задаем k - количество лучших ребер, которые будут браться для каждой вершины (т.е. всего ребер будет 200 * k)

k = 8

# генерируем ребра
edges = gen_edges(k)

# упорядочиваем ребра так, как попросили в условии задачи - то есть, по сути разбиваем граф на путь (либо на компоненты)
# связности, в каждой из которых находим путь
edges_ordered = edges_ordering(edges, k)
# записываем упорядоченные ребра в txt-файл
edges_write(edges_ordered, 'edges.txt')

# рисуем картинку, считыывая txt-файл
draw_picture()
