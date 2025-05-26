import random
import os


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
    
    def get_data(self):
        player_exists = False
        user_data = []
        if os.path.exists("user_data.txt"):
            with open("user_data.txt", "r") as file:
                for line in file:
                    user_data = line.strip().split(" ")
                    if user_data[0] == self.player_name:
                        player_exists = True
                        break
                if not player_exists:
                    self.create_new_player(self.player_name)


    def create_new_player(self, player_name: str):
        default_line = f"{player_name} 1000 0 0 0\n"
        
        with open("user_data.txt", "a") as file:
            file.write(default_line)

    def set_balance(self, new_balance: int):
        self.balance = new_balance

    def increment_win(self):
        self.games_won += 1
        self.games_played += 1

    def increment_loss(self):
        self.games_lost += 1
        self.games_played += 1