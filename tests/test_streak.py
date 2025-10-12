import pytest
from streak import longest_positive_streak

def test_empty_list():
    assert longest_positive_streak([]) == 0

def test_no_positive_numbers():
    assert longest_positive_streak([-1, -5, 0]) == 0

def test_single_streak():
    assert longest_positive_streak([1, 2, 3, 4]) == 4

def test_multiple_streaks():
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_streak_at_end():
    assert longest_positive_streak([-1, 0, 1, 2, 3, 4, 5]) == 5
