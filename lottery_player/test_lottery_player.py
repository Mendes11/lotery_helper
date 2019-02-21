import pytest

from lottery_player import generate_number_combinations


def test_combination_without_limit():
    combinations = generate_number_combinations(1, 4, 2)
    expected = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert combinations == expected


def test_combination_with_limit():
    combinations = generate_number_combinations(1, 4, 2, max_iter=2)
    expected = [(1, 2), (1, 3)]
    assert combinations == expected


def test_combination_with_random_selection():
    original = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    combinations = generate_number_combinations(1, 4, 2,
                                                random_selection=True)
    assert not set(combinations) - set(original)
    assert not combinations == original

def test_combination_different_range():
    combinations = generate_number_combinations(1, 3, 2)
    expected = [(1, 2), (1, 3), (2, 3)]
    assert combinations == expected

def test_combination_different_range_max_lower_than_min():
    with pytest.raises(ValueError) as exc:
        generate_number_combinations(3, 1, 2)
        assert exc == 'range_max must be higher than range_min'

def test_combination_different_range_not_enough_range_for_num_digits():
    with pytest.raises(ValueError) as exc:
        generate_number_combinations(1, 2, 3)
        assert exc == 'num_digits must be less or equal than the total range'
