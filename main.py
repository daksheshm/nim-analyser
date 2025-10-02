# main.py

import argparse
from game_logic import calculate_nim_sum, is_winning_position, get_optimal_move
from database import setup_database, store_game_analysis, query_state
from utils import format_analysis

def analyze_and_store(heaps):
    """
    Analyzes the game state and stores the result in the database.

    Args:
        heaps (list of int): The sizes of the heaps.
    """
    nim_sum = calculate_nim_sum(heaps)
    winning_pos = is_winning_position(heaps)
    optimal_move = get_optimal_move(heaps)

    store_game_analysis(heaps, nim_sum, winning_pos, optimal_move)

    return nim_sum, winning_pos, optimal_move

def main():
    """Main function to run the Nim Game Analyser."""
    parser = argparse.ArgumentParser(description="NIM Game Analyser")
    parser.add_argument('heaps', metavar='H', type=int, nargs='+',
                        help='An integer for the size of each heap.')

    args = parser.parse_args()
    heaps = args.heaps

    setup_database()

    cached_result = query_state(heaps)
    if cached_result:
        print("--- Analysis from Database ---")
        print(f"Game State: {cached_result['state']}")
        print(f"Nim-Sum (XOR Sum): {cached_result['nim_sum']}")
        print(f"Position Type: {'Winning' if cached_result['is_winning'] else 'Losing'}")
        print(f"Optimal Move: {cached_result['optimal_move']}")

    else:
        nim_sum, winning_pos, optimal_move = analyze_and_store(heaps)
        print(format_analysis(heaps, nim_sum, winning_pos, optimal_move))


if __name__ == "__main__":
    main()