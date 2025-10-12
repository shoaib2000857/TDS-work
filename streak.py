def longest_positive_streak(nums: list[int]) -> int:
    """
    Calculates the length of the longest run of consecutive values
    strictly greater than 0.

    Args:
        nums: A list of integers.

    Returns:
        The length of the longest positive streak.
    """
    max_streak = 0
    current_streak = 0
    for num in nums:
        if num > 0:
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
            current_streak = 0

    # Final check in case the longest streak is at the end
    if current_streak > max_streak:
        max_streak = current_streak

    return max_streak
