import itertools
from math import factorial

import xlsxwriter

from random import shuffle, choice, sample

from lottery_player.exceptions import WrongRangeException


def generate_number_combinations(range_min, range_max, num_digits,
                                 max_iter=None, random_selection=False):
    if range_min > range_max:
        raise WrongRangeException('"Valor Mínimo" deve ser menor do que o '
                                  '"Valor Máximo".')
    if range_max - range_min +1 <= num_digits:
        raise WrongRangeException('"Número de Dígitos" deve ser menor ou '
                                  'igual ao período de valores acima.')

    combinations = itertools.combinations(range(range_min, range_max+1),
                                               num_digits)
    # if random_selection:
    #     shuffle(combinations)
    # if max_iter is not None:
    #     return combinations[:max_iter]
    return combinations


def expected_list_size(range_min, range_max, num_digits):
    num_values = range_max - range_min + 1
    numerator = factorial(num_values)
    denominator = factorial(num_digits) * factorial(num_values - num_digits)
    return int(numerator / denominator)


def populate_excel_worksheet(worksheet, data, selected_indexes=None):
    for row, line in enumerate(data):
        if selected_indexes is not None and row not in selected_indexes:
            continue
        for col, cell in enumerate(line):
            worksheet.write(row, col, cell)
    return worksheet


def generate_excel_file(filename, data, selected_indexes=None):
    """
    Generates an excel file that will store all data in a table form

    data must be a list of tuples or a matrix

    :param filename: str
    :param data: list
    :return: file-like
    """
    workbook = xlsxwriter.Workbook(filename)
    populate_excel_worksheet(workbook.add_worksheet(), data, selected_indexes)
    workbook.close()


def create_lottery_helper_file(range_min, range_max, n_digits,
                              max_combinations, is_random, filepath):
    # First, creates a generator, preventing it from overflowing memory
    combinations = generate_number_combinations(range_min, range_max,
                                                n_digits)
    selected_indexes = None
    if max_combinations is not None and not is_random:
        selected_indexes = range(0, max_combinations)
    elif max_combinations is not None and is_random:
        total_size = expected_list_size(range_min, range_max, n_digits)
        selected_indexes = sample(range(0, total_size), max_combinations)
    generate_excel_file(filepath, combinations,
                        selected_indexes=selected_indexes)
