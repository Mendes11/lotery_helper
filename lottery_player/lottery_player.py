import itertools
import xlsxwriter

from random import shuffle


def generate_number_combinations(range_min, range_max, num_digits,
                                 max_iter=None, random_selection=False):
    if range_min > range_max:
        raise ValueError('range_max must be higher than range_min')
    if range_max - range_min +1 <= num_digits:
        raise ValueError('num_digits must be less or equal than the total '
                         'range')
    combinations = list(itertools.combinations(range(range_min, range_max+1),
                                               num_digits))
    if random_selection:
        shuffle(combinations)
    if max_iter is not None:
        return combinations[:max_iter]
    return combinations


def populate_excel_worksheet(worksheet, data):
    for row, line in enumerate(data):
        for col, cell in enumerate(line):
            worksheet.write(row, col, cell)
    return worksheet


def generate_excel_file(filename, data):
    """
    Generates an excel file that will store all data in a table form

    data must be a list of tuples or a matrix

    :param filename: str
    :param data: list
    :return: file-like
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = populate_excel_worksheet(workbook.add_worksheet(), data)
    workbook.close()


def create_lottery_helper_file(range_min, range_max, n_digits,
                              max_combinations, is_random, filepath):
    combinations = generate_number_combinations(range_min, range_max,
                                                n_digits,
                                                max_combinations, is_random)
    generate_excel_file(filepath, combinations)
