# game_logic.py

from functools import reduce

def calculate_nim_sum(heaps):
    # binary xor of all elements
    return reduce(lambda x, y: x ^ y, heaps)

def is_winning_position(heaps):
    
    # check if current game is a winning state
    
    return calculate_nim_sum(heaps) != 0

def get_optimal_move(heaps):
    
    nim_sum = calculate_nim_sum(heaps) 
    if nim_sum == 0: #losing pos no optimal moves
        return (None, None) 

    for i, heap_size in enumerate(heaps):
        target_size = heap_size ^ nim_sum
        if target_size < heap_size:
            return (i, heap_size - target_size)

    return (None, None) 
