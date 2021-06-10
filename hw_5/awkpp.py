import argparse
import csv
import math
import random
import re
import statistics
from io import TextIOWrapper
from zipfile import ZipFile

PATTERN = re.compile(r'.+.csv')

# делаем так, чтобы библиотеки, импортируемые в этой
# библиотеке не подключались автоматически при импорте библиотеки
__all__ = [
    'get_file_info',
    'read_file_and_write_output',
    'get_info_read_write'
]


def create_parser():
    """
    Эта функция отвечает за возможность библиотеки принимать
    дополнительный параметр - имя файла с инструкциями.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('awkpp_file_name', nargs='?')
    return parser


def get_file_info(awkpp_file_name):
    """
    Эта функция открывает файл с инструкциями и получает
    название csv-файла, а также условие фильтра строк.
    """
    with open(awkpp_file_name, encoding="utf-8") as file:
        file_name = file.readline().strip()
        print(file_name)
        # поскольку в примерах файла к ДЗ вторая строка
        # пустая, то считаем ее пустой и считываем, ничего не делая
        file.readline()
        # записываем в список условия, после чего собираем
        # их с помощью join и скобочек, поскольку внутри одного условия,
        # то есть одной строки, может вылезти конструкция
        # следующего вида: condition1 or condition2,
        # в одно выражение все условия фильтрации
        condition = f"({') and ('.join([line.strip() for line in file])})"
    return file_name, condition


def read_file_and_write_output(file_name, bool_expression):
    """
    Эта функция отвечает за открытие csv-файла,
    фильтр и запись в output.csv строчек, удовлетворяющих условию.
    """
    try:
        # используем try-except для фиксирования потенциальных ошибок
        with ZipFile(file_name) as zf:
            with zf.open(PATTERN.findall(file_name)[0], 'r') as infile:
                with open('output.csv',
                          "w",
                          newline='',
                          encoding='utf-8-sig') as csv_file:
                    # открываем csv-файл в котором будем
                    # проверять по фильтру строчки и csc-файл output
                    reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))
                    writer = csv.DictWriter(
                        csv_file,
                        fieldnames=reader.fieldnames)
                    # перебираем все строки в csv-файле
                    # проверяем на истинность выражение - если
                    # оно истинно, то записываем строку в output.csv
                    writer.writerows([row for row in reader
                                      if eval(bool_expression)])
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def get_info_read_write(file_name_awkpp):
    """
    Эта функция комбинирует функции get_file_info и
    read_file_and_write_output в одной функции.
    """
    file_name, bool_expression = get_file_info(file_name_awkpp)
    read_file_and_write_output(file_name, bool_expression)


if __name__ == '__main__':
    parser = create_parser().parse_args()
    # с помощью argparse принимаем параметр - имя файла
    if parser.awkpp_file_name:
        # если на вход был параметр - имя файла, то запускаем обратку csv-файла
        file_name, bool_expression = get_file_info(parser.awkpp_file_name)
        read_file_and_write_output(file_name, bool_expression)
