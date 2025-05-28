import random
import os
import sqlite3
import time

DB_PATH = "player_data.db"

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name VARCHAR(20) PRIMARY KEY,
        value INTEGER NOT NULL,
        wins INTEGER DEFAULT(0) NOT NULL,
        losses INTEGER DEFAULT(0) NOT NULL,
        ties INTEGER DEFAULT(0) NOT NULL,
        games INTEGER DEFAULT(0) NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_data(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result is not None:
        _, value, wins, losses, ties, games = result
    else:
        cursor.execute("Insert into players (name, value, wins, losses, ties, games) values (?, 1000, 0, 0, 0, 0)", (name,))
        conn.commit()
        value, wins, losses, ties, games = 1000, 0, 0, 0, 0

    conn.close()
    return value, wins, losses, ties, games
        
def save_data(name, balance, wins, losses, ties, games):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE players
        SET value = ?, wins = ?, losses = ?, ties = ?, games = ?
        WHERE name = ?
    """, (balance, wins, losses, ties, games, name))
    
    conn.commit()
    conn.close()