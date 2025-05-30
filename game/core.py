import random
import os
import sqlite3
import time
from . import database

class BlackjackGame:

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.bet = 0
        database.initialize_db()
        self.balance, self.games_won, self.games_lost, self.games_tied, self.games_played = database.get_data(player_name)

    def start_round(self, new_bet):
        self.place_bet(new_bet)

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
        self.balance -= self.bet
        self.bet *= 2
        self.player_hit()
        if not self.game_over:
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
        self.deck.clear()
        self.player_hand.clear()
        self.dealer_hand.clear()
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
        # if high > self.get_player_totals()[1]:
        #     return False
        if low != high:
            return (high < 18)
        else:
            return (low < 17)
        
    def pay(self):
        if not self.paid:
            self.balance += self.payout()
            self.paid = True
            database.save_data(self.player_name, self.balance, self.games_won, self.games_lost, self.games_tied, self.games_played)
        
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

    def increment_win(self):
        self.games_won += 1
        self.games_played += 1

    def increment_loss(self):
        self.games_lost += 1
        self.games_played += 1
    
    def increment_ties(self):
        self.games_tied += 1
        self.games_played += 1