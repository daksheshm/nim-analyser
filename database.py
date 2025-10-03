# database.py

import sqlite3

def get_db_connection():    

    # connect to the sqlite db
    
    conn = sqlite3.connect('nim_analysis.db')
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():

    # creating table if it dne
    
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

    # store current game info into db
    
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

    # checking db if state already exists
    
    conn = get_db_connection()
    cursor = conn.cursor()
    state_str = str(state)
    cursor.execute('SELECT * FROM game_states WHERE state = ?', (state_str,))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None
