import random
import os
import sqlite3
import time

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
        self.game_over = False
        self.double = False
        self.player_total = 0
        self.dealer_total = 0
        self.player_alt = False
        self.dealer_alt = False
        self.player_high_total = 0
        self.dealer_high_total = 0

        #initialize values in case account does not currently exist in database
        self.balance = 1000
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0

        #check if account exists and load values if so OR create new account with default values if not
        self.get_data()

    def game(self):
        self.hit("player")
        self.hit("dealer")
        self.hit("player")
        self.hit("dealer")

        while not self.game_over:
            print("finish game")

    def hit(self, player):
        rand = random.randint(0, len(self.deck) - 1)
        num = self.deck.pop(rand)

        if player == "player":
            self.player_hand.append(num)
            self.player_hand_count += 1
        else:
            self.dealer_hand.append(num)
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

    def set_player_total(self):
        total = 0
        high_total = 0
        aces = 0
        for i in range(self.player_hand_count):
            card_value = ((self.player_hand[i] - 1) % 13) + 1
            if card_value == 1:
                total += 1
                high_total += 11
                aces += 1
            elif card_value > 1 and card_value < 11:
                total += card_value
                high_total += card_value
            else:
                total += 10
                high_total += 10

        while high_total > 21 and aces > 0:
            high_total -= 10 
            aces -= 1
        self.player_total = total
        self.player_high_total = high_total
        if total is not high_total:
            self.player_alt = True
        return
    
    def set_dealer_total(self):
        total = 0
        high_total = 0
        aces = 0
        for i in range(self.dealer_hand_count):
            card_value = ((self.dealer_hand[i] - 1) % 13) + 1
            if card_value == 1:
                total += 1
                high_total += 11
                aces += 1
            elif card_value > 1 and card_value < 11:
                total += card_value
                high_total += card_value
            else:
                total += 10
                high_total += 10

        while high_total > 21 and aces > 0:
            high_total -= 10 
            aces -= 1
        self.dealer_total = total
        self.dealer_high_total = high_total
        if total is not high_total:
            self.dealer_alt = True
        return
    
    def get_player_totals(self):
        return [self.player_total, self.player_high_total]

    def get_dealer_totals(self):
        return [self.dealer_total, self.dealer_high_total]
    

#################### Account Info Getters/Setters
    def set_balance(self, new_balance: int):
        self.balance = new_balance

    def get_balance(self):
        return self.balance

    def increment_win(self):
        self.games_won += 1
        self.games_played += 1

    def get_wins(self):
        return self.games_won

    def increment_loss(self):
        self.games_lost += 1
        self.games_played += 1

    def get_losses(self):
        return self.games_lost
    
    def get_games(self):
        return self.games_played
    
###################### Account Info Load/Save
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