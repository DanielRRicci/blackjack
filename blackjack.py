import random
import os
import sqlite3
import time

conn = sqlite3.connect("player_data.db")
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

class BlackjackGame:

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []

        self.get_data()

    def start_round(self):
        self.player_hand_count = 0
        self.dealer_hand_count = 0
        self.game_over = False
        self.past_init = False
        self.can_double = True
        self.paid = False
        self.dealer_bust = False
        self.player_blackjack = False
        self.can_blackjack = True
        self.player_bust = False
        self.player_win = False
        self.dealer_win = False
        self.push = False
        self.player_total = 0
        self.dealer_total = 0
        self.player_alt = False
        self.dealer_alt = False
        self.player_high_total = 0
        self.dealer_high_total = 0
        self.bet = 0


        self.init_deck()
        self.player_hit()
        self.dealer_hit()
        self.player_hit()
        self.dealer_hit()
        self.can_blackjack = False
        self.past_init = True

    def player_hit(self):
        rand = random.randint(0, len(self.deck) - 1)
        num = self.deck.pop(rand)
        self.player_hand.append(num)
        self.player_hand_count += 1
        self.set_player_total()
        self.check_game_state()
        if self.past_init:
            self.can_double = False

    def dealer_hit(self):
        rand = random.randint(0, len(self.deck) - 1)
        num = self.deck.pop(rand)
        self.dealer_hand.append(num)
        self.dealer_hand_count += 1
        self.set_dealer_total()

    def double(self):
        self.player_hit()
        self.bet *= 2
        self.stand()

    def stand(self):
        while self.should_dealer_draw():
            self.dealer_hit()
        self.game_over = True
        self.check_game_state()
        
    def place_bet(self, bet_value: int):
        self.bet = bet_value
        self.balance -= bet_value

    def get_card(self, num):
        suits = ['c', 'd', 'h', 's']
        suit = suits[num // 13]
        card = str((num % 13) + 1) + suit
        return card

    def init_deck(self):
        self.deck = list(range(52))

    def set_player_total(self):
        total = 0
        high_total = 0
        aces = 0
        for i in range(self.player_hand_count):
            card_value = (self.player_hand[i] % 13) + 1
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
            card_value = (self.dealer_hand[i] % 13) + 1
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
    
    def is_game_over(self):
        return self.game_over
    
    def check_game_state(self):
        total = self.get_player_totals()[0]
        high_total = self.get_player_totals()[1]
        d_total = self.get_dealer_totals()[0]
        d_high_total = self.get_dealer_totals()[1]
        if (total == 21 or high_total == 21) and self.can_blackjack == True:
            self.player_blackjack = True
            self.game_over = True
            self.player_win = True
            self.dealer_win = False
            self.increment_win()
        elif total > 21:
            self.player_bust = True
            self.game_over = True
            self.player_win = False
            self.dealer_win = True
            self.increment_loss()
        elif d_total > 21:
            self.game_over = True
            self.player_win = True
            self.dealer_win = False
            self.dealer_bust = True
            self.increment_win()
        elif self.is_game_over() == True and high_total == d_high_total:
            self.push = True
            self.player_win = False
            self.dealer_win = False
            self.game_over = True
            self.increment_ties()
        elif high_total > d_high_total and self.game_over:
            self.player_win = True
            self.dealer_win = False
            self.increment_win()
        elif high_total < d_high_total and self.game_over:
            self.player_win = False
            self.dealer_win = True
            self.increment_loss()
        
    def should_dealer_draw(self):
        low = self.get_dealer_totals()[0]
        high = self.get_dealer_totals()[1]
        if high > self.get_player_totals()[1]:
            return False
        if low != high:
            return (high < 18)
        else:
            return (low < 17)
        
    def pay(self):
        if not self.paid:
            self.balance += self.payout()
            self.paid = True
            self.save_data()
        
    def payout(self):
        payout = self.bet
        if self.player_blackjack:
            payout = int(self.bet * 2.5)
        elif self.push:
            payout = self.bet
        elif self.player_win:
            payout = self.bet * 2
        else:
            payout = 0
        return payout

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
    
    def increment_ties(self):
        self.games_tied += 1
        self.games_played += 1
    
    def get_games(self):
        return self.games_played
    
###################### Account Info Load/Save
    def get_data(self):
        cursor.execute("SELECT * FROM players WHERE name = ?", (self.player_name,))
        result = cursor.fetchone()
        if result is not None:
            name, value, wins, losses, ties, games = result
            name = name
            self.balance = value
            self.games_won = wins
            self.games_lost = losses
            self.games_tied = ties
            self.games_played = games
            print("Result not none")
            print(value)
        else:
            cursor.execute("Insert into players (name, value, wins, losses, ties, games) values (?, 1000, 0, 0, 0, 0)", (self.player_name,))
            conn.commit()
            print("Result none")
            self.get_data()
            
    def save_data(self):
        cursor.execute("""UPDATE players SET name = ?, value = ?, wins = ?, 
                       losses = ?, ties = ?, games = ? WHERE name = ?""", 
                       (self.player_name, self.balance, self.games_won, self.games_lost, self.games_tied, self.games_played, self.player_name))
        print(str(self.balance) + " balance")
        conn.commit()