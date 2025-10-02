# game_logic.py

from functools import reduce

def calculate_nim_sum(heaps):
    """
    Calculates the Nim-sum of the game state, which is the XOR sum of the heap sizes.

    Args:
        heaps (list of int): A list representing the sizes of the heaps.

    Returns:
        int: The Nim-sum of the heaps.
    """
    return reduce(lambda x, y: x ^ y, heaps)

def is_winning_position(heaps):
    """
    Determines if the current game state is a winning or losing position.
    A position is a losing position if the Nim-sum is 0.

    Args:
        heaps (list of int): The current sizes of the heaps.

    Returns:
        bool: True if it's a winning position, False otherwise.
    """
    return calculate_nim_sum(heaps) != 0

def get_optimal_move(heaps):
    """
    Computes the optimal move from a given game state.

    Args:
        heaps (list of int): The current sizes of the heaps.

    Returns:
        tuple: A tuple containing the index of the heap to take from and the number of items to take.
               Returns (None, None) if it's a losing position (no winning move).
    """
    nim_sum = calculate_nim_sum(heaps)
    if nim_sum == 0:
        return (None, None) 

    for i, heap_size in enumerate(heaps):
        target_size = heap_size ^ nim_sum
        if target_size < heap_size:
            return (i, heap_size - target_size)

    return (None, None) 