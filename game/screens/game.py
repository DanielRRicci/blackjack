import pygame
import os
from .base import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, screen, game, bet_value, assets, clock):
        super().__init__(screen, assets)
        self.game = game
        self.bet_value = bet_value
        self.clock = clock
        self.fonts = assets['fonts']
        self.warning_font = self.fonts['30']
        self.button_font = self.fonts['50']
        self.balance_surf = self.fonts['50'].render("Balance:", False, 'Black')
        self.balance_rect = self.balance_surf.get_rect(topleft = (1150, 30))
        self.player_total_text_surf = self.fonts['30'].render("Player Total", False, 'Black')
        self.player_total_text_rect = self.player_total_text_surf.get_rect(center = (200, 600))

    def run(self):
        # , game, base_path, bet_value
        clock = pygame.time.Clock()
        animation = False

        while not self.game.is_game_over():
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True

            mouse_pos = pygame.mouse.get_pos()
            screen = self.screen
            assets = self.assets

            # Draw background and base board
            screen.blit(assets['board'], assets['board_rect'])

            # Deck stack
            deck_rect = assets["card_back"].get_rect(center = (120, 150))
            for i in range(13):
                screen.blit(assets['card_back'], (deck_rect.left + 2 * i, deck_rect.top + 2 * i))

            # Buttons
            self._draw_button('hit', mouse_pos, clicked, self.game.player_hit, animation, -315)
            self._draw_button('stand', mouse_pos, clicked, self.game.stand, animation, -65)
            self._draw_button('double', mouse_pos, clicked, self.game.double, animation, 250)

            # Balance display
            screen.blit(self.balance_surf, self.balance_rect)
            balance_display = self.button_font.render(str(self.game.balance), False, 'Black')
            screen.blit(balance_display, balance_display.get_rect(midtop = self.balance_rect.midbottom))

            # Player total
            p_totals = self.game.get_player_totals()
            total_text = f"{p_totals[0]}/{p_totals[1]}" if p_totals[0] != p_totals[1] else str(p_totals[0])
            total_surf = self.warning_font.render(total_text, False, 'Black')
            screen.blit(self.player_total_text_surf, self.player_total_text_rect)
            screen.blit(total_surf, total_surf.get_rect(midtop = self.player_total_text_rect.midbottom))

            # Player cards
            self._draw_hand(self.game.player_hand, y=750)

            # Dealer face-down card + 1 revealed
            self._draw_dealer_hand_partial()

            pygame.display.update()
            self.clock.tick(60)

    def _draw_hand(self, hand, y):
        x = 75
        for card in hand:
            card_surf = self.assets['cards'][self.game.get_card(card)]
            self.screen.blit(card_surf, card_surf.get_rect(midleft=(x, y)))
            x += 136

    def _draw_dealer_hand_partial(self):
        x = 75
        y = 350

        # Dealer's first (face-up) card
        card_key = self.game.get_card(self.game.dealer_hand[0])
        card_surf = self.assets['cards'][card_key]
        self.screen.blit(card_surf, card_surf.get_rect(midleft=(x, y)))

        # Face-down card
        x += 136
        card_back_surf = self.assets['card_back']
        self.screen.blit(card_back_surf, card_back_surf.get_rect(midleft=(x, y)))


    def _draw_button(self, name, mouse_pos, clicked, action, animation, offset):
        hit_surf = self.fonts['50'].render(name, False, 'Grey')
        hit_surf_hover = self.fonts['50'].render(name, False, 'Black')
        hit_rect = hit_surf.get_rect(center = (self.assets['board_rect'].centerx + offset, self.assets['board_rect'].centery + 100))
        double_warn_surf = self.fonts['30'].render("Double would exceed current Balance", False, 'Red')
        double_warn_rect = double_warn_surf.get_rect(center = (self.assets['board_rect'].centerx, 200))

        self.screen.blit(hit_surf, hit_rect)

        if hit_rect.collidepoint(mouse_pos):
            self.screen.blit(hit_surf_hover, hit_rect)
            if name == 'double' and self.game.balance < self.bet_value:
                self.screen.blit(double_warn_surf, double_warn_rect)
            elif clicked and not animation:
                action()
                
