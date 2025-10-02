# database.py

import sqlite3

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('nim_analysis.db')
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Creates the game_states table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS game_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL UNIQUE,
            nim_sum INTEGER NOT NULL,
            is_winning BOOLEAN NOT NULL,
            optimal_move TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def store_game_analysis(state, nim_sum, is_winning, optimal_move):
    """
    Stores the analysis of a game state in the database.

    Args:
        state (list of int): The game state (heap sizes).
        nim_sum (int): The calculated Nim-sum.
        is_winning (bool): Whether the position is winning.
        optimal_move (tuple): The optimal move (heap_index, items_to_take).
    """
    conn = get_db_connection()
    state_str = str(state)
    optimal_move_str = str(optimal_move) if optimal_move[0] is not None else "N/A"

    try:
        conn.execute('''
            INSERT INTO game_states (state, nim_sum, is_winning, optimal_move)
            VALUES (?, ?, ?, ?)
        ''', (state_str, nim_sum, is_winning, optimal_move_str))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def query_state(state):
    """
    Queries the database for a previously analyzed game state.

    Args:
        state (list of int): The game state to query.

    Returns:
        dict: A dictionary with the analysis if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    state_str = str(state)
    cursor.execute('SELECT * FROM game_states WHERE state = ?', (state_str,))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None