import pytest

from lottery_player.exceptions import WrongRangeException
from lottery_player.lottery_player import generate_number_combinations, \
    expected_list_size


def test_is_not_list():
    combinations = generate_number_combinations(1, 4, 2)
    assert type(combinations) != list

def test_combination_without_limit():
    combinations = generate_number_combinations(1, 4, 2)
    expected = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert list(combinations) == expected


def test_combination_different_range():
    combinations = generate_number_combinations(1, 3, 2)
    expected = [(1, 2), (1, 3), (2, 3)]
    assert list(combinations) == expected


def test_combination_different_range_max_lower_than_min():
    with pytest.raises(WrongRangeException) as exc:
        generate_number_combinations(3, 1, 2)
        assert exc == '"Valor Mínimo" deve ser menor do que o ' \
                      '"Valor Máximo".'


def test_combination_different_range_not_enough_range_for_num_digits():
    with pytest.raises(WrongRangeException) as exc:
        generate_number_combinations(1, 2, 3)
        assert exc == '"Número de Dígitos" deve ser menor ou ' \
                      'igual ao período de valores acima.'


def test_combination_different_initial_range():
    combinations = generate_number_combinations(2, 4, 2)
    expected = [(2, 3), (2, 4), (3, 4)]
    assert list(combinations) == expected


def test_expected_list_size():
    size = expected_list_size(range_min=1, range_max=4, num_digits=2)
    expected = 6
    assert size == expected


def test_expected_list_size_higher_range():
    size = expected_list_size(range_min=1, range_max=6, num_digits=2)
    expected = 15
    assert size == expected


def test_expected_list_size_more_digits():
    size = expected_list_size(range_min=1, range_max=4, num_digits=3)
    expected = 4
    assert size == expected


def test_expected_list_size_different_min_range():
    size = expected_list_size(range_min=2, range_max=4, num_digits=2)
    expected = 3
    assert size == expected
