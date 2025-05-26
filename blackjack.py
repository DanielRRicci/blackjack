import random
import os


class BlackjackGame:
    def __init__(self, player_name: str):
        
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.init_deck()
        self.player_hand_count = 0
        self.dealer_hand_count = 0
        self.deck_count = 52
        self.game_over = False
        self.double = False
        self.money = self.load_money()

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
    
    def load_money(self):
        if os.path.exists("money.txt"):
            with open("money.txt", "r") as file:
                try:
                    return int(file.read())
                except ValueError:
                    return 1000  # fallback if file is corrupted
        else:
            # File doesn't exist, create it with default value
            with open("money.txt", "w") as file:
                file.write("1000")
            return 1000
        
    def save_money(self, money):
        with open("money.txt", "w") as file:
            file.write(str(money))

    def update_money(self, amount):
        self.money += amount
        self.save_money(self.money)
