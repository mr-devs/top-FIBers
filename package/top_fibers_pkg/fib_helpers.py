"""
A collection of functions that are utilized in the calc_fib_indices.py script.
"""


def calc_fib_index(rt_counts):
    """
    Calculate a user's FIB-index based a list of the retweet counts they earned.

    Parameters:
    -----------
    - rt_counts (list) : list of retweet count values for retweets sent by a user

    Return:
    -----------
    - fib_position (int) : a user's FIB index

    Errors:
    -----------
    - TypeError
    """
    if not isinstance(rt_counts, list):
        raise TypeError("`rt_counts` must be a list!")

    rt_counts.sort()
    for fib_position in range(1, len(rt_counts) + 1)[::-1]:
        if rt_counts[-fib_position] >= fib_position:
            return fib_position

    # If the above criteria is never met, we return the fib_position as zero
    fib_position = 0
    return fib_position
