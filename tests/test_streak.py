import pytest
from streak import longest_positive_streak

def test_empty_list():
    """Test that an empty list returns a streak of 0."""
    assert longest_positive_streak([]) == 0

def test_multiple_streaks():
    """Test that the function returns the length of the longest streak."""
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_zeros_and_negatives():
    """Test that zeros and negative numbers break the streak."""
    assert longest_positive_streak([1, 2, 0, 3, 4, -5, 6]) == 2

def test_all_positive():
    """Test a list with all positive numbers."""
    assert longest_positive_streak([1, 1, 1]) == 3

def test_no_positive():
    """Test a list with no positive numbers."""
    assert longest_positive_streak([-1, -2, 0, -5]) == 0

def test_streak_at_end():
    """Test a list where the longest streak is at the end."""
    assert longest_positive_streak([1, -2, 3, 4, 5]) == 3

def test_streak_at_beginning():
    """Test a list where the longest streak is at the beginning."""
    assert longest_positive_streak([1, 2, 3, -4, 5]) == 3
