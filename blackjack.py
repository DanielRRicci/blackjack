import random
import os
import sqlite3

conn = sqlite3.connect("player_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    name VARCHAR(20) PRIMARY KEY,
    value INTEGER DEFAULT(1000) NOT NULL,
    wins INTEGER DEFAULT(0) NOT NULL,
    losses INTEGER DEFAULT(0) NOT NULL,
    games INTEGER DEFAULT(0) NOT NULL
)
""")
conn.commit()

class BlackjackGame:

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.init_deck()
        self.player_hand_count = 0
        self.dealer_hand_count = 0
        self.deck_count = 52
        self.game_over = False
        self.double = False


        self.balance = 1000
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0

    def get_data(self):
        cursor.execute("SELECT * FROM players WHERE name = ?", (self.player_name,))
        result = cursor.fetchone()
        if result is not None:
            name, value, wins, losses, games = result
            self.balance = value
            self.games_won = wins
            self.games_lost = losses
            self.games_played = games
        else:
            cursor.execute("Insert into players (name) values (?)", (self.player_name,))
            conn.commit()
            
    def save_data(self):
        cursor.execute("UPDATE players SET value = ?, wins = ?, losses = ?, games = ? WHERE name = ? ", (self.player_name, self.balance, self.games_won, self.games_lost, self.games_played))
        conn.commit()

    def set_balance(self, new_balance: int):
        self.balance = new_balance

    def increment_win(self):
        self.games_won += 1
        self.games_played += 1

    def increment_loss(self):
        self.games_lost += 1
        self.games_played += 1

    def hit(self, player):
        rand = random.randint(0, self.deck_count)
        num = self.deck[rand]

        if self.player:
            self.player_hand[self.player_hand_count] = num
            self.player_hand_count += 1
        else:
            self.dealer_hand[self.dealer_hand_count] = num
            self.dealer_hand_count += 1

        self.deck_count -= 1

    def double(self):
        self.hit(True)
        self.double = True
        self.stand()

    def stand(self):
        self.game_over = True

    def get_card(self, num):
        suits = ['c', 'd', 'h', 's']
        suit = suits[self.num / 4]
        card = str(self.num % 4) + suit
        return card

    def init_deck(self):
        self.deck = list(range(52))

    def get_player_total(self):
        total = 0
        for i in range(self.player_hand_count):
            total += self.player_hand[i - 1]
        return total
    
    def get_dealer_total(self):
        total = 0
        for i in range(self.dealer_hand_count):
            total += self.dealer_hand[i - 1]
        return total