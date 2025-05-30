import pygame
from sys import exit
from game.core import BlackjackGame
from game.assets import load_assets

# Import screen functions
from game.screens.base import BaseScreen
from game.screens.title import TitleScreen
from game.screens.name import NameScreen
from game.screens.bet import BetScreen
from game.screens.game import GameScreen
from game.screens.result import ResultScreen

# Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# Load all shared fonts/surfaces/assets
assets = load_assets()

def main():
    adjust = True
    should_quit = False
    # TITLE SCREEN
    title_screen = TitleScreen(screen, assets, clock)
    title_screen.run()
    # NAME ENTRY
    name_screen = NameScreen(screen, assets, clock)
    player_name = name_screen.run()
    if not player_name:
        return  # Quit if no name entered

    # Create a game instance for the player
    game = BlackjackGame(player_name)

    while not should_quit:
        # BETTING SCREEN
        if adjust:
            bet_screen = BetScreen(screen, game, assets, clock)
            bet_value = bet_screen.run()
            
        game.start_round(bet_value)

        # GAME SCREEN (main gameplay)
        game_screen = GameScreen(screen, game, bet_value, assets, clock)
        game_screen.run()

        # RESULT SCREEN (win/loss/payout options)
        result_screen = ResultScreen(screen, game, bet_value, assets, clock)
        result = result_screen.run()
        adjust = result[0]
        should_quit = result[1]

# Start the game
if __name__ == "__main__":
    main()
    pygame.quit()
    exit()
