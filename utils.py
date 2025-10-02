# utils.py

def format_analysis(state, nim_sum, is_winning, optimal_move):
    """Formats the game analysis for display."""
    lines = [
        "--- Nim Game Analysis ---",
        f"Game State: {state}",
        f"Nim-Sum (XOR Sum): {nim_sum}",
        f"Position Type: {'Winning' if is_winning else 'Losing'}"
    ]
    if is_winning:
        lines.append(f"Optimal Move: Take {optimal_move[1]} from heap {optimal_move[0]}")
    else:
        lines.append("Optimal Move: No winning move available.")

    return "\n".join(lines)